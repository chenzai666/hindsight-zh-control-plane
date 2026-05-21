# Hindsight runtime reconstruction

## Scope

This document captures the **current verified runtime shape** of the live `hindsight-minimal` container after switching it to the Chinese image layer.

Use it to recreate the service **without re-deriving everything from `docker inspect`** next time.

## Verified live facts

- Container name: `hindsight-minimal`
- Image: `chenzai666/hindsight-zh-control-plane:latest`
- Command: `['/app/start-all.sh']`
- Network mode: `hindsight-net`
- Published ports:
  - 8888 -> 8888/tcp
  - 9999 -> 9999/tcp
- Network aliases seen at inspect time:
  - (none recorded)

## Important notes

- Secrets are **masked** in this document.
- The database URL shown below is sanitized.
- Reuse the same real secrets from your existing deployment environment when recreating.
- Current deployment does **not** use bind mounts.
- Current deployment restart policy is `no`.

## Compose skeleton

```yaml
# Current verified deployment shape for hindsight-minimal
services:
  hindsight-minimal:
    image: chenzai666/hindsight-zh-control-plane:latest
    container_name: hindsight-minimal
    restart: "no"
    command: ["/app/start-all.sh"]
    network_mode: hindsight-net
    ports:
      - "8888:8888/tcp"
      - "9999:9999/tcp"
    environment:
      - HINDSIGHT_API_PORT=8888
      - HINDSIGHT_ENABLE_API=true
      - HINDSIGHT_API_HOST=0.0.0.0
      - HINDSIGHT_CP_DATAPLANE_API_URL=http://localhost:8888
      - PATH=/app/api/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      - LANG=C.UTF-8
      - PYTHON_VERSION=3.11.15
      - HF_HUB_VERBOSITY=error
      - HINDSIGHT_ENABLE_CP=true
      - HINDSIGHT_API_LLM_PROVIDER=minimax
      - HINDSIGHT_API_LLM_BASE_URL=https://api.minimaxi.com/v1
      - PYTHON_SHA256=272179ddd9a2e41a0fc8e42e33dfbdca0b3711aa5abf372d3f2d51543d09b625
      - HINDSIGHT_API_LOG_LEVEL=info
      - TRANSFORMERS_VERBOSITY=error
      - TOKENIZERS_PARALLELISM=***
      - HINDSIGHT_API_LLM_API_KEY=***
      - HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:***@hindsight-postgres:5432/hindsight
      - HF_HUB_DOWNLOAD_TIMEOUT=600
      - NODE_ENV=production
      - GPG_KEY=***
      - PYTHONUNBUFFERED=1
```

## docker run skeleton

```bash
docker run -d \
  --name hindsight-minimal \
  --restart no \
  -p 8888:8888/tcp \
  -p 9999:9999/tcp \
  -e 'HINDSIGHT_API_PORT=8888' \
  -e 'HINDSIGHT_ENABLE_API=true' \
  -e 'HINDSIGHT_API_HOST=0.0.0.0' \
  -e 'HINDSIGHT_CP_DATAPLANE_API_URL=http://localhost:8888' \
  -e 'PATH=/app/api/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
  -e 'LANG=C.UTF-8' \
  -e 'PYTHON_VERSION=3.11.15' \
  -e 'HF_HUB_VERBOSITY=error' \
  -e 'HINDSIGHT_ENABLE_CP=true' \
  -e 'HINDSIGHT_API_LLM_PROVIDER=minimax' \
  -e 'HINDSIGHT_API_LLM_BASE_URL=https://api.minimaxi.com/v1' \
  -e 'PYTHON_SHA256=272179ddd9a2e41a0fc8e42e33dfbdca0b3711aa5abf372d3f2d51543d09b625' \
  -e 'HINDSIGHT_API_LOG_LEVEL=info' \
  -e 'TRANSFORMERS_VERBOSITY=error' \
  -e 'TOKENIZERS_PARALLELISM=***' \
  -e 'HINDSIGHT_API_LLM_API_KEY=***' \
  -e 'HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:***@hindsight-postgres:5432/hindsight' \
  -e 'HF_HUB_DOWNLOAD_TIMEOUT=600' \
  -e 'NODE_ENV=production' \
  -e 'GPG_KEY=***' \
  -e 'PYTHONUNBUFFERED=1' \
  --network hindsight-net \
  chenzai666/hindsight-zh-control-plane:latest \
  /app/start-all.sh
```

## Required secret-bearing variables

When recreating, replace these masked values with the real ones:

- `HINDSIGHT_API_DATABASE_URL`
- `HINDSIGHT_API_LLM_API_KEY`
- any future token/secret variables

## Post-recreate verification checklist

After recreate, verify all of these:

1. `docker ps` shows `hindsight-minimal` running on image `chenzai666/hindsight-zh-control-plane:latest`
2. `docker logs hindsight-minimal` shows:
   - `Application startup complete.`
   - `Uvicorn running on http://0.0.0.0:8888`
   - `Starting Control Plane...`
   - `✅ Hindsight is running!`
3. `http://127.0.0.1:9999/` responds
4. control-plane bundle still contains Chinese UI strings such as `记忆构成`
5. API startup finishes against PostgreSQL without migration errors

## Why this file exists

This deployment was originally reconstructed from live container state. This file is the durable handoff so future recreates do not need another reverse-engineering pass.
