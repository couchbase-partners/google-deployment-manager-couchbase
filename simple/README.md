# simple

This is an Google Deployment Manager (DM) template that installs Couchbase Enterprise.  You can run it from a cloud shell or the CLI on your local machine.

The template provisions Instance Group Managers (IGM), pd-ssd, and a Service Account to create a Runtime Config.

## Environment Setup

You will need a GCP account.  You can login to GCP [here](https://console.cloud.google.com/).  Once logged in, open up a cloud shell.

Now, you'll need a copy of this repo.  To make a local copy, run the commands:

    git clone https://github.com/couchbase-partners/google-deployment-manager-couchbase.git
    cd google-deployment-manager-couchbase
    cd simple

## Creating a Deployment

This repo contains four different parameters files.  You can deploy with any of them using [deploy.sh](deploy.sh).  For example, to deploy the simple configuration run the command:

    ./deploy.sh simple <some deployment name>

The script then passes the cluster configuration to GCP and builds your cluster automatically.

To access the cluster, open the [Google Cloud Console](http://cloud.google.com/console), navigate to Compute Engine and pick a node.  You can access Couchbase Server on port 8091 of the public IP of that node.  Couchbase Sync Gateway is accessible on port 4984.

## Deleting a Deployment

To delete your deployment you can either run the command below or use the GUI in the [Google Cloud Console](http://cloud.google.com/console).

    gcloud deployment-manager deployments delete <some deployment name>
