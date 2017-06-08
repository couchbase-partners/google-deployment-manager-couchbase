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
                        'sourceImage': URL_BASE + 'debian-cloud/global/images/debian-7-wheezy-v20151104'
                    },
                    'diskType': 'pd-ssd',
                    'diskSizeGb': context.properties['diskSize']
                }],
                'metadata': {'items': [{'key':'startup-script', 'value':GenerateStartupScript(context)}]},
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

    services=context.properties['services']
    servicesParameter=''
    for service in services:
        servicesParameter += service + ','
    servicesParameter=servicesParameter[:-1]
    script += 'services="' + servicesParameter + '"\n\n'

    # We need a beta of gcloud to use the runtime config to select a rally point
    script += 'echo "Installing gcloud beta..."\n'
    script += 'gcloud components update -q\n'
    script += 'gcloud components install beta -q\n\n'

    if 'syncGateway' in services or 'accelerator' in services:
        script+=context.imports['scripts/installMobile.sh']
#        script+= context.imports['scripts/configureMobile.sh']
    else:
        script+= context.imports['scripts/installServer.sh']
#        script+= context.imports['scripts/configureServer.sh']
    return script
