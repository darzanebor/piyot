#!/bin/bash
gunicorn -u `id -u` -g `id -g` --threads=1 --workers=2 --log-config=gunicorn_logging.conf --worker-connections="${PIYOT_WORKER_CONN:-500}" --bind="${PIYOT_HOST:-0.0.0.0}:${PIYOT_PORT:-5000}" main:application
