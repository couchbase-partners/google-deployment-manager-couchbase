#!/bin/sh

#mkdir tmp

#cp -r ../simple/*.py tmp
cp -r ../simple/scripts tmp

cp -r resources tmp
cp c2d_deployment_configuration.json tmp
cp couchbase.jinja* tmp
cp test_config.yaml tmp

#rm -rf tmp
zip -r -X archive.zip tmp
