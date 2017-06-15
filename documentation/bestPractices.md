# Best Practices

## Compute

GCE offers both standard compute types and custom types.  Machine sizes depend on workload.  The standard Couchbase recommendations [here](https://developer.couchbase.com/documentation/server/current/install/pre-install.html) are a good place to start.

### Memory Allocation

The DM template is currently setting 50% for data and 25% for index.  These can be adjusted post deploy.

### Fault Tolerance and High Availability

The Couchbase concept of a Server Group maps closely to an Availability Zone.

## Storage

Google offers numerous storage options for IaaS.  When running Couchbase, three are viable:

* pd-ssd
* SSD Ephemeral Drive
* RAM Disk

For the vast majority of applications, pd-ssd is preferable.  It often outperforms the ephemeral as it is network bound and offers persistence that the ephemeral does not.  pd-ssd does all this at an attractive price point.

## Network

The Google network is globally flat.  This is amazing for running a geographically distributed database like Couchbase.  Private IPs can be routed around the world without need for VPN or leased line solutions.  When connecting with another cloud or an on-premises cluster in a hybrid scenario, VPN or leased lines are still required.

### Security

By default the template opens 8091 and 4984 to internet traffic.  You may want to consider closing these.
