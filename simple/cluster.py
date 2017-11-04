import naming

def GenerateConfig(context):
    config={}
    config['resources'] = []

    for group in context.properties['groups']:
        groupJSON = {
            'name': naming.GroupName(context, context.properties['cluster'], group['group']),
            'type': 'group.py',
            'properties': {
                'runtimeconfigName': context.properties['runtimeconfigName'],
                'serverVersion': context.properties['serverVersion'],
                'syncGatewayVersion': context.properties['syncGatewayVersion'],
                'couchbaseUsername': context.properties['couchbaseUsername'],
                'couchbasePassword': context.properties['couchbasePassword'],
                'license': context.properties['license'],
                'cluster': context.properties['cluster'],
                'region': context.properties['region'],
                'group': group['group'],
                'diskSize': group['diskSize'],
                'nodeCount': group['nodeCount'],
                'nodeType': group['nodeType'],
                'services': group['services']
            }
        }
        config['resources'].append(groupJSON)
    return config
