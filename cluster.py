
def GenerateConfig(context):
    config={}
    config['resources'] = []

    runtimeconfigName = context.env['deployment'] + '-' + cluster['cluster'] + '-runtimeconfig'
    runtimeconfig = {
        'name': runtimeconfigName,
        'type': runtimeconfig.v1beta1.config,
        'properties': {
            'config': runtimeconfigName
        }
    }
    config['resources'].append(runtimeconfig)

    nodeCount = {
        'name': 'nodeCount'
        'type': runtimeconfig.v1beta1.variable
        'properties': {
            'parent': '$(ref.' + runtimeconfigName + '.name)'
            'variable': 'nodeCount'
            'text': getNodeCount(context)
        }
    }
    config['resources'].append(nodeCount)

    nodeNames = {
        'name': 'nodeNames'
        'type': runtimeconfig.v1beta1.variable
        'properties': {
            'parent': '$(ref.' + runtimeconfigName + '.name)'
            'variable': 'nodeNames'
            'value': None
        }
    }
    config['resources'].append(nodeNames)

    for group in context.properties['groups']:
        groupJSON = {
            'name': context.env['deployment'] + '-' + cluster['cluster'] + '-' + group['group'],
            'type': 'group.py',
            'properties': {
                'couchbaseUsername': context.properties['couchbaseUsername'],
                'couchbasePassword': context.properties['couchbasePassword'],
                'cluster': context.properties['cluster'],
                'region': context.properties['region'],
                'group': group['group'],
                'diskSize': group['diskSize'],
                'machineCount': group['machineCount'],
                'machineType': group['machineType'],
                'services': group['services']
            }
        }
        config['resources'].append(groupJSON)
    return config

def getNodeCount(context):
    nodeCount = 0
    for group in context.properties['groups']:
        nodeCount += group['nodeCount']
    return nodeCount
