# Build VM Image

This README describes how we build the VMs that the templates use.  Users should not need to do this.

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
      python image_creator.py --project couchbase-public --disk ${INSTANCE} --name ${INSTANCE} --description ${INSTANCE} --destination_project couchbase-public --license couchbase-public/${INSTANCE}
    done


The admin portal is at https://console.cloud.google.com/partner/solutions?project=couchbase-public&authuser=1
