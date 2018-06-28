#!/bin/bash

# breaks for symlinks
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

AWSREGION="us-east-1"
AWS_ACCESS_KEY_ID=AKIAJNHXLYCGYXFMDAYA
AWS_SECRET_ACCESS_KEY=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

# S3 parameters
S3BUCKET_NAME="npm-ci-cache"
S3STORAGE_TYPE="STANDARD"
CONTENT_TYPE="application/x-compressed-tar"
DATE_VALUE=`date -R`

cd /frontend

# if no cache file was downloaded, create one and upload
FILE="npm_cache.tar"

# try to download the cache file from s3
URL="https://s3.amazonaws.com/${S3BUCKET_NAME}/${FILE}"
STATUSCODE=$(curl --silent --output $FILE --write-out "%{http_code}" $URL)

echo "Downloading cache file from S3"
# check if the download succeeded
if [ -f "${FILE}" ]; then
    tar -zxf "${FILE}"

    if [ "$?" != "0" ]; then
        # corrupt file
        STATUSCODE="999"
    else
        minimumsize=1000000
        actualsize=$(wc -c <"$FILE")
        if [ $actualsize -lt $minimumsize ]; then
            # file too small to be correct
            # probably an empty file
            STATUSCODE="1000"
        fi
    fi
fi

if [ "$STATUSCODE" == "1000" ]; then
    echo "Downloading the cache file failed. Reason: file too small ($actualsize bytes)."
fi
if [ "$STATUSCODE" == "999" ]; then
    echo "Downloading the cache file failed. Reason: Corrupted file."
fi
if [ "$STATUSCODE" != "200" ]; then
    echo "Downloading the cache file failed. Reason: $STATUSCODE"
fi

npm set progress false
npm set global true
npm set global-style true
npm set prefix "/frontend"
npm set userconfig "/frontend/node_modules"
# changes the default cache location
npm set cache "/frontend/.npm"
# The age of the cache, in seconds
npm set searchstaleness=3600000

cd $(npm root -g)/npm
npm install fs-extra
sed -i -e s/graceful-fs/fs-extra/ -e s/fs\.rename/fs.move/ ./lib/utils/rename.js
cd /frontend

# install the packages
npm install -g cache-shrinkwrap --prefer-offline --prefix /frontend
# cache the packages from the shrinkwrap file
cache-shrinkwrap /frontend/npm-shrinkwrap.json
npm install -g webpack phantomjs-prebuilt --prefer-offline --unsafe-perm --prefix /frontend
npm install -g --prefer-offline --unsafe-perm --prefix /frontend
npm install -g

if [ "$1" == "production" ]; then
    npm run publish --prefix /frontend
fi

# if no cache file was downloaded, create one and upload
if [ "$STATUSCODE" != "200" ]; then
    echo "Uploading a new cache file to S3"
    tar -zcf "${FILE}" /frontend/.npm /frontend/lib/node_modules/

    resource="/${S3BUCKET_NAME}/${FILE}"
    stringToSign="PUT\n\n${CONTENT_TYPE}\n${DATE_VALUE}\n${resource}"
    signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${AWS_SECRET_ACCESS_KEY} -binary | base64`
    curl --silent -X PUT -T "${FILE}" \
      -H "Host: ${S3BUCKET_NAME}.s3.amazonaws.com" \
      -H "Date: ${DATE_VALUE}" \
      -H "Content-Type: ${CONTENT_TYPE}" \
      -H "Authorization: AWS ${AWS_ACCESS_KEY_ID}:${signature}" \
      https://${S3BUCKET_NAME}.s3.amazonaws.com/${FILE}
    echo "New cache file uploaded to S3"
fi