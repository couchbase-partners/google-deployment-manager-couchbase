def GenerateConfig(context):
    config={}
    config['resources'] = []
    config['outputs'] = []

    for cluster in context.properties['clusters']:
        for group in cluster['groups']:
            groupJSON = {
                'name': context.env['deployment'] + '-' + cluster['cluster'] + '-' + group['group'],
                'type': 'group.py',
                'properties': {
                    'couchbaseUsername': context.properties['couchbaseUsername'],
                    'couchbasePassword': context.properties['couchbasePassword'],
                    'clusterName': cluster['cluster'],
                    'region': cluster['region'],
                    'groupName': group['group'],
                    'diskSize': group['diskSize'],
                    'machineCount': group['machineCount'],
                    'machineType': group['machineType'],
                    'services': group['services']
                }
            }
            config['resources'].append(groupJSON)
    return config
