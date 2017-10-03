def GenerateConfig(context):
    license = 'byol'

    couchbaseUsername='couchbase'
    couchbasePassword = GeneratePassword()

    deployment = {
        'name': 'deployment',
        'type': 'deployment.py',
        'properties': {
            'serverVersion': '4.6.3',
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
    config['resources'].append(couchbasePassword)
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
    # https://stackoverflow.com/questions/3854692/generate-password-in-python
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    from os import urandom
    return "".join(chars[ord(c) % len(chars)] for c in urandom(8))
