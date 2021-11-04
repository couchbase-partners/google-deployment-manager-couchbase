import naming


def GenerateConfig(context):
    config = {}
    config['resources'] = []
    config['outputs'] = []

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
        clusterName = cluster['cluster']
        clusterResourceName = naming.ClusterName(context, clusterName)

        clusterJSON = {
            'name': clusterResourceName,
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

        for group in cluster['groups']:
            groupName = group['group']
            outputName = naming.ExternalIpOutputName(clusterName, groupName)

            readActionName = naming.ExternalIpVariableReadActionName(context, clusterName, groupName)

            config['outputs'].append({
                'name': outputName,
                'value': '$(ref.%s.text)' % readActionName
            })

    firewall = {
        'name': naming.FirewallName(context),
        'type': 'compute.v1.firewall',
        'properties': {
            'sourceRanges': ['0.0.0.0/0'],
            'allowed': [{
                'IPProtocol': 'tcp',
                'ports': ['8091', '8092', '8093', '8094', '8095', '8096', '18091', '18092', '18093', '18094', '18095', '18096', '4984', '4985', '11210', '9130']
            }]
        }
    }
    config['resources'].append(firewall)

    return config
