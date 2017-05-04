def GenerateConfig(context):
    config={}
    config['resources'] = []
    config['outputs'] = []

    couchbaseUsername=context.properties['couchbaseUsername']
    couchbasePassword=context.properties['couchbasePassword']

    for cluster in context.properties['clusters']:
        region = cluster['region']
        for group in cluster['groups']:
            diskSize = group['diskSize']
            instanceCount = group['instanceCount']
            instanceType = group['instanceType']
            services = group['services']

            igm = {
              'name': 'igm-' + region,
              'type': 'regional_igm.py',
              'properties': {
              }
            }
            config['resources'].append(igm)

    return config
