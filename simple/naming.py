import re

def _SanitizeDeploymentName(deploymentName):
    sanitizedName = '-'.join(deploymentName.split("-")[-2:])[-20:]
    if re.match('[0-9-].*', sanitizedName):
        sanitizedName = 'cb-' + sanitizedName[-17:]
    return sanitizedName

def BaseDeploymentName(context):
    return _SanitizeDeploymentName(context.env['deployment'])

def ClusterName(context, clusterName):
    return '%s-%s' % (BaseDeploymentName(context), clusterName)

def GroupName(context, clusterName, groupName):
    return '%s-%s-%s' % (BaseDeploymentName(context), clusterName, groupName)

def RuntimeConfigName(context):
    return '%s-runtimeconfig' % BaseDeploymentName(context)

def WaiterName(context, clusterName, groupName):
    return '%s-%s-%s-waiter' % \
           (BaseDeploymentName(context), clusterName, groupName)

def ExternalIpVariableCreateActionName(context, clusterName, groupName):
    return '%s-%s-%s-ext-ip-create' % \
           (BaseDeploymentName(context), clusterName, groupName)

def ExternalIpVariableReadActionName(context, clusterName, groupName):
    return '%s-%s-%s-ext-ip-read' % \
           (BaseDeploymentName(context), clusterName, groupName)

def ExternalIpOutputName(clusterName, groupName):
    return 'externalIp-%s-%s' % (clusterName, groupName)

def FirewallName(context):
    return '%s-firewall' % BaseDeploymentName(context)

def InstanceTemplateName(context, clusterName, groupName):
    return '%s-%s-%s-it' % \
           (BaseDeploymentName(context), clusterName, groupName)

def InstanceGroupManagerName(context, clusterName, groupName):
    return '%s-%s-%s-igm' % \
           (BaseDeploymentName(context), clusterName, groupName)

def InstanceGroupInstanceBaseName(context, clusterName, groupName):
    return '%s-%s-%s-vm' % \
           (BaseDeploymentName(context), clusterName, groupName)
