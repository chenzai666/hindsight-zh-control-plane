# INSTALL

## 1. 拉取镜像

```bash
docker pull chenzai666/hindsight-zh-control-plane:latest
```

或指定版本：

```bash
docker pull chenzai666/hindsight-zh-control-plane:0.6.2
```

## 2. 运行

将你原本：

```bash
ghcr.io/vectorize-io/hindsight:latest
```

替换成：

```bash
chenzai666/hindsight-zh-control-plane:latest
```

## 3. docker compose 示例

```yaml
services:
  hindsight:
    image: chenzai666/hindsight-zh-control-plane:latest
    container_name: hindsight-minimal
    restart: unless-stopped
    ports:
      - "9999:9999"
      - "8888:8888"
    environment:
      - HINDSIGHT_API_DATABASE_URL=postgresql://user:pass@postgres:5432/hindsight
```

## 4. recreate 后是否会回英文

不会。

因为中文 control-plane 已经固化在镜像层里，不再依赖容器内手工替换。
