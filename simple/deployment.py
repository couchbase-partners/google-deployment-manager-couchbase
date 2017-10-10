def GenerateConfig(context):
    config={}
    config['resources'] = []

    runtimeconfigName = '-'.join(context.env['deployment'].split("-")[-2:])[-20:] + '-runtimeconfig'
    runtimeconfig = {
        'name': runtimeconfigName,
        'type': 'runtimeconfig.v1beta1.config',
        'properties': {
            'config': runtimeconfigName
        }
    }
    config['resources'].append(runtimeconfig)

    for cluster in context.properties['clusters']:
        clusterJSON = {
            'name': '-'.join(context.env['deployment'].split("-")[-2:])[-20:] + '-' + cluster['cluster'],
            'type': 'cluster.py',
            'properties': {
                'serverVersion': context.properties['serverVersion'],
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
        'name': '-'.join(context.env['deployment'].split("-")[-2:])[-20:] + '-firewall',
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
