#!/usr/bin/env bash
set -Eeuxo pipefail

ROOT=$PWD/../

cd ${ROOT}/delayed-inserter
docker build -t juchiast/delayed-inserter:latest .
docker push juchiast/delayed-inserter:latest
