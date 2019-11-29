#!/usr/bin/env bash
set -Eeuxo pipefail

gunicorn -b 127.0.0.1:8080 \
    --worker-class eventlet \
    --workers 1 \
    api:app
