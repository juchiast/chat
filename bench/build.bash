#!/usr/bin/env bash
set -Eeuxo pipefail

ROOT=$PWD/../

cd ${ROOT}/bench
docker build -t juchiast/chat-bench:latest .
docker push juchiast/chat-bench:latest
