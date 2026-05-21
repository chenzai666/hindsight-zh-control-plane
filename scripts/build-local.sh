#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-chenzai666/hindsight-zh-control-plane:local}

docker build -t "$IMAGE_NAME" .
echo "Built: $IMAGE_NAME"
