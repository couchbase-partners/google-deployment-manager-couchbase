def GenerateConfig(context):
    license = 'hourly-pricing'

    couchbaseUsername='couchbase'
    couchbasePassword = {
        'name': 'generated-password',
        'type': 'password.py',
        'properties': {
            'length': 8,
            'includeSymbols': True
        }
    }

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

    outputs = {
        'couchbaseUsername': couchbaseUsername,
        'couchbasePassword': couchbasePassword
    }

    config={}
    config['resources'] = []
    config['resources'].append(deployment)
    config['outputs'].append(outputs)
    )
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
