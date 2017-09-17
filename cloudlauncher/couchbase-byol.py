def GenerateConfig(context):
    clusters=GetClusters(context)

    deployment = {
        'name': 'deployment',
        'type': 'deployment.py',
        'properties': {
            'couchbaseUsername': context.properties['couchbaseUsername'],
            'couchbasePassword': context.properties['couchbasePassword'],
            'license': 'byol',
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
    availableRegions = [
        'us-central1',
        'us-west1',
        'us-east1',
        'us-east4',
        'europe-west1',
        'europe-west2',
        'europe-west3',
        'asia-southeast1',
        'asia-east1',
        'asia-northeast1',
        'australia-southeast1'
    ]
    for region in availableRegions:
        if context.properties[region]:
            regions.append(region)
    return regions
