URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
  items = []
  for key, value in context.properties['metadata-from-file'].iteritems():
    items.append({
      'key': key,
      'value': context.imports[value]
    })
  metadata = {'items': items}

  deployment = context.env['deployment']
  machineType = context.properties['machineType']
  instance_template = deployment + '-it'
  igm = deployment + '-igm'
  region = context.properties['region']

  resources = [
      {
          'name': instance_template,
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
                      'diskSizeGb': '100'
                  }],
                  'metadata': metadata,
              }
          }
      },
      {
          'name': igm,
          'type': 'compute.v1.regionInstanceGroupManager',
          'properties': {
              'region': region,
              'baseInstanceName': deployment + '-instance',
              'instanceTemplate': '$(ref.' + instance_template + '.selfLink)',
              'targetSize': 4,
              'autoHealingPolicies': [{
                  'initialDelaySec': 60
              }]
          }
      }
  ]

  return {'resources': resources}
