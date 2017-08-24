def GenerateConfig(context):
    config={}
    config['resources'] = []

    zones = GetZonesList(context)
    for zone in zones:
        pass

    return config

def GetZonesList(context):
    zones = []
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

    assert len(zones) > 0, 'No regions selected for Couchbase nodes.'
    return regions
