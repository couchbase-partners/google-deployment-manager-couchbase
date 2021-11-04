#!/bin/sh

readonly ARCHIVE_NAME=archive-testdrive.zip

if [[ -f ${ARCHIVE_NAME} ]]; then
  echo "Removing ${ARCHIVE_NAME}..."
  rm ${ARCHIVE_NAME}
fi

if [[ -d tmp ]]; then
  echo "Removing tmp directory..."
  rm -rf tmp
fi

mkdir tmp

cp couchbase.py tmp
cp couchbase.py.schema tmp
cp test_config.yaml tmp

cp ../simple/deployment.py tmp
cp ../simple/deployment.py.schema tmp
cp ../simple/cluster.py tmp
cp ../simple/cluster.py.schema tmp
cp ../simple/group.py tmp
cp ../simple/group.py.schema tmp
cp ../simple/naming.py tmp
cp ../simple/startupCommon.sh tmp
cp ../simple/server.sh tmp
cp ../simple/syncGateway.sh tmp
cp ../simple/successNotification.sh tmp

cd tmp
zip -r -X ${ARCHIVE_NAME} .
cd -
mv tmp/${ARCHIVE_NAME} .
rm -rf tmp

echo "${ARCHIVE_NAME} created."
