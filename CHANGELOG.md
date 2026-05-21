# CHANGELOG

## 0.6.2

- 基于 Hindsight `0.6.2`
- 引入中文 control-plane patch
- 增加 GitHub Actions 自动构建并推送 Docker Hub 镜像
- 固化中文前端到镜像层，避免 `docker recreate` 后回退英文
