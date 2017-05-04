URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
  items = []
  for key, value in context.properties['metadata-from-file'].iteritems():
    items.append({'key': key, 'value': context.imports[value]})
  metadata = {'items': items}

  deployment = context.env['deployment']
  region = context.properties['region']
  machineCount = context.properties['machineCount']
  machineType = context.properties['machineType']
  diskSize = context.properties['diskSize']

  it_name = deployment + '-' + region + '-it'
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
    'name': deployment + '-' + region + '-igm',
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
