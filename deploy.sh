#!/bin/sh

DEPLOYMENT_NAME=$1
PARAMETERS_FILE=$2

gcloud deployment-manager deployments create ${DEPLOYMENT_NAME} --config parameters.${PARAMETERS_FILE}.yaml
