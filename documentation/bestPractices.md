# Best Practices

## Compute

All services on all nodes
* n1-something

Using MDS
Data - ...
Query - ...
Index - ...

### Memory Allocation

We're currently doing 50% for data and 25% for index.  These can be adjusted post deploy.

### Fault Tolerance and High Availability

The Couchbase concept of a Server Group maps closely to an Availability Zone.

Q: How to autoscaling groups in GCP work with AZs?

## Storage

Google offers numerous storage options for IaaS.  When running Couchbase, three are viable:

* pd-ssd
* SSD Ephemeral Drive
* RAM Disk

## Network

The Google network is globally flat.  This is amazing for running a geographically distributed database like Couchbase.  Private IPs can be routed around the world without need for VPN or leased line solutions.  When connecting with another cloud or an on-premises cluster in a hybrid scenario, VPN or leased lines are still required.

### Security

A number of steps are necessary to secure a Couchbase cluster:
* Configure authentication for the administrator tool
* Enable SSL for traffic between nodes
* Enable authentication for connections to the database as well.
