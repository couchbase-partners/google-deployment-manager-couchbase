import naming

def GenerateConfig(context):
    config={}
    config['resources'] = []
    config['outputs'] = []

    clusterName = context.properties['cluster']

    for group in context.properties['groups']:
        groupName = group['group']

        groupProperties = {
            'runtimeconfigName': context.properties['runtimeconfigName'],
            'serverVersion': context.properties['serverVersion'],
            'syncGatewayVersion': context.properties['syncGatewayVersion'],
            'couchbaseUsername': context.properties['couchbaseUsername'],
            'couchbasePassword': context.properties['couchbasePassword'],
            'license': context.properties['license'],
            'cluster': context.properties['cluster'],
            'region': context.properties['region'],
        }
        for key in group:
            groupProperties[key] = group[key]

        groupJSON = {
            'name': naming.GroupName(context, clusterName, groupName),
            'type': 'group.py',
            'properties': groupProperties
        }
        config['resources'].append(groupJSON)
        config['outputs'].append({
            'name': naming.ExternalIpOutputName(clusterName, groupName),
            'value': '$(ref.%s.externalIp)' % naming.GroupName(context, clusterName, groupName)
        })
    return config
