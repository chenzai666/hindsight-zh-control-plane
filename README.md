# hindsight-zh-control-plane

Hindsight 中文 control-plane 可复用部署层。

## 目标

解决官方 `ghcr.io/vectorize-io/hindsight` 在 `docker recreate` / 重建容器后前端恢复英文的问题。

本仓库通过：

- 基于官方 Hindsight 镜像构建
- 在构建阶段拉取 `vectorize-io/hindsight` `v0.6.2`
- 应用中文汉化 patch
- 重新构建 `hindsight-control-plane`
- 将中文 `standalone` 覆盖进最终镜像 `/app/control-plane`
- 一并包含 recall API 错误透传修复、Graph 2D 图谱页补翻译、Mental Models 页面扫尾汉化
- 启动时幂等同步 4 条默认 mental model 的中文内容，并关闭其自动刷新，避免重建后恢复英文

产出镜像：

- Docker Hub: `chenzai666/hindsight-zh-control-plane`

## 当前对应版本

- Upstream Hindsight: `0.6.2`
- Base runtime image: `ghcr.io/vectorize-io/hindsight:latest`

## 自动构建

GitHub Actions 工作流：

- push 到 `main` → 推送 `latest`
- push tag → 推送对应 tag
- 固定额外推送：`0.6.2`

## 仓库结构

- `Dockerfile` — 自定义镜像构建文件
- `patches/hindsight-control-plane-zh.patch` — 中文汉化 patch
- `.github/workflows/docker-image.yml` — Docker Hub 自动构建发布
- `INSTALL.md` — 使用说明
- `CHANGELOG.md` — 变更记录
- `notes/` — 说明与维护笔记
- `scripts/` — 辅助脚本

## GitHub Actions secrets

需要在仓库 Actions secrets 中配置：

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## 镜像使用示例

```yaml
services:
  hindsight:
    image: chenzai666/hindsight-zh-control-plane:latest
    container_name: hindsight-minimal
    restart: unless-stopped
    ports:
      - "9999:9999"
      - "8888:8888"
```

## 说明

本仓库只负责 control-plane 中文化部署层，不改 Hindsight API 行为。
