# Best Practices

The Deployment Manager (DM) templates aim to configure Couchbase according to our recommended best practices on Google Compute Engine (GCE).

## Compute

GCE offers both standard compute types and custom types.  Machine sizes depend on workload.  While one core machines will deploy successfully, [we recommend machines with 4 or more cores](https://developer.couchbase.com/documentation/server/current/install/pre-install.html) for production applications.

Machines with 16 cores and more will have higher I/O limits than machines with fewer cores.  For this reason we recommend 16 core machines for most applications.

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

As of 6/28/17, I/O for pd-ssd caps out at 1.7TB  This is not currently reflected in Google's documentation.

## Network

The Google network is globally flat.  This is amazing for running a geographically distributed database like Couchbase.  Private IPs can be routed around the world without need for VPN or leased line solutions.  When connecting with another cloud or an on-premises cluster in a hybrid scenario, VPN or leased lines are still required.

GCP also provides convenient setup of a VPN from your laptop to a GCP project, making it simple to connect applications to the cloud as you develop them.

## Security

The template automatically sets up a username and password for the Couchbase Web Administrator.  By default the template opens 8091 to internet traffic.  You may want to consider closing this.

The template does not currently configure SSL. We recommend setting it up for production applications.

These templates open Sync Gateway access to the internet over ports 4984 and 4985.  We typically recommend securing the admin interface for access from `127.0.0.1` only.  That can be done by editing the `/home/sync_gateway/sync_gateway.json` file.
