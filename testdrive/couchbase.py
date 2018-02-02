import naming
import random

def GenerateConfig(context):
    config={}
    config['resources'] = []

    couchbaseUsername='couchbase'
    couchbasePassword = GeneratePassword()

    clusterName = 'td'
    serverGroupName = 'server'
    syncGatewayGroupName = 'syncgateway'

    cluster = GetCluster(context, clusterName, serverGroupName, syncGatewayGroupName)

    deployment = {
        'name': 'deployment',
        'type': 'deployment.py',
        'properties': {
            'serverVersion': context.properties['serverVersion'],
            'syncGatewayVersion': context.properties['syncGatewayVersion'],
            'couchbaseUsername': couchbaseUsername,
            'couchbasePassword': couchbasePassword,
            'license': 'byol',
            'clusters': [cluster]
        }
    }
    config['resources'].append(deployment)

    serverAdminUrl = 'http://$(ref.deployment.' \
        + naming.ExternalIpOutputName(clusterName, serverGroupName) \
        + '):8091/'

    syncGatewayAdminUrl = 'http://$(ref.deployment.' \
        + naming.ExternalIpOutputName(clusterName, syncGatewayGroupName) \
        + '):4985/_admin/'

    config['outputs'] = [
        { 'name': 'couchbaseUsername', 'value': couchbaseUsername },
        { 'name': 'couchbasePassword', 'value': couchbasePassword },
        { 'name': 'serverAdminUrl', 'value': serverAdminUrl },
        { 'name': 'syncGatewayAdminUrl', 'value': syncGatewayAdminUrl }
    ]

    return config

def GetCluster(context, clusterName, serverGroupName, syncGatewayGroupName):
    cluster = {
        'cluster': clusterName,
        'region': GetRandomRegion(),
        'groups':
            [
                {
                    'group': serverGroupName,
                    'diskSize': context.properties['serverDiskSize'],
                    'nodeCount': context.properties['serverNodeCount'],
                    'nodeType': context.properties['serverNodeType'],
                    'services': ['data','query','index','fts']
                },
                {
                    'group': syncGatewayGroupName,
                    'diskSize': context.properties['syncGatewayDiskSize'],
                    'nodeCount': context.properties['syncGatewayNodeCount'],
                    'nodeType': context.properties['syncGatewayNodeType'],
                    'services': ['syncGateway']
                }
            ]
    }
    return cluster

def GetRandomRegion():
    availableRegions = [
        'us-central1',
        'us-west1',
        'us-east1',
        'us-east4'
    ]
    return random.choice(availableRegions)

def GeneratePassword():
    categories = ['ABCDEFGHJKLMNPQRSTUVWXYZ', 'abcdefghijkmnopqrstuvwxyz', '123456789', '*-+.']
    password=[]
    for category in categories:
        password.insert(random.randint(0, len(password)), random.choice(category))
    while len(password) < 8:
        password.insert(random.randint(0, len(password)), random.choice(''.join(categories)))
    return ''.join(password)
