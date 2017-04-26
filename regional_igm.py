# Copyright 2017 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

# limitations under the License.
"""Creates an autoscaled managed instance group."""
# This consists of multiple resources:
# - Instance Template to define the properties for each VM
#      The image and machine size are hardcoded. They could be parameterized
# - Instance Group Manager
# - Autoscaler to grow and shrink the size of the the Instance Group
# - Load Balancer to distribute traffice to the VMs.


URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

# Every Python Template needs to have the GenerateConfig() or generate_config()
# method
# This method is called by DM in expansion and must return either:
#    - the yaml format required by DM
#    - a python dictionary representing the yaml (this is more efficient)


def GenerateConfig(context):
  """Generates the configuration."""

  items = []
  for key, value in context.properties['metadata-from-file'].iteritems():
    items.append({
        'key': key,
        'value': context.imports[value]
        })
  metadata = {'items': items}

  deployment = context.env['deployment']
  machinesize = context.properties['machinesize']
  instance_template = deployment + '-it'
  igm = deployment + '-igm'
  region = context.properties['region']

  # Create a dictionary which represents the resources
  # (Intstance Template, IGM, etc.)
  resources = [
      {
          # Create the Instance Template
          'name': instance_template,
          'type': 'compute.v1.instanceTemplate',
          'properties': {
              'properties': {
                  'machineType': machinesize,
                  'networkInterfaces': [{
                      'network':
                          URL_BASE + context.env['project'] +
                          '/global/networks/default',
                      'accessConfigs': [{
                          'name': 'External NAT',
                          'type': 'ONE_TO_ONE_NAT'
                      }]
                  }],
                  'disks': [{
                      'deviceName': 'boot',
                      'type': 'PERSISTENT',
                      'boot': True,
                      'autoDelete': True,
                      'initializeParams': {
                          'sourceImage':
                              URL_BASE +
                              'ubuntu-os-cloud/global/images/ubuntu-1404-trusty-v20170424'
                      },
                      'diskType': 'pd-ssd',
                      'diskSizeGb': '100'
                  }],
                  'metadata': metadata,
              }
          }
      },
      {
          # Instance Group Manager
          'name': igm,
          'type': 'compute.v1.regionInstanceGroupManager',
          'properties': {
              'region': region,
              'baseInstanceName': deployment + '-instance',
              'instanceTemplate': '$(ref.' + instance_template + '.selfLink)',
              'targetSize': 4,
              'autoHealingPolicies': [{
                  'initialDelaySec': 60
              }]
          }
      }
  ]

  return {'resources': resources}
