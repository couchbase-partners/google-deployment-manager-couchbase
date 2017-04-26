# couchbase-google-deployment-manager

This is a Google Deployment Manger (DM) template that deploys Couchbase Enterprise to Google Compute Engine (GCE) on Google Cloud Platform (GCP).

Some best practices are covered [here](documentation/bestPractices.md).

## Deploying from the Command Line

To deploy from the command line you will need a GCP account and the glcoud tool installed.  Instruction for installing the Google Cloud SDK that includes gcloud are [here](https://cloud.google.com/sdk/).

To set up your Google environment, run the command:

    gcloud init

Now, you'll need a copy of this repo.  To make a local copy, run the commands:

    git clone https://github.com/couchbase-partners/google-deployment-manager-couchbase.git
    cd google-deployment-manager-couchbase

This repo countains four different parameters files.  You can deploy with any of them using [deploy.sh](deploy.sh).  For example, to deploy the simple configuration run the command:

    ./deploy.sh simple <some deployment name>

The script then passes the cluster configuration to GCP and builds your cluster automatically.

## Accessing the cluster

... need content

## Deleting a Deployment

To delete a deployment, run the command:

    gcloud deployment-manager deployments delete <some deployment name>

## Next Steps

...need links here
