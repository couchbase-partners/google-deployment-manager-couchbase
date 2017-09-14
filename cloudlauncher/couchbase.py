def GenerateConfig(context):
    clusters=GetClusters(context)

    deployment = {
        'name': 'deployment',
        'type': 'deployment.py',
        'properties': {
            'couchbaseUsername': context.properties['couchbaseUsername'],
            'couchbasePassword': context.properties['couchbasePassword'],
            'clusters': clusters
        }
    }

    config={}
    config['resources'] = []
    config['resources'].append(deployment)
    return config

def GetClusters(context):
    clusters = []
    regions = GetRegionsList(context)
    for region in regions:
        cluster = {
            'cluster': region,
            'region': region,
            'groups':
            [
                {
                    'group': 'server',
                    'diskSize': context.properties['serverDiskSize'],
                    'nodeCount': context.properties['serverNodeCount'],
                    'nodeType': context.properties['serverNodeType'],
                    'services': ['data','query','index','fts']
                },
                {
                    'group': 'syncgateway',
                    'diskSize': context.properties['syncgatewayDiskSize'],
                    'nodeCount': context.properties['syncgatewayNodeCount'],
                    'nodeType': context.properties['syncgatewayNodeType'],
                    'services': ['syncGateway']
                }
            ]
        }
        clusters.append(cluster)
    return clusters

def GetRegionsList(context):
    regions = []
    if context.properties['us-central1']:
        regions.append('us-central1')
    if context.properties['us-west1']:
        regions.append('us-west1')
    if context.properties['us-east1']:
        regions.append('us-east1')
    if context.properties['us-east4']:
        regions.append('us-east4')
    if context.properties['europe-west1']:
        regions.append('europe-west1')
    if context.properties['europe-west2']:
        regions.append('europe-west2')
    if context.properties['europe-west3']:
        regions.append('europe-west3')
    if context.properties['asia-southeast1']:
        regions.append('asia-southeast1')
    if context.properties['asia-east1']:
        regions.append('asia-east1')
    if context.properties['asia-northeast1']:
        regions.append('asia-northeast1')
    if context.properties['australia-southeast1']:
        regions.append('australia-southeast1')
    return regions
