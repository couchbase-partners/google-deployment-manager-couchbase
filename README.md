# couchbase-google-deployment-manager

This is a Google Deployment Manger (DM) template that deploys Couchbase Enterprise to Google Compute Engine (GCE) on Google Cloud Platform (GCP).

Some best practices are covered [here](documentation/bestPractices.md).

## Deploying from the Command Line

To deploy from the command line you will need a GCP account and the glcoud tool installed.  Instruction for installing the Google Cloud SDK that includes gcloud are [here](https://cloud.google.com/sdk/).

To set up your environment, run the command:

    gcloud init

This repo countains four different parameters files.  You can deploy with any of them using [deploy.sh](deploy.sh).  For example, to deploy the simple configuration run the command:

    ./deploy.sh <some deployment name> simple

The script then passes the cluster configuration to GCP and builds your cluster automatically.
