URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
    license=context.properties['license']
    if 'syncGateway' in context.properties['services']:
        sourceImage = URL_BASE + 'couchbase-public/global/images/couchbase-sync-gateway-ee-' + license
    else:
        sourceImage = URL_BASE + 'couchbase-public/global/images/couchbase-server-ee-' + license

    instanceTemplateName = context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-it'
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
                'metadata': {'items': [{'key':'startup-script', 'value':GenerateStartupScript(context)}]},
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

    instanceGroupManager = {
        'name': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-igm',
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'region': context.properties['region'],
            'baseInstanceName': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-instance',
            'instanceTemplate': '$(ref.' + instanceTemplateName + '.selfLink)',
            'targetSize': context.properties['nodeCount'],
            'autoHealingPolicies': [{
                'initialDelaySec': 60
            }]
        }
    }

    config={}
    config['resources'] = []
    config['resources'].append(instanceTemplate)
    config['resources'].append(instanceGroupManager)
    return config

def GenerateStartupScript(context):
    script = '#!/usr/bin/env bash\n\n'
    script += 'DEPLOYMENT="' + context.env['deployment'] + '"\n'
    script += 'CLUSTER="' + context.properties['cluster'] + '"\n'

    services=context.properties['services']
    if 'data' in services or 'query' in services or 'index' in services or 'fts' in services:
        script += 'couchbaseUsername="' + context.properties['couchbaseUsername'] + '"\n'
        script += 'couchbasePassword="' + context.properties['couchbasePassword'] + '"\n'

        servicesParameter=''
        for service in services:
            servicesParameter += service + ','
        servicesParameter=servicesParameter[:-1]

        script += 'services="' + servicesParameter + '"\n\n'
        script+= context.imports['server.sh']

    if 'syncGateway' in services:
        script+=context.imports['syncGateway.sh']

    return script
