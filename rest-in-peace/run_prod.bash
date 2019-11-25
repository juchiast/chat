#!/usr/bin/env bash
set -Eeuxo pipefail

gunicorn -b 0.0.0.0:8080 \
    --workers 1 \
    api:app
