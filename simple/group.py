import naming

URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

WAITER_TIMEOUT = '900s'

def GenerateConfig(context):
    runtimeconfigName = context.properties['runtimeconfigName']
    instanceGroupTargetSize = context.properties['nodeCount']

    externalIpCreateAction = GenerateExternalIpCreateActionConfig(context, runtimeconfigName)
    externalIpCreateActionName = externalIpCreateAction['name']

    instanceTemplate = GenerateInstanceTemplateConfig(context, runtimeconfigName)
    instanceTemplateName = instanceTemplate['name']

    instanceGroupManager = GenerateInstanceGroupManagerConfig(context, instanceTemplateName, instanceGroupTargetSize, externalIpCreateActionName)
    instanceGroupManagerName = instanceGroupManager['name']

    groupWaiter = GenerateGroupWaiterConfig(context, runtimeconfigName, instanceGroupManagerName, instanceGroupTargetSize)
    groupWaiterName = groupWaiter['name']

    externalIpReadAction = GenerateExternalIpReadActionConfig(context, runtimeconfigName, externalIpCreateActionName, groupWaiterName)
    externalIpReadActionName = externalIpReadAction['name']

    config={}
    config['resources'] = [
        externalIpCreateAction,
        instanceTemplate,
        instanceGroupManager,
        groupWaiter,
        externalIpReadAction
    ]
    config['outputs'] = [
        {
            'name': 'externalIp',
            'value': '$(ref.%s.text)' % externalIpReadActionName
        }
    ]
    return config

def GenerateExternalIpCreateActionConfig(context, runtimeconfigName):
    clusterName = context.properties['cluster']
    groupName = context.properties['group']
    project = context.env['project']

    externalIpVariablePath = _ExternalIpVariablePath(clusterName, groupName)
    actionName = naming.ExternalIpVariableCreateActionName(context, clusterName, groupName)
    action = {
        'name': actionName,
        'action': 'gcp-types/runtimeconfig-v1beta1:runtimeconfig.projects.configs.variables.create',
        'properties': {
            'parent': 'projects/%s/configs/%s' % (project, runtimeconfigName),
            'name': 'projects/%s/configs/%s/variables/%s' % (project, runtimeconfigName, externalIpVariablePath),
            'text': '<new_unknown>'
        },
        'metadata': {
            'dependsOn': [runtimeconfigName]
        }
    }
    return action

def GenerateExternalIpReadActionConfig(context, runtimeconfigName, externalIpCreateActionName, groupWaiterName):
    clusterName = context.properties['cluster']
    groupName = context.properties['group']
    project = context.env['project']

    externalIpVariablePath = _ExternalIpVariablePath(clusterName, groupName)
    name = naming.ExternalIpVariableReadActionName(context, clusterName, groupName)
    action = {
        'name': name,
        'action': 'gcp-types/runtimeconfig-v1beta1:runtimeconfig.projects.configs.variables.watch',
        'properties': {
            'name': 'projects/%s/configs/%s/variables/%s' % (project, runtimeconfigName, externalIpVariablePath),
            'newerThan': '$(ref.%s.updateTime)' % externalIpCreateActionName
        },
        'metadata': {
            'dependsOn': [groupWaiterName]
        }
    }
    return action

def GenerateInstanceTemplateConfig(context, runtimeconfigName):
    license = context.properties['license']

    # As I dropped the schema files to fix the disk issue this broke.  Need to dig in more here to figure out what's going on.
    # useImageFamily = context.properties['useImageFamily']
    useImageFamily = False

    if 'syncGateway' in context.properties['services']:
        sourceImage = _SyncGatewayImageUrl(license, useImageFamily)
    else:
        sourceImage = _ServerImageUrl(license, useImageFamily)

    clusterName = context.properties['cluster']
    groupName = context.properties['group']

    instanceTemplateName = naming.InstanceTemplateName(context, clusterName, groupName)

    instanceTemplate = {
        'name': instanceTemplateName,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'properties': {
                'machineType': context.properties['nodeType'],
                'networkInterfaces': [{
                    'network': URL_BASE + context.env['project'] + '/global/networks/default',
                    'accessConfigs': [{
                        'name': 'External NAT',
                        'type': 'ONE_TO_ONE_NAT'
                    }]
                }],
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': sourceImage,
                        'diskType': 'pd-ssd',
                        'diskSizeGb': context.properties['diskSize']
                    }
                }],
                'metadata': {
                    'items': [
                        { 'key': 'startup-script', 'value': GenerateStartupScript(context) },
                        { 'key': 'runtime-config-name', 'value': runtimeconfigName },
                        { 'key': 'external-ip-variable-path', 'value': _ExternalIpVariablePath(clusterName, groupName) },
                        { 'key': 'status-success-base-path', 'value': _WaiterSuccessPath(clusterName, groupName) },
                        { 'key': 'status-failure-base-path', 'value': _WaiterFailurePath(clusterName, groupName) },
                    ]
                },
                'serviceAccounts': [{
                    'email': 'default',
                    'scopes': [
                        'https://www.googleapis.com/auth/cloud-platform',
                        'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                        'https://www.googleapis.com/auth/devstorage.read_only',
                        'https://www.googleapis.com/auth/logging.write',
                        'https://www.googleapis.com/auth/monitoring.write',
                        'https://www.googleapis.com/auth/cloudruntimeconfig'
                    ]
                }]
            }
        }
    }
    return instanceTemplate

def GenerateInstanceGroupManagerConfig(context, instanceTemplateName, instanceGroupTargetSize, externalIpCreateActionName):
    clusterName = context.properties['cluster']
    groupName = context.properties['group']

    instanceGroupManagerName = naming.InstanceGroupManagerName(context, clusterName, groupName)
    baseInstanceName = naming.InstanceGroupInstanceBaseName(context, clusterName, groupName)

    instanceGroupManager = {
        'name': instanceGroupManagerName,
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'region': context.properties['region'],
            'baseInstanceName': baseInstanceName,
            'instanceTemplate': '$(ref.' + instanceTemplateName + '.selfLink)',
            'targetSize': instanceGroupTargetSize
        },
        'metadata': {
            'dependsOn': [externalIpCreateActionName]
        }
    }
    return instanceGroupManager

def GenerateGroupWaiterConfig(context, runtimeconfigName, instanceGroupManagerName, instanceGroupTargetSize):
    clusterName = context.properties['cluster']
    groupName = context.properties['group']

    groupWaiterName = naming.WaiterName(context, clusterName, groupName)
    groupWaiter = {
        'name': groupWaiterName,
        'type': 'runtimeconfig.v1beta1.waiter',
        'metadata': {
            'dependsOn': [instanceGroupManagerName],
        },
        'properties': {
            'parent': '$(ref.%s.name)' % runtimeconfigName,
            'waiter': groupWaiterName,
            'timeout': WAITER_TIMEOUT,
            'success': {
                'cardinality': {
                    'number': instanceGroupTargetSize,
                    'path': _WaiterSuccessPath(clusterName, groupName),
                },
            },
            'failure': {
                'cardinality': {
                    'number': 1,
                    'path': _WaiterFailurePath(clusterName, groupName),
                },
            },
        },
    }
    return groupWaiter

def GenerateStartupScript(context):
    script = '#!/usr/bin/env bash\n\n'
    script += context.imports['startupCommon.sh']

    # GCP is now running the startup script on reboot.  This is a workaround.
    script += 'if [ -d "/opt/couchbase" ]; then\n'
    script += '  echo "Couchbase Server is already installed.  Exiting"\n'
    script += '  exit\n'
    script += 'elif [ -d "/home/sync_gateway" ]; then\n'
    script += '  echo "Sync Gateway is already installed.  Exiting."\n'
    script += '  exit\n'
    script += 'fi\n\n'

    services=context.properties['services']
    if 'data' in services or 'query' in services or 'index' in services or 'fts' in services or 'eventing' in services or 'analytics' in services:
        script += 'CLUSTER="' + context.properties['cluster'] + '"\n'
        script += 'serverVersion="' + context.properties['serverVersion'] + '"\n'
        script += 'couchbaseUsername="' + context.properties['couchbaseUsername'] + '"\n'
        script += 'couchbasePassword="' + context.properties['couchbasePassword'] + '"\n'
        script += 'nodeCount="' + str(context.properties['clusterNodesCount']) + '"\n'

        servicesParameter=''
        for service in services:
            servicesParameter += service + ','
        servicesParameter=servicesParameter[:-1]

        script += 'services="' + servicesParameter + '"\n\n'
        script+= context.imports['server.sh']

    if 'syncGateway' in services:
        script += 'syncGatewayVersion="' + context.properties['syncGatewayVersion'] + '"\n'
        script += context.imports['syncGateway.sh']

    script += context.imports['successNotification.sh']

    return script

def _SyncGatewayImageUrl(license, useFamily):
    if useFamily:
        return URL_BASE + 'couchbase-public/global/images/family/couchbase-sync-gateway-ee-' + license
    else:
        return URL_BASE + 'couchbase-public/global/images/couchbase-sync-gateway-ee-' + license + '-v20200923'

def _ServerImageUrl(license, useFamily):
    if (useFamily):
        return URL_BASE + 'couchbase-public/global/images/family/couchbase-server-ee-' + license
    else:
        return URL_BASE + 'couchbase-public/global/images/couchbase-server-ee-' + license + '-v20200923'

def _WaiterSuccessPath(clusterName, groupName):
    return 'status/clusters/%s/groups/%s/success' % (clusterName, groupName)

def _WaiterFailurePath(clusterName, groupName):
    return 'status/clusters/%s/groups/%s/failure' % (clusterName, groupName)

def _ExternalIpVariablePath(clusterName, groupName):
    return 'external-ip/clusters/%s/groups/%s' % (clusterName, groupName)
