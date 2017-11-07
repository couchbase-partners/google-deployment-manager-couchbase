import naming

URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'
WAITER_TIMEOUT = '300s'

def GenerateConfig(context):
    license=context.properties['license']
    if 'syncGateway' in context.properties['services']:
        sourceImage = URL_BASE + 'couchbase-public/global/images/couchbase-sync-gateway-ee-' + license + '-v20171101'
    else:
        sourceImage = URL_BASE + 'couchbase-public/global/images/couchbase-server-ee-' + license + '-v20171101'

    runtimeconfigName = context.properties['runtimeconfigName']
    clusterName = context.properties['cluster']
    groupName = context.properties['group']

    instanceGroupTargetSize = context.properties['nodeCount']
    waiterSuccessPath = 'status/clusters/%s/groups/%s/success' % (clusterName, groupName)
    waiterFailurePath = 'status/clusters/%s/groups/%s/failure' % (clusterName, groupName)

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
                        'sourceImage': sourceImage
                    },
                    'diskType': 'pd-ssd',
                    'diskSizeGb': context.properties['diskSize']
                }],
                'metadata': {
                    'items': [
                        { 'key': 'startup-script', 'value': GenerateStartupScript(context) },
                        { 'key': 'runtime-config-name', 'value': runtimeconfigName },
                        { 'key': 'status-success-base-path', 'value': waiterSuccessPath },
                        { 'key': 'status-failure-base-path', 'value': waiterFailurePath },
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

    instanceGroupManagerName = naming.InstanceGroupManagerName(context, clusterName, groupName)
    instanceGroupManager = {
        'name': instanceGroupManagerName,
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'region': context.properties['region'],
            'baseInstanceName': naming.InstanceGroupInstanceBaseName(context, clusterName, groupName),
            'instanceTemplate': '$(ref.' + instanceTemplateName + '.selfLink)',
            'targetSize': instanceGroupTargetSize,
            'autoHealingPolicies': [{
                'initialDelaySec': 60
            }]
        }
    }

    groupWaiterName = naming.WaiterName(context, clusterName, groupName)
    groupWaiter = {
        'name': groupWaiterName,
        'type': 'runtimeconfig.v1beta1.waiter',
        'metadata': {
            'dependsOn': [instanceGroupManagerName],
        },
        'properties': {
            'parent': '$(ref.%s.name)' % runtimeconfigName,
            'waiter': 'software',
            'timeout': WAITER_TIMEOUT,
            'success': {
                'cardinality': {
                    'number': instanceGroupTargetSize,
                    'path': waiterSuccessPath,
                },
            },
            'failure': {
                'cardinality': {
                    'number': 1,
                    'path': waiterFailurePath,
                },
            },
        },
    }

    config={}
    config['resources'] = []
    config['resources'].append(instanceTemplate)
    config['resources'].append(instanceGroupManager)
    config['resources'].append(groupWaiter)
    return config

def GenerateStartupScript(context):
    script = '#!/usr/bin/env bash\n\n'
    script += context.imports['startupCommon.sh']

    services=context.properties['services']
    if 'data' in services or 'query' in services or 'index' in services or 'fts' in services:
        script += 'CLUSTER="' + context.properties['cluster'] + '"\n'
        script += 'serverVersion="' + context.properties['serverVersion'] + '"\n'
        script += 'couchbaseUsername="' + context.properties['couchbaseUsername'] + '"\n'
        script += 'couchbasePassword="' + context.properties['couchbasePassword'] + '"\n'

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
