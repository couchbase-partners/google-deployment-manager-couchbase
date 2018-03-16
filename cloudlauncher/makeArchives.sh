#!/bin/sh

function makeArchive()
{
  license=$1
  rm archive-${license}.zip
  mkdir tmp

  cp couchbase-${license}.py tmp/couchbase.py
  cp couchbase.py.display tmp
  cp couchbase.py.schema tmp
  cp c2d_deployment_configuration.json tmp
  cp test_config.yaml tmp

  cp ../simple/deployment.py tmp
  cp ../simple/cluster.py tmp
  cp ../simple/group.py tmp
  cp ../simple/naming.py tmp
  cp ../simple/startupCommon.sh tmp
  cp ../simple/server.sh tmp
  cp ../simple/syncGateway.sh tmp
  cp ../simple/successNotification.sh tmp

  cp -r resources tmp

  zip -r -X archive-${license}.zip tmp
  rm -rf tmp
}

makeArchive byol
makeArchive hourly-pricing
