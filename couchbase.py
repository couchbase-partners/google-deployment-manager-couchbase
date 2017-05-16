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
      groupName = group['group']
      diskSize = group['diskSize']
      machineCount = group['machineCount']
      machineType = group['machineType']
      services = group['services']

      groupJSON=GenerateGroup(groupName, deployment, region, diskSize, machineCount, machineType)
      config['resources'].append(groupJSON)

  return config

def GenerateGroup(groupName, deployment, region, diskSize, machineCount, machineType):
  groupJSON = {
    'name': deployment + '-' + region + '-' + groupName,
    'type': 'group.py',
    'properties': {
      'groupName': groupName,
      'region': region,
      'diskSize': diskSize,
      'machineCount': machineCount,
      'machineType': machineType,
    }
  }
  return groupJSON
