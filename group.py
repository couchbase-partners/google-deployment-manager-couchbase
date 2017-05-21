def GenerateConfig(context):
    URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

    items = []
    items.append({'key':'startup-script', 'value':GenerateStartupScript(context)})
    metadata = {'items': items}

    it_name = context.env['deployment'] + '-' + context.properties['clusterName'] + '-' + context.properties['groupName'] + '-it'
    it = {
        'name': it_name,
        'type': 'compute.v1.instanceTemplate',
        'properties': {
            'properties': {
                'machineType': context.properties['machineType'],
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
                'metadata': metadata,
            }
        }
    }

    igm = {
        'name': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-igm',
        'type': 'compute.v1.regionInstanceGroupManager',
        'properties': {
            'region': context.properties['region'],
            'baseInstanceName': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + context.properties['group'] + '-instance',
            'instanceTemplate': '$(ref.' + it_name + '.selfLink)',
            'targetSize': context.properties['machineCount'],
            'autoHealingPolicies': [{
                'initialDelaySec': 60
            }]
        }
    }

    resources = []
    resources.append(it)
    resources.append(igm)
    return {'resources': resources}

def GenerateStartupScript(context):
    script = '''
    #!/usr/bin/env bash
    '''

    services=context.properties['services']
    if 'syncGateway' in services or 'accelerator' in services:
        script+=context.imports['installMobile.sh']
    else:
        script+= context.imports['installServer.sh']
    return script
