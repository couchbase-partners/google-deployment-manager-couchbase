# Build VM Image

This README describes how we build the VM that the templates use.  Users should not need to do this.

# Script

    INSTANCE=couchbase-45ce
    NEWINSTANCE=couchbase-new-$INSTANCE
    SNAPSHOT=image-snapshot-$INSTANCE
    IMAGEDISK=image-disk-$INSTANCE
    TEMPORARYDISK=temporary-disk-$INSTANCE

    gcloud compute instances stop $INSTANCE
    gcloud compute disks snapshot $INSTANCE  --snapshot-names  $SNAPSHOT
    gcloud compute disks create $IMAGEDISK --source-snapshot $SNAPSHOT
    gcloud compute disks create $TEMPORARYDISK --size 200
    gcloud compute instances create $NEWINSTANCE --scopes storage-rw --disk name=$IMAGEDISK,device-name=$IMAGEDISK --disk name=$TEMPORARYDISK,device-name=$TEMPORARYDISK
    gcloud compute ssh $NEWINSTANCE

    sudo mkdir /mnt/tmp
    sudo mkfs.ext4 -F /dev/disk/by-id/google-$TEMPORARYDISK
    sudo mount -o discard,defaults /dev/disk/by-id/google-$TEMPORARYDISK /mnt/tmp
    sudo mkdir /mnt/image-disk
    sudo mount /dev/disk/by-id/google-$IMAGEDISK-part1 /mnt/image-disk

    sudo umount /mnt/image-disk/
    sudo dd if=/dev/disk/by-id/google-$IMAGEDISK of=/mnt/tmp/disk.raw bs=4096
