
def GenerateConfig(context):
    config={}
    config['resources'] = []

    runtimeconfigName = context.env['deployment'] + '-' + context.properties['cluster'] + '-runtimeconfig'
    runtimeconfig = {
        'name': runtimeconfigName,
        'type': 'runtimeconfig.v1beta1.config',
        'properties': {
            'config': runtimeconfigName
        }
    }
    config['resources'].append(runtimeconfig)

    nodeCount = {
        'name': context.env['deployment'] + '-' + context.properties['cluster'] + '-nodeCount',
        'type': 'runtimeconfig.v1beta1.variable',
        'properties': {
            'parent': '$(ref.' + runtimeconfigName + '.name)',
            'variable': 'nodeCount',
            'text': str(getNodeCount(context))
        }
    }
    config['resources'].append(nodeCount)

    for group in context.properties['groups']:
        groupJSON = {
            'name': context.env['deployment'] + '-' + context.properties['cluster'] + '-' + group['group'],
            'type': 'group.py',
            'properties': {
                'couchbaseUsername': context.properties['couchbaseUsername'],
                'couchbasePassword': context.properties['couchbasePassword'],
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

def getNodeCount(context):
    nodeCount = 0
    for group in context.properties['groups']:
        services = group['services']
        if 'data' in services or 'query' in services or 'index' in services or 'fts' in services:
            nodeCount += group['nodeCount']
    return nodeCount
