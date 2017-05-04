def GenerateConfig(context):
  config={}
  config['resources'] = []
  config['outputs'] = []

  couchbaseUsername=context.properties['couchbaseUsername']
  couchbasePassword=context.properties['couchbasePassword']

  for cluster in context.properties['clusters']:
    region = cluster['region']
    for group in cluster['groups']:
      diskSize = group['diskSize']
      machineCount = group['machineCount']
      machineType = group['machineType']
      services = group['services']

      igm = {
        'name': region + '-igm',
        'type': 'regional_igm.py',
        'properties': {
          'region': region,
          'diskSize': diskSize,
          'machineCount': machineCount,
          'machineType': machineType,
          'metadata-from-file': {
            'startup-script': 'startup-script.sh'
          }
        }
      }
      config['resources'].append(igm)

  return config
