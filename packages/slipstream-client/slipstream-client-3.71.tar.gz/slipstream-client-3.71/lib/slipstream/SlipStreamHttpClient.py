"""
 SlipStream Client
 =====
 Copyright (C) 2013 SixSq Sarl (sixsq.com)
 =====
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from __future__ import print_function

import os
import json
from collections import defaultdict

import slipstream.util as util
import slipstream.exceptions.Exceptions as Exceptions

from slipstream.UserInfo import UserInfo
from slipstream.HttpClient import HttpClient
from slipstream.NodeInstance import NodeInstance
from slipstream.NodeDecorator import NodeDecorator

etree = util.importETree()


class SlipStreamHttpClient(object):
    URL_IGNORE_ABORT_ATTRIBUTE_QUERY = '?ignoreabort=true'

    def __init__(self, configHolder):
        self.category = None
        self.run_dom = None
        self.ignoreAbort = False
        self.username = ''
        self.password = ''
        self.diid = ''
        self.node_instance_name = ''
        self.serviceurl = ''
        self.verboseLevel = None
        self.retry = True

        configHolder.assign(self)
        self._assemble_endpoints()
        self.httpClient = HttpClient(configHolder=configHolder)
        self.httpClient.init_session(self.serviceurl)
        self.api = self.httpClient.get_ss_api()

    def set_retry(self, retry):
        self.retry = retry

    def _assemble_endpoints(self):
        self.runEndpoint = self.serviceurl + util.RUN_RESOURCE_PATH
        self.run_url = self.runEndpoint + '/' + self.diid

        self.userEndpoint = '%s/user/%s' % (self.serviceurl,
                                            self.username)

        self.configuration_endpoint = '%s%s' % (self.serviceurl,
                                                util.CONFIGURATION_RESOURCE_PATH)

    @staticmethod
    def _strip_unwanted_attrs(resource):
        unwanted = ('id', 'resourceURI', 'acl', 'operations',
                    'created', 'updated', 'name', 'description', 'properties')
        for k in resource.keys():
            if k in unwanted:
                del resource[k]
        return resource

    def _get_user(self):
        _, jresp = self.httpClient.get(self.serviceurl + '/api/user/%s' % self.username,
                                       accept='application/json')
        return self._strip_unwanted_attrs(json.loads(jresp))

    def _get_user_params(self):
        _, jresp = self.httpClient.get(self.serviceurl + '/api/user-param',
                                       accept='application/json')
        user_params = json.loads(jresp)
        if user_params.get('count', 0) < 1:
            raise Exception('No user params found for %s.' % self.username)
        return self._strip_unwanted_attrs(user_params.get('userParam')[0])

    def _get_cloud_cred(self, cloud_qualifier):
        creds = self._get_cloud_creds(cloud_qualifier)
        cred = self._strip_unwanted_attrs(creds.get('credentials')[0])
        cred[UserInfo.CLOUD_USERNAME_KEY] = cred.get('key', '')
        cred[UserInfo.CLOUD_PASSWORD_KEY] = cred.get('secret', '')
        return cred

    def _get_cloud_creds(self, cloud_qualifier):
        _filter = "$filter=type^='cloud-cred' and connector/href='connector/%s'" % \
                  cloud_qualifier
        _, jresp = self.httpClient.put(self.serviceurl + '/api/credential?%s' % _filter,
                                       accept='application/json')
        creds = json.loads(jresp)
        if creds.get('count', 0) < 1:
            raise Exception('No cloud creds found for %s with %s.' % (self.username, _filter))
        return creds

    def _get_connector_conf(self, cloud_qualifier):
        _, jresp = self.httpClient.get(self.serviceurl + '/api/connector/%s' % cloud_qualifier,
                                       accept='application/json')
        return self._strip_unwanted_attrs(json.loads(jresp))

    def get_user_info(self, cloud_qualifier):

        user_info = UserInfo(cloud_qualifier)

        user = self._get_user()
        if 'password' in user:
            del user['password']
        user_info.set_user_params(user)

        user_info.set_general_params(self._get_user_params())

        if cloud_qualifier:
            connector_conf = self._get_connector_conf(cloud_qualifier)
            connector_conf.update(self._get_cloud_cred(cloud_qualifier))
            user_info.set_cloud_params(connector_conf)

        return user_info

    def _extractModuleResourceUri(self, run):
        rootElement = etree.fromstring(run.encode('utf-8'))
        return rootElement.attrib[NodeDecorator.MODULE_RESOURCE_URI]

    def get_nodes_instances(self, cloud_service_name=None):
        '''Return dict {<node_instance_name>: NodeInstance, }
        '''
        nodes_instances = {}

        self._retrieveAndSetRun()

        nodes_instances_runtime_parameters = \
            DomExtractor.extract_nodes_instances_runtime_parameters(self.run_dom, cloud_service_name)

        nodes_runtime_parameters = DomExtractor.extract_nodes_runtime_parameters(self.run_dom)

        for node_instance_name, node_instance_runtime_parameters in nodes_instances_runtime_parameters.items():

            node_instance = NodeInstance(node_instance_runtime_parameters)
            node_name = node_instance.get_node_name()

            if nodes_runtime_parameters:
                node_runtime_parameters = nodes_runtime_parameters.get(node_name, {})
                if node_runtime_parameters:
                    node_instance.set_parameter(NodeDecorator.MAX_PROVISIONING_FAILURES_KEY,
                        node_runtime_parameters.get(NodeDecorator.MAX_PROVISIONING_FAILURES_KEY, '0'))

            image_attributes = DomExtractor.extract_node_image_attributes(self.run_dom, node_name)
            node_instance.set_image_attributes(image_attributes)

            image_targets = DomExtractor.extract_node_image_targets(self.run_dom, node_name)
            node_instance.set_image_targets(image_targets)

            build_state = DomExtractor.extract_node_image_build_state(self.run_dom, node_name)
            node_instance.set_build_state(build_state)

            nodes_instances[node_instance_name] = node_instance

        return nodes_instances

    def _get_nodename(self):
        'Node name derived from the node instance name.'
        return self.node_instance_name.split(
            NodeDecorator.NODE_MULTIPLICITY_SEPARATOR)[0]

    def get_run_category(self):
        self._retrieveAndSetRun()
        return DomExtractor.extractCategoryFromRun(self.run_dom)

    def get_run_type(self):
        self._retrieveAndSetRun()
        return DomExtractor.extractTypeFromRun(self.run_dom)

    def get_run_mutable(self):
        self._retrieveAndSetRun()
        return DomExtractor.extract_mutable_from_run(self.run_dom)

    def discard_run(self):
        self.run_dom = None

    def _retrieveAndSetRun(self):
        if self.run_dom is None:
            url = self.run_url
            _, run = self._retrieve(url)
            self.run_dom = etree.fromstring(run.encode('utf-8'))

    def _retrieve(self, url):
        return self._httpGet(url, 'application/xml')

    def execute(self, resourceUri):
        url = self.runEndpoint
        return self._httpPost(url, resourceUri, 'text/plain')

    def complete_state(self, node_instance_name):
        url = '%s/%s:%s' % (self.run_url, node_instance_name,
                            NodeDecorator.COMPLETE_KEY)
        url += SlipStreamHttpClient.URL_IGNORE_ABORT_ATTRIBUTE_QUERY
        return self._httpPost(url, 'reset', 'text/plain')

    def terminate_run(self):
        return self._httpDelete(self.run_url)

    def _fail(self, message):
        self.setRuntimeParameter(
            NodeDecorator.globalNamespacePrefix + NodeDecorator.ABORT_KEY, message)

    def sendReport(self, report):
        resource_id = self._create_external_object_report(report)
        upload_url = self._generate_upload_url_external_object_report(resource_id)
        self._upload_report(upload_url, report)
        self._set_report_ready(resource_id)

    def _create_external_object_report(self, report_path):
        resp = self.api.cimi_add('externalObjects',
                                 {'externalObjectTemplate': {'href': 'external-object-template/report',
                                                             'runUUID': self.diid,
                                                             'component': self.node_instance_name,
                                                             'filename': os.path.basename(report_path),
                                                             'contentType': 'application/tar+gzip'}})
        return resp.json['resource-id']

    def _generate_upload_url_external_object_report(self, resource_id):
        resp = self.api.cimi_operation(resource_id, "http://sixsq.com/slipstream/1/action/upload")
        return resp.json['uri']

    def _upload_report(self, url, report):
        self._printDetail('Uploading report to: %s' % url)
        body = open(report, 'rb').read()
        self._httpPut(url, body, 'application/tar+gzip', accept="*/*")

    def _set_report_ready(self, resource_id):
        self.api.cimi_operation(resource_id, "http://sixsq.com/slipstream/1/action/ready")

    def isAbort(self):
        return self.getGlobalAbortMessage() != ''

    def getGlobalAbortMessage(self):
        url = '%s/%s%s' % (self.run_url,
                           NodeDecorator.globalNamespacePrefix,
                           NodeDecorator.ABORT_KEY)
        url += SlipStreamHttpClient.URL_IGNORE_ABORT_ATTRIBUTE_QUERY
        _, content = self._httpGet(url, accept='text/plain')
        return content.strip().strip('"').strip("'")

    def get_run_parameters(self):
        self._retrieveAndSetRun()
        return DomExtractor.extract_run_parameters_from_run(self.run_dom)

    def getRuntimeParameter(self, key, ignoreAbort=False):

        url = self.run_url + '/' + key
        if self.ignoreAbort or ignoreAbort:
            url += SlipStreamHttpClient.URL_IGNORE_ABORT_ATTRIBUTE_QUERY
        try:
            _, content = self._httpGet(url, accept='text/plain')
        except Exceptions.NotFoundError as ex:
            raise Exceptions.NotFoundError('"%s" for %s' % (str(ex), key))

        return content.strip().strip('"').strip("'")

    def setRuntimeParameter(self, key, value, ignoreAbort=False):
        url = self.run_url + '/' + key
        if self.ignoreAbort or ignoreAbort:
            url += SlipStreamHttpClient.URL_IGNORE_ABORT_ATTRIBUTE_QUERY

        _, content = self._httpPut(url, util.removeASCIIEscape(value),
                                   accept='text/plain')

        return content.strip().strip('"').strip("'")

    def unset_runtime_parameter(self, key, ignore_abort=False):
        url = '%s/%s' % (self.run_url, key)

        if (self.ignoreAbort or ignore_abort):
            url += SlipStreamHttpClient.URL_IGNORE_ABORT_ATTRIBUTE_QUERY

        self._httpDelete(url)

    def _httpGet(self, url, accept='application/xml'):
        return self.httpClient.get(url, accept, retry=self.retry)

    def _httpPut(self, url, body=None, contentType='application/xml', accept='application/xml'):
        return self.httpClient.put(url, body, contentType, accept, retry=self.retry)

    def _httpPost(self, url, body=None, contentType='application/xml'):
        return self.httpClient.post(url, body, contentType, retry=self.retry)

    def _httpDelete(self, url, body=None):
        return self.httpClient.delete(url, body=body, retry=self.retry)

    def _printDetail(self, message):
        util.printDetail(message, self.verboseLevel, util.VERBOSE_LEVEL_DETAILED)

    def put_new_image_id(self, image_resource_uri, image_id):
        url = self.serviceurl + '/' + image_resource_uri
        self._printDetail('Set new image id: %s %s' % (url, image_id))
        self._httpPut(url, image_id)

    def launchDeployment(self, params):
        body = '&'.join(params)
        resp, _ = self._httpPost(self.runEndpoint, body,
                                 contentType='text/plain')
        return resp.headers['location']

    def getRunState(self, uuid=None, ignoreAbort=True):
        if not uuid and not self.diid:
            raise Exceptions.ExecutionException("Run ID should be provided "
                                                "to get state.")
        state_key = NodeDecorator.globalNamespacePrefix + NodeDecorator.STATE_KEY
        self.run_url = self.runEndpoint + '/' + (uuid or self.diid)
        return self.getRuntimeParameter(state_key, ignoreAbort=ignoreAbort)

    def remove_instances_from_run(self, node_name, ids, detele_ids_only=True):
        """ids : []
        """
        url = '%s/%s' % (self.run_url, node_name)
        body = "ids=%s" % ','.join(map(str, ids))
        if detele_ids_only:
            body = body + '&delete-ids-only=true'
        self._httpDelete(url, body=body)

    def get_server_configuration(self):
        _, config = self._retrieve(self.configuration_endpoint)
        return config

    def login(self, username, password):
        self.api.login_internal(username=username, password=password)

    def logout(self):
        self.api.logout()

    def get_session(self):
        return self.httpClient.get_session()

    def get_api(self):
        return self.api


class DomExtractor(object):
    EXTRADISK_PREFIX = 'extra.disk'
    EXTRADISK_VOLATILE_KEY = EXTRADISK_PREFIX + '.volatile'

    PATH_TO_NODE_ON_RUN = 'module/nodes/entry/node'
    PATH_TO_PARAMETER = 'parameters/entry/parameter'

    @staticmethod
    def extract_nodes_instances_runtime_parameters(run_dom, cloud_service_name=None):
        """Return dict {<node_instance_name>: {<runtimeparamname>: <value>, }, }
        """
        nodes_instances = {}
        for node_instance_name in run_dom.attrib['nodeNames'].split(','):
            node_instance_name = node_instance_name.strip()

            node_instance = {}
            node_instance[NodeDecorator.NODE_INSTANCE_NAME_KEY] = node_instance_name

            # Unfortunately, this doesn't work on Python < 2.7
            # query = "runtimeParameters/entry/runtimeParameter[@group='%s']" % node_instance_name
            query = "runtimeParameters/entry/runtimeParameter"
            for rtp in run_dom.findall(query):
                if rtp.get('group') == node_instance_name:
                    key = DomExtractor._get_key_from_runtimeparameter(rtp)
                    node_instance[key] = rtp.text
            nodes_instances[node_instance_name] = node_instance

        if cloud_service_name is not None:
            for node_instance_name in nodes_instances.keys():
                if cloud_service_name != nodes_instances[node_instance_name][NodeDecorator.CLOUDSERVICE_KEY]:
                    del nodes_instances[node_instance_name]

        return nodes_instances

    @staticmethod
    def extract_nodes_runtime_parameters(run_dom):
        """Return dict {<node_name>: {<runtimeparamname>: <value>, }, }
        """
        nodes = {}
        node_names = DomExtractor._get_node_names(run_dom)

        for node_name in node_names:
            node = {}
            node[NodeDecorator.NODE_NAME_KEY] = node_name

            # Unfortunately, this doesn't work on Python < 2.7
            # query = "runtimeParameters/entry/runtimeParameter[@group='%s']" % node_instance_name
            query = "runtimeParameters/entry/runtimeParameter"
            for rtp in run_dom.findall(query):
                if rtp.get('group') == node_name:
                    key = DomExtractor._get_key_from_runtimeparameter(rtp)
                    node[key] = rtp.text
            nodes[node_name] = node

        return nodes

    @staticmethod
    def _get_node_names(run_dom):
        """Return list of node names in the run.
        """
        node_names = []
        for group in run_dom.attrib['groups'].split(','):
            node_name = ""
            try:
                node_name = group.split(NodeDecorator.NODE_PROPERTY_SEPARATOR)[1]
            except IndexError:
                pass
            else:
                node_names.append(node_name.strip())
        return node_names

    @staticmethod
    def _get_key_from_runtimeparameter(rtp):
        return rtp.attrib['key'].split(NodeDecorator.NODE_PROPERTY_SEPARATOR, 1)[-1]

    @staticmethod
    def extract_node_image_attributes(run_dom, nodename):
        """ Return image attributes of all nodes.
        """
        image = DomExtractor.extract_node_image(run_dom, nodename)
        attributes = {}

        if image is not None:
            attributes = DomExtractor.get_attributes(image)

        return attributes

    @staticmethod
    def extract_node_image(run_dom, nodename):
        """ Return image attributes of all nodes.
        """
        image = None

        if DomExtractor.get_module_category(run_dom) == NodeDecorator.IMAGE:
            image = run_dom.find('module')
        else:
            for node in run_dom.findall(DomExtractor.PATH_TO_NODE_ON_RUN):
                if node.get('name') == nodename:
                    image = node.find('image')

        return image

    @staticmethod
    def extract_deployment(run_dom, nodename):
        """ Return the deployment module of a run.
        """
        return run_dom.find('module')

    @staticmethod
    def extract_node_image_targets(run_dom, node_name):

        if NodeDecorator.is_orchestrator_name(node_name):
            module_dom = DomExtractor.extract_deployment(run_dom, node_name)
        else:
            module_dom = DomExtractor.extract_node_image(run_dom, node_name)

        return DomExtractor.get_targets_from_module(module_dom)

    @staticmethod
    def extract_node_image_build_state(run_dom, node_name):

        if NodeDecorator.is_orchestrator_name(node_name):
            return {}

        image_dom = DomExtractor.extract_node_image(run_dom, node_name)
        return DomExtractor.get_build_state_from_image(image_dom)

    @staticmethod
    def get_build_state_from_image(image_dom):
        build_state = {}

        for st in image_dom.findall('buildStates/buildState'):
            module_uri = st.get('moduleUri')
            built_on = st.get('builtOn', '').split(',')
            build_state[module_uri] = dict(module_uri=module_uri, built_on=built_on)

        return build_state

    @staticmethod
    def get_module_category(run_dom):
        module = run_dom.find('module')
        return module.get('category', None) if module is not None else None

    @staticmethod
    def get_extra_disks_from_image(image_dom):
        extra_disks = {}

        for entry in image_dom.findall('parameters/entry'):
            param_name = entry.find('parameter').get('name')
            if param_name.startswith(DomExtractor.EXTRADISK_PREFIX):
                try:
                    extra_disks[param_name] = entry.find('parameter/value').text or ''
                except AttributeError:
                    pass

        return extra_disks

    @staticmethod
    def get_element_value_from_element_tree(element_tree, element_name):
        element = element_tree.find(element_name)
        value = getattr(element, 'text', '')
        if value is None:
            value = ''
        return value

    @staticmethod
    def get_attributes(dom):
        return dom.attrib

    @staticmethod
    def get_packages(module_dom):
        packages = []

        for package in module_dom.findall('packagesExpanded/packageExpanded'):
            name = package.get('name')
            if name:
                packages.append(name)

        return packages

    @staticmethod
    def extractCategoryFromRun(run_dom):
        return run_dom.attrib['category']

    @staticmethod
    def extractTypeFromRun(run_dom):
        return run_dom.attrib['type']

    @staticmethod
    def extract_mutable_from_run(run_dom):
        return run_dom.attrib[util.RUN_PARAM_MUTABLE]

    @staticmethod
    def extractDefaultCloudServiceNameFromRun(run_dom):
        return run_dom.attrib['cloudServiceName']

    @staticmethod
    def extract_run_parameters_from_run(run_dom):
        parameters = {}
        for node in run_dom.findall(DomExtractor.PATH_TO_PARAMETER):
            value = node.find('value')
            parameters[node.get('name')] = value.text if value is not None else None
        return parameters

    @staticmethod
    def get_targets_from_module(module_dom):
        """Return deployment targets of the given image.
        """
        targets = {}
        for st in module_dom.findall('targetsExpanded/targetExpanded/subTarget'):
            name = st.get('name')
            subtarget = dict(name=name,
                             order=int(st.get('order')),
                             module_uri=st.get('moduleUri'),
                             module=st.get('moduleShortName'),
                             script=st.text)

            targets.setdefault(name, [])
            targets[name].append(subtarget)

        for target in targets.itervalues():
            target.sort(key=lambda t: t.get('order'))

        if module_dom.tag == "imageModule" or module_dom.tag == "image" \
                or module_dom.get('category') == NodeDecorator.IMAGE:
            targets[NodeDecorator.NODE_PACKAGES] = DomExtractor.get_packages(module_dom)

        return targets

    @staticmethod
    def server_config_dom_into_dict(config_dom, categories=[], value_updater=None):
        """
        :param config_dom: Element Tree representation of the server's configuration.
        :param categories: categories to extract; if empty, extracts all categories.
        :return: dictionary {'category': [('param', 'value'),],}
        """
        config = defaultdict(list)
        for param in config_dom.findall('parameters/entry'):
            category = param.find('parameter').get('category')
            if categories and (category not in categories):
                continue
            name = param.find('parameter').get('name')
            value = param.find('parameter/value').text
            if value is None:
                value = ''
            if '\n' in value:
                value = value.replace('\n', '')
            if hasattr(value_updater, '__call__'):
                value = value_updater(value)
            config[category].append((name, value))
        return config
