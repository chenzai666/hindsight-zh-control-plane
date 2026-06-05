#!/usr/bin/env bash
set -euo pipefail

/app/start-all.upstream.sh &
UPSTREAM_PID=$!

cleanup() {
  kill "$UPSTREAM_PID" 2>/dev/null || true
  wait "$UPSTREAM_PID" 2>/dev/null || true
}
trap cleanup INT TERM

API_HEALTH_URL="${HINDSIGHT_API_HEALTH_URL:-http://localhost:8888/health}"
SEEDED=0
for _ in $(seq 1 120); do
  if ! kill -0 "$UPSTREAM_PID" 2>/dev/null; then
    wait "$UPSTREAM_PID"
    exit $?
  fi
  if curl -fsS "$API_HEALTH_URL" >/dev/null 2>&1; then
    python3 /app/zh-seed/seed-zh-mental-models.py || true
    SEEDED=1
    break
  fi
  sleep 1
done

if [ "$SEEDED" != "1" ]; then
  echo "[hindsight-zh] API did not become healthy before seed timeout; continuing" >&2
fi

wait "$UPSTREAM_PID"
