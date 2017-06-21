# Best Practices

The Deployment Manager (DM) templates aim to configure Couchbase according to our recommended best practices on Google Compute Engine (GCE).

## Compute

GCE offers both standard compute types and custom types.  Machine sizes depend on workload.  The standard Couchbase recommendations [here](https://developer.couchbase.com/documentation/server/current/install/pre-install.html) are a good place to start.

We recommend deploying GCE nodes via an Instance Group Manager (IGM) as it improves reliability and simplifies the addition and removal of nodes.

### Memory Allocation

Couchbase recommends allocating 85% of system memory to the database. When using MDS this can be tuned between data, query, etc. The templates currently allocate 50% for data and 15% for index. This can be adjusted after deployment.

### Fault Tolerance and High Availability

The IGM in the templates places nodes across AZs in a round robin fashion.  For most installs this will be sufficient.

Ideally you may want to configure Couchbase Server Groups to map to Availability Zones.  The templates do not set this up.

## Storage

Google offers numerous storage options for IaaS.  When running Couchbase, three are viable:

* pd-ssd
* SSD Ephemeral Drive
* RAM Disk

For the vast majority of applications, pd-ssd is preferable.  It often outperforms the ephemeral as it is network bound and offers persistence that the ephemeral does not.  pd-ssd does all this at an attractive price point.

## Network

The Google network is globally flat.  This is amazing for running a geographically distributed database like Couchbase.  Private IPs can be routed around the world without need for VPN or leased line solutions.  When connecting with another cloud or an on-premises cluster in a hybrid scenario, VPN or leased lines are still required.

## Security

By default the template opens 8091 and 4984 to internet traffic.  You may want to consider closing these.

The template does not currently configure SSL. We recommend setting it up for production applications.
