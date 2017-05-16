URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
  deployment = context.env['deployment']
  groupName = context.properties['groupName']
  region = context.properties['region']
  machineCount = context.properties['machineCount']
  machineType = context.properties['machineType']
  diskSize = context.properties['diskSize']

  items = []
  items.append({'key':'startup-script', 'value':context.imports['startup-script.sh']})
  metadata = {'items': items}

  it_name = deployment + '-' + region + '-' + groupName + '-it'
  it = {
    'name': it_name,
    'type': 'compute.v1.instanceTemplate',
    'properties': {
      'properties': {
        'machineType': machineType,
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
          'diskSizeGb': diskSize
        }],
        'metadata': metadata,
      }
    }
  }

  igm = {
    'name': deployment + '-' + region + '-' + groupName + '-igm',
    'type': 'compute.v1.regionInstanceGroupManager',
    'properties': {
      'region': region,
      'baseInstanceName': deployment + '-instance',
      'instanceTemplate': '$(ref.' + it_name + '.selfLink)',
      'targetSize': machineCount,
      'autoHealingPolicies': [{
        'initialDelaySec': 60
      }]
    }
  }

  resources = []
  resources.append(it)
  resources.append(igm)
  return {'resources': resources}
