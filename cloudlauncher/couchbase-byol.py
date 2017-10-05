def GenerateConfig(context):
    license = 'byol'

    couchbaseUsername='couchbase'
    couchbasePassword = GeneratePassword()

    deployment = {
        'name': 'deployment',
        'type': 'deployment.py',
        'properties': {
            'serverVersion': context.properties['serverVersion'],
            'couchbaseUsername': couchbaseUsername,
            'couchbasePassword': couchbasePassword,
            'license': license,
            'clusters': GetClusters(context)
        }
    }

    outputs = [
        {
            'name': 'couchbaseUsername',
            'value': couchbaseUsername
        },
        {
            'name': 'couchbasePassword',
            'value': couchbasePassword
        }
    ]

    config={}
    config['resources'] = []
    config['resources'].append(deployment)
    config['outputs']=outputs
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

def GeneratePassword():
    import random
    categories = ['ABCDEFGHJKLMNPQRSTUVWXYZ', 'abcdefghijkmnopqrstuvwxyz', '123456789', '*-+.']
    password=[]
    for category in categories:
        password.insert(random.randint(0, len(password)), random.choice(category))
    while len(password) < 8:
        password.insert(random.randint(0, len(password)), random.choice(''.join(categories)))
    return ''.join(password)
