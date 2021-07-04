#!/usr/bin/env bash
set -Eeuxo pipefail

python3 init_database.py

gunicorn -b 127.0.0.1:8080 \
    --workers 4 \
    api:app
