# deployment

This directory contains a **directly usable** Docker Compose deployment template for the Chinese Hindsight image layer.

## Files

- `docker-compose.yml` — deploys:
  - `hindsight-postgres`
  - `hindsight-minimal`
- `.env.example` — environment variable template

## Quick start

```bash
cd deployment
cp .env.example .env
# edit .env with your real secrets

# create the external Docker network once if it does not exist
docker network create hindsight-net 2>/dev/null || true

docker compose up -d
```

## What this template assumes

- Hindsight image: `chenzai666/hindsight-zh-control-plane:latest`
- PostgreSQL image: `pgvector/pgvector:pg18`
- Network: existing external network `hindsight-net`
- Ports:
  - `8888` for API
  - `9999` for control-plane

## Required environment variables

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `HINDSIGHT_API_LLM_PROVIDER`
- `HINDSIGHT_API_LLM_BASE_URL`
- `HINDSIGHT_API_LLM_API_KEY`
- `HINDSIGHT_API_LLM_MODEL`

`docker-compose.yml` builds `HINDSIGHT_API_DATABASE_URL` from `${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, and `${POSTGRES_DB}`. Do not replace it with a literal masked password such as `***`.

## Post-deploy verification

```bash
docker compose ps
docker logs hindsight-minimal --tail 200
curl http://127.0.0.1:9999/
```

Check for these startup signals in logs:

- `Application startup complete.`
- `Uvicorn running on http://0.0.0.0:8888`
- `✅ Hindsight is running!`

## Notes

- This template is derived from the currently verified live runtime shape.
- It is meant to replace future ad-hoc reconstruction from `docker inspect`.
- Secrets are intentionally externalized into `.env`.
