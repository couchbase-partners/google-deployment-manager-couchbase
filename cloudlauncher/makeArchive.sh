#!/bin/sh

rm archive.zip
mkdir tmp

cp couchbase.py tmp
cp couchbase.py.display tmp
cp couchbase.py.schema tmp
cp c2d_deployment_configuration.json tmp
cp test_config.yaml tmp

cp ../simple/deployment.py tmp
cp ../simple/cluster.py tmp
cp ../simple/group.py tmp
cp ../simple/server.sh tmp
cp ../simple/syncGateway.sh tmp

cp -r resources tmp

zip -r -X archive.zip tmp
rm -rf tmp
