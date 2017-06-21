URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
    config={}
    config['resources'] = []

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
                        'sourceImage': URL_BASE + 'ubuntu-os-cloud/global/images/ubuntu-1404-trusty-v20170424'
                    },
                    'diskType': 'pd-ssd',
                    'diskSizeGb': context.properties['diskSize']
                }],
                'metadata': {'items': [{'key':'startup-script', 'value':GenerateStartupScript(context)}]},
                'serviceAccounts': [{
                    'name': context.env['deployment'] + '-sa',
                    'scopes': ['https://www.googleapis.com/auth/cloud-platform']
                }]
            }
        }
    }
    config['resources'].append(instanceTemplate)

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
    config['resources'].append(instanceGroupManager)

    return config

def GenerateStartupScript(context):
    script = '#!/usr/bin/env bash\n\n'
    script += 'couchbaseUsername="' + context.properties['couchbaseUsername'] + '"\n'
    script += 'couchbasePassword="' + context.properties['couchbasePassword'] + '"\n'
    script += 'DEPLOYMENT="' + context.env['deployment'] + '"\n'
    script += 'CLUSTER="' + context.properties['cluster'] + '"\n'

    services=context.properties['services']
    servicesParameter=''
    for service in services:
        servicesParameter += service + ','
    servicesParameter=servicesParameter[:-1]
    script += 'services="' + servicesParameter + '"\n\n'

    if 'data' in services or 'query' in services or 'index' in services or 'fts' in services:
        script+= context.imports['scripts/installServer.sh']
        script+= context.imports['scripts/configureServer.sh']
    if 'syncGateway' in services:
        script+=context.imports['scripts/installSyncGateway.sh']
        script+= context.imports['scripts/configureSyncGateway.sh']

    return script
