#!/usr/bin/env bash
set -Eeuxo pipefail

gunicorn -b 127.0.0.1:8080 \
    --workers 4 \
    api:app
