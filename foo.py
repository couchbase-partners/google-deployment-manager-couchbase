    # Maybe move this under cluster?
    if 'mobileGateways' in context.properties:
        for gateways in context.properties['mobileGateways']:
            region = gateways['region']
            diskSize = gateways['diskSize']
            instanceCount = gateways['instanceCount']
            instanceType = gateways['instanceType']
            services = gateways['services']

            # make the instance group here
