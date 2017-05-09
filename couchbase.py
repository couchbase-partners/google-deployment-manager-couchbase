def GenerateConfig(context):
  config={}
  config['resources'] = []
  config['outputs'] = []

  deployment = context.env['deployment']
  couchbaseUsername=context.properties['couchbaseUsername']
  couchbasePassword=context.properties['couchbasePassword']

  for cluster in context.properties['clusters']:
    region = cluster['region']
    for group in cluster['groups']:
      diskSize = group['diskSize']
      machineCount = group['machineCount']
      machineType = group['machineType']
      services = group['services']

      groupJSON=GenerateGroup(deployment, region, diskSize, machineCount, machineType)
      config['resources'].append(groupJSON)

  return config

def GenerateGroup(deployment, region, diskSize, machineCount, machineType):
  groupJSON = {
    'name': deployment + '-' + region + '-group',
    'type': 'group.py',
    'properties': {
      'region': region,
      'diskSize': diskSize,
      'machineCount': machineCount,
      'machineType': machineType,
    }
  }
  return groupJSON
