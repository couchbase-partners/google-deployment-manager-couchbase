# Cloud Launcher

This folder contains artifacts for the Couchbase Cloud Launcher offer.  This should not be used directly, but through the Cloud Launcher instead.

# Build VM Image

First off, open up a cloud shell.  While you could do this on your local machine with gcloud, it's way easier to just use a cloud shell.

Now we need to decide what OS image to use.  We're using the latest Ubuntu 14.04.  You can figure out what that is by running:

    gcloud compute images list
    IMAGE_VERSION=v20180522
    IMAGE_NAME=ubuntu-1404-trusty-${IMAGE_VERSION}

Next, create an image for each license:

    LICENSES=( \
      couchbase-server-ee-byol \
      couchbase-sync-gateway-ee-byol \
      couchbase-server-ee-hourly-pricing \
      couchbase-sync-gateway-ee-hourly-pricing \
    )

    for LICENSE in "${LICENSES[@]}"
    do
      INSTANCE=${LICENSE}-${IMAGE_VERSION}
      gcloud compute instances create ${INSTANCE} \
        --project "couchbase-public" \
        --zone "us-central1-f" \
        --machine-type "n1-standard-8" \
        --network "default" \
        --maintenance-policy "MIGRATE" \
        --scopes default="https://www.googleapis.com/auth/cloud-platform" \
        --image "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/${IMAGE_NAME}" --boot-disk-size "20" \
        --boot-disk-type "pd-standard" \
        --boot-disk-device-name ${INSTANCE} \
        --no-boot-disk-auto-delete \
        --scopes "storage-rw"
    done

Now we're going to delete all four VMs.  We'll be left with their boot disks.  This command takes a few minutes to run and doesn't print anything.  

    for LICENSE in "${LICENSES[@]}"
    do
      INSTANCE=${LICENSE}-${IMAGE_VERSION}
      gcloud compute instances delete ${INSTANCE} \
        --project "couchbase-public" \
        --zone "us-central1-f"
    done

We were previously piping yes, but that doesn't seem to be working currently, so you'll have to type "y" a few times.

Now you need to attach the license ID to each image.  That process is described [here](https://cloud.google.com/launcher/docs/partners/technical-components#create_the_base_solution_vm).  
Note that you do not need to mount the disks and delete files since none were created.  To start, install the partner utilities:

    mkdir partner-utils
    cd partner-utils
    curl -O https://storage.googleapis.com/c2d-install-scripts/partner-utils.tar.gz
    tar -xzvf partner-utils.tar.gz
    sudo python setup.py install

Now apply the license:

    for LICENSE in "${LICENSES[@]}"
    do
      INSTANCE=${LICENSE}-${IMAGE_VERSION}
      python image_creator.py \
        --project couchbase-public \
        --disk ${INSTANCE} \
        --name ${INSTANCE} \
        --description ${INSTANCE} \
        --destination-project couchbase-public \
        --license couchbase-public/${LICENSE}
    done

The license ID for ubuntu-os-cloud/ubuntu-1404-trusty should be attached by default.

# Create Deployment Package

To create the deployment package run

    ./makeArchives.sh

You'll upload archive-byol.zip and archive-hourly-pricing.zip in the portal at a later point in this process.

# Create Solutions

Couchbase has two solutions in Cloud Launcher.  Those can be edited in the Partner Portal [here](https://console.cloud.google.com/partner/solutions?project=couchbase-public).  The copy for the solutions is as follows:

## 1 - Solution Metadata

### Solution Name
* couchbase-enterprise-edition
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
* Couchbase Enterprise Edition
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

### More solution info
https://www.couchbase.com/partners/google/

### Version
Couchbase EE

### Category ID
* Big Data
* Databases

## 3 - Company Information

### Name of Company
Couchbase

### Company Description
Couchbase provides the world’s most complete, scalable, and highest performing NoSQL database. We engineered the product to meet the most demanding enterprise and big data requirements for distributed database performance and scalability.

## 4 - Test Drive
To update the Test Drive login to [Orbitera](https://www.orbitera.com/).  You'll then want to build the template under [testdrive](../testdrive).  The manual is [here](https://github.com/couchbase-partners/test-drive).

## 5 - Documentation & Support

### Tutorials and Documentation

#### Type
Documentation

#### URL
https://developer.couchbase.com/documentation/server/current/cloud/couchbase-gcp-cloud-launcher.html

#### Description
Deploying Couchbase on Google Cloud Launcher

### Support description
With Couchbase customers all around the world, our support team provides global coverage. So wherever you’re located, we’ve got you covered. For customers requiring round-the-clock support, 24x7x365 service level agreements are available.

### Support URL
http://support.couchbase.com/

### EULA URL
https://www.couchbase.com/ESLA02152018

## 6 - Deployment Package

### Configure Deployment Package
Select "Upload a package" and upload the zip you created with [markArchives.sh](makeArchives.sh) earlier.  With this complete you can test and publish the offer.  You may want to upload the package before configuring anything else since it sometimes clobbers others changes in the portal.  This package upload will clobber the solution name, so BYOL will need to be renamed after upload.
