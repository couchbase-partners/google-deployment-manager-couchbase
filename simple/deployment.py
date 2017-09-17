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
                'license': context.properties['license'],
                'cluster': cluster['cluster'],
                'region': cluster['region'],
                'groups': cluster['groups'],
            }
        }
        config['resources'].append(clusterJSON)

    firewall = {
        'name': context.env['deployment'] + '-firewall',
        'type': 'compute.v1.firewall',
        'properties': {
            'sourceRanges': ['0.0.0.0/0'],
            'allowed': [{
                'IPProtocol': 'tcp',
                'ports': ['8091', '4984', '4985']
            }]
        }
    }
    config['resources'].append(firewall)

    return config
