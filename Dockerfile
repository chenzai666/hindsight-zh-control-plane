ARG HINDSIGHT_VERSION=0.6.2
ARG HINDSIGHT_IMAGE_TAG=latest

FROM node:20-bookworm AS builder
ARG HINDSIGHT_VERSION
WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates python3 make g++ \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch v${HINDSIGHT_VERSION} https://github.com/vectorize-io/hindsight.git source
WORKDIR /build/source

COPY patches/hindsight-control-plane-zh.patch /tmp/hindsight-control-plane-zh.patch
RUN git apply /tmp/hindsight-control-plane-zh.patch

WORKDIR /build/source/hindsight-clients/typescript
RUN npm ci && npm run build

WORKDIR /build/source/hindsight-control-plane
RUN npm ci && npm run build

FROM ghcr.io/vectorize-io/hindsight:${HINDSIGHT_IMAGE_TAG}
ARG HINDSIGHT_VERSION
LABEL org.opencontainers.image.title="Hindsight ZH Control Plane" \
      org.opencontainers.image.description="Chinese-localized Hindsight control-plane layered on the official Hindsight image" \
      org.opencontainers.image.version="${HINDSIGHT_VERSION}" \
      org.opencontainers.image.source="https://github.com/chenzai666/hindsight-zh-control-plane"

USER root
RUN rm -rf /app/control-plane
COPY --from=builder /build/source/hindsight-control-plane/standalone /app/control-plane

COPY scripts/seed-zh-mental-models.py /app/zh-seed/seed-zh-mental-models.py
COPY scripts/start-all-zh.sh /app/start-all-zh.sh
RUN mv /app/start-all.sh /app/start-all.upstream.sh \
    && chmod +x /app/start-all-zh.sh /app/start-all.upstream.sh /app/zh-seed/seed-zh-mental-models.py \
    && chown -R hindsight:hindsight /app/control-plane /app/zh-seed /app/start-all-zh.sh /app/start-all.upstream.sh
USER hindsight

CMD ["/app/start-all-zh.sh"]
