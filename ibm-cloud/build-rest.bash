#!/usr/bin/env bash
set -Eeuxo pipefail

ROOT=$PWD/../

cd ${ROOT}/rest-in-peace
docker build -t juchiast/rest-in-peace:latest .
docker push juchiast/rest-in-peace:latest
