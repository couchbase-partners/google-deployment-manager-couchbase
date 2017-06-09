def GenerateConfig(context):
    config={}
    config['resources'] = []

    for cluster in context.properties['clusters']:
        clusterJSON = {
            'name': context.env['deployment'] + '-' + cluster['cluster'],
            'type': 'cluster.py',
            'properties': {
                'couchbaseUsername': context.properties['couchbaseUsername'],
                'couchbasePassword': context.properties['couchbasePassword'],
                'cluster': cluster['cluster'],
                'region': cluster['region'],
                'groups': cluster['groups'],
            }
        }
        config['resources'].append(clusterJSON)

    serviceAccount = {
        'name': context.env['deployment'] + '-sa',
        'type': 'iam.v1.serviceAccount',
        'properties': {
            'accountId': context.env['deployment'] + '-sa',
            'displayName': context.env['deployment'] + '-sa'
        }
    }
    config['resources'].append(serviceAccount)

    return config
