#!/bin/sh

#set environment
set -e

#check file directory
if [ -z "$FILE_DIR" ]; then
  echo >&2 "FILE_DIR must be set"
  exit 1
fi

#check AWS Bucket details
if [ -z "$AWS_BUCKET" ]; then
  echo >&2 "AWS_BUCKET must be set"
  exit 1
fi

#run mlflow server and sqlite and S3 one after another
mkdir -p "$FILE_DIR" && mlflow server \
    --backend-store-uri sqlite:///${FILE_DIR}/sqlite.db \
    --default-artifact-root s3://${AWS_BUCKET}/artifacts \
    --host 0.0.0.0 \
    --port $PORT