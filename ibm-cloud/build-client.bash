#!/usr/bin/env bash
set -Eeuxo pipefail

ROOT=$PWD/../

cd ${ROOT}/chat-client
rm -r ./build
npm run-script build
cp Dockerfile ./build
docker build -t juchiast/chat-client:latest ./build
docker push juchiast/chat-client:latest
