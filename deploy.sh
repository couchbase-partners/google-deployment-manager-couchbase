#!/bin/sh

PARAMETERS_FILE=$1
DEPLOYMENT_NAME=$2

gcloud deployment-manager deployments create ${DEPLOYMENT_NAME} --config parameters.${PARAMETERS_FILE}.yaml
