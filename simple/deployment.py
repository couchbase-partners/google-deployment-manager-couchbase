import naming

def GenerateConfig(context):
    config={}
    config['resources'] = []

    runtimeconfigName = naming.RuntimeConfigName(context)
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
            'name': naming.ClusterName(context, cluster['cluster']),
            'type': 'cluster.py',
            'properties': {
                'runtimeconfigName': runtimeconfigName,
                'serverVersion': context.properties['serverVersion'],
                'syncGatewayVersion': context.properties['syncGatewayVersion'],
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
        'name': naming.FirewallName(context),
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
