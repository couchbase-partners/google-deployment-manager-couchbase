# Getting Started on Cloud Launcher

This document describes how to get started using the Couchbase Enterprise offer on Google Cloud Launcher.  Cloud Launcher is a GUI for deploying ISV solutions in Google Cloud Platform (GCP).

## Deploying with Cloud Launcher

First, navigate to the Couchbase Cloud Launcher page [here](XXXXXXXXX).

![](./images/cloudlauncher01.png)

Now click "Launch on Compute Engine."  This will take you to a page where you can configure the VM settings.  The default Deployment name is over a character limit.  Enter a shorter deployment name like "couchbase."

![](./images/cloudlauncher02.png)

Enter a password in the "Couchbase Temporary Password" field.  This is the password that you will use to login to the Couchbase GUI on port 8091.

![](./images/cloudlauncher03.png)

Now click "Deploy."  You will be redirected to a screen in Deployment Manager.

![](./images/cloudlauncher04.png)

Deployment of the template will take several minutes.  Once deployed, the page will look like this:

![](./images/cloudlauncher05.png)

That's it!  Now it's just a matter of waiting for Couchbase to come up.

At this point a number of Instance Group Managers have been deployed.  It will take several more minutes for the VMs that those manage to start and for their startup scripts to complete installing and configuring Couchbase.  However, we can login and take a look around while that completes.

## Logging into Couchbase Server

You've now deployed Couchbase.  One next step is to inspect the resources that have been deployed and login to Couchbase Server.

Click the three horizontal lines at the top left of the screen to pull down the sidebar.  On that select "Compute Engine" and then "VM Instances."

![](./images/cloudlauncher06.png)

Now you can see a list of all the VMs being deployed by the Instance Group Managers that are part of the deployment we started.  Depending on how quickly you do this, they may still be deploying.  

![](./images/cloudlauncher07.png)

Click on one of the Server VMs to get a detailed view.

![](./images/cloudlauncher08.png)

Scroll down and copy the "External IP"

![](./images/cloudlauncher09.png)

Now paste that in another tab and type ":8091" after it to open a browser to Couchbase Server.

![](./images/cloudlauncher10.png)

If you've done that very quickly, you'll see the Couchbase Setup Screen.  The Deployment Manager template automatically sets Couchbase up, so we can just wait and hit refresh until that screen goes away.

![](./images/cloudlauncher11.png)

When setup is complete you'll see the login screen shown above.  Enter the "Couchbase Username" and "Couchbase Temporary Password" you provided earlier and press "Sign In."

![](./images/cloudlauncher12.png)

You'll now see the current view of the cluster.  If you've done this quickly, the cluster might not be done adding nodes and rebalancing yet.  Once it settles down you'll see a view like the one below.

![](./images/cloudlauncher13.png)

Feel free to click around, load sample buckets or try evaluating queries.  You can also setup XDCR links between the different clusters the deployment created.

## Logging into Couchbase Sync Gateway

Back in the GCP Console, go to the VM Instances view again.

![](./images/cloudlauncher14.png)

Now let's select a Sync Gateway node.

![](./images/cloudlauncher15.png)

Scroll down to get the "External IP" for that node.  Copy that.

![](./images/cloudlauncher16.png)

Now, open a new tab and past the "External IP" and type ":4984" after it.  This opens the interface for Couchbase Sync Gateway.  It's already setup and configured to connect to an empty bucket on the cluster.

![](./images/cloudlauncher17.png)

Open another browser tab, this time to the "External IP" followed by ":4985/\_admin/"

![](./images/cloudlauncher18.png)

This is the admin interface for Sync Gateway, once again connected to that empty bucket.

## SSH into a Server node

Go back to the "VM Instances" view.

![](./images/cloudlauncher19.png)

Click on a Server node.

![](./images/cloudlauncher20.png)

Then, under "Remote access," click on "SSH."  This will open a new tab.

![](./images/cloudlauncher21.png)

GCP is now automatically opening an SSH connection to that node.  When complete, you should see a terminal session.

![](./images/cloudlauncher22.png)

Try running these commands:

    cd /opt/couchbase/bin
    ls

![](./images/cloudlauncher23.png)

Couchbase is installed under this path.  Various commands to interact with Couchbase are in this directory.

## Next Steps

You've now deployed Couchbase Enterprise with both Server and Sync Gateway running, accessed the user interfaces and connected to a node via SSH.  For more steps and detailed tutorials please see the Couchbase [developer website](https://developer.couchbase.com/).
