def GenerateConfig(context):
    config={}
    config['resources'] = []
    config['outputs'] = []

    couchbaseUsername=context.properties['couchbaseUsername']
    couchbasePassword=context.properties['couchbasePassword']

    for cluster in context.properties['clusters']:
        region = cluster['region']
        for nodes in cluster['nodes']:
            diskSize = nodes['diskSize']
            instanceCount = nodes['instanceCount']
            instanceType = nodes['instanceType']
            services = nodes['services']

            config['resources'].append(regional_igm())

    if 'mobileGateways' in context.properties:
        for gateways in context.properties['mobileGateways']:
            region = gateways['region']
            diskSize = gateways['diskSize']
            instanceCount = gateways['instanceCount']
            instanceType = gateways['instanceType']
            services = gateways['services']

            # make the instance group here

    return config
