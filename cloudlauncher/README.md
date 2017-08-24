# Cloud Launcher

This folder contains artifacts for the Couchbase Cloud Launcher offer.  This should not be used diretly, but through the Cloud Launcher instead.

# Build VM Image

First off, we need to decide what OS image to use.  We're using the latest Ubuntu 14.04.  You can figure out what that is by running:

    gcloud compute images list
    IMAGE_NAME=ubuntu-1404-trusty-v20170718

Next, create the instances:

    INSTANCES=( couchbase-server-ee-hourly couchbase-sync-gateway-ee-hourly couchbase-server-ee-byol couchbase-sync-gateway-ee-byol)

    for INSTANCE in "${INSTANCES[@]}"
    do
      gcloud compute --project "couchbase-public" instances create ${INSTANCE} --zone "us-central1-f" --machine-type "n1-standard-8" --network "default" --maintenance-policy "MIGRATE" --scopes default="https://www.googleapis.com/auth/cloud-platform" --image "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/${IMAGE_NAME}" --boot-disk-size "20" --boot-disk-type "pd-standard" --boot-disk-device-name ${INSTANCE} --scopes "storage-rw"
    done

Now make sure the instances all started up ok:

    for INSTANCE in "${INSTANCES[@]}"
    do
      gcloud compute instances describe ${INSTANCE}
    done

Now you need to attach the license ID to each image.  That process is described [here](https://cloud.google.com/launcher/docs/partners/technical-components#create_the_base_solution_vm).  Note that you do not need to mount the disks and delete files since none were created.  If everything is configured, all you need to do is delete the instances while not deleting the disks and then run:

    for INSTANCE in "${INSTANCES[@]}"
    do
      python image_creator.py --project couchbase-public --disk ${INSTANCE} --name ${INSTANCE} --description ${INSTANCE} --destination-project couchbase-public --license couchbase-public/${INSTANCE}
    done

# Create Deployment Package

To create the deployment package run

    ./makeArchive.sh

Upload archive.zip later in the portal.  Note that you will have to modify `group.py` to create the Hourly Pricing and BYOL offers.

# Create Solutions

Couchbase has two solutions in Cloud Launcher.  Those can be edited in the Partner Portal [here](https://console.cloud.google.com/partner/solutions?project=couchbase-public&authuser=1).  The copy for the solutions is as follows:

## 1 - Solution Metadata

### Solution Name
* couchbase-enterprise-edition-hourly-pricing
* couchbase-enterprise-edition-byol

### Search Metadata
Couchbase, NoSQL, Big Data, Cache, Database

### Search Keywords
* Couchbase
* NoSQL
* Big Data
* Cache
* Database

## 2 - Solution Details

### Name of Solution
* Couchbase Enterprise Edition (Hourly Pricing)
* Couchbase Enterprise Edition (BYOL)

### Tagline
The system of engagement database for web, mobile and IoT

### Solution Icon
[./resources/en-us/logo.png](./resources/en-us/logo.png)

### Solution Description
Couchbase Server provides highly elastic, available, scalable & real-time big data management system with consistent high performance, flexible global deployment topologies and a set of native SDKs to ease development & deployment of modern applications.

### Price Description
This template includes a license for Couchbase Enterprise Edition and <a href="https://www.couchbase.com/support-policy">Silver Support</a>.

This template is for bring your own license (BYOL) users.  To purchase a license go <a href="https://www.couchbase.com/subscriptions-and-support">here</a>.

### Version
4.6.2

### Category ID
* Big Data
* Databases

## 3 - Company Information

### Name of Company
Couchbase

### Company Description
Couchbase provides the world’s most complete, scalable, and highest performing NoSQL database. We engineered the product to meet the most demanding enterprise and big data requirements for distributed database performance and scalability.

## 4 - Test Drive (Optional)
We're currently working with Orbitera on the Test Drive.  It's not yet complete.

## 5 - Documentation & Support

### Support Description
With Couchbase customers all around the world, our support team provides global coverage. So wherever you’re located, we’ve got you covered. For customers requiring round-the-clock support, 24x7x365 service level agreements are available.

### Support URL
http://support.couchbase.com/

### EULA URL
https://www.couchbase.com/docs/common/terms-of-service.html

## 6 - Deployment Package

### Configure Deployment Package
Select `Upload a package` and upload the zip you created with `markArchive.sh` earlier.  Once complete you can test the BYOL by clicking [here](https://console.cloud.google.com/launcher/config/couchbase-public/couchbase-enterprise-edition-byol?src=console&project=couchbase-dev&authuser=1&preview=couchbase-public%2Fcouchbase-enterprise-edition-byol).
