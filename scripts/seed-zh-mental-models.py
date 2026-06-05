#!/usr/bin/env python3
"""Idempotently localize built-in/shared mental models to Chinese.

This runs at container startup after the Hindsight API is healthy. It only updates
known mental model ids in the target bank and disables automatic refresh so the
localized content is not overwritten by later consolidation.
"""

from __future__ import annotations

import os
import sys
from urllib.parse import urlparse, unquote

try:
    import psycopg  # type: ignore
except Exception:  # pragma: no cover
    psycopg = None

try:
    import psycopg2  # type: ignore
except Exception:  # pragma: no cover
    psycopg2 = None

BANK_ID = os.environ.get("HINDSIGHT_ZH_MENTAL_MODEL_BANK_ID", "shared:user:agent-main")

UPDATES = {
    "fix-validation-must-use-user-visible-path": {
        "name": "修复验证必须走用户可见路径",
        "source_query": "修复不能只凭代码修改、配置存在或服务重启来判定完成；必须从用户实际可见的路径验证结果。",
        "content": """# 修复验证必须走用户可见路径

## 核心原则
代码修复、配置调整或服务操作，不能只凭间接证据宣称成功。必须通过用户实际会看到、会使用的入口完成验证。

## 不足以证明修好的证据
- 代码已经修改
- 配置文件里已有目标值
- 服务或容器已经重启
- 后端健康检查通过
- 日志没有明显报错

这些只能说明“改动已发生”，不能证明“用户侧已恢复”。

## 必须验证的证据
- 访问真实入口、域名、页面或命令路径
- 触发用户实际遇到的问题场景
- 看到期望输出、页面文案、接口返回或功能行为
- 对前端问题，确认运行中 bundle 已切换，而不只看源码
- 对配置问题，确认运行进程或容器实际读取了新配置

## 汇报口径
- 已通过用户可见路径验证：可以说“已修好”
- 只完成代码或配置修改：只能说“已修复根因，尚未完成用户侧验证”
- 验证受阻：明确说明阻塞点和下一步，不要用“大概率”替代验证
""",
    },
    "hindsight-is-for-durable-knowledge-not-runtime-noise": {
        "name": "Hindsight 应存长期知识，而不是运行噪音",
        "source_query": "Hindsight 适合保存稳定规则、架构事实和可复用经验；不应写入心跳、PID、内存采样、临时任务状态等短期运行噪音。",
        "content": """# Hindsight 应存长期知识，而不是运行噪音

Hindsight 的定位是结构化、可复用的知识层，不是运行日志仓库。

## 适合写入的内容
- 稳定的用户偏好和长期规则
- 架构事实、服务拓扑、关键配置约定
- 可复用的排障经验和踩坑结论
- 经过筛选后仍有长期价值的操作经验

## 不应写入的内容
- 心跳、健康检查、PID、端口瞬时状态
- 内存、CPU、磁盘等一次性采样
- 临时任务进度、批次编号、短期状态
- 工具空输出、补丁 diff、上下文压缩块
- 很快过期的会话过程噪音

## 实操规则
写入前先问：这条信息一周后是否仍有复用价值？
- 是：可以进入 Hindsight
- 否：留在日志、会话记录或监控系统即可

## 目标
保持 Hindsight 作为“可召回的长期经验库”，避免被运行噪音稀释召回质量。
""",
    },
    "hermes-hindsight-main-provider-vs-sidecar": {
        "name": "Hermes Hindsight 有主存储路径和 sidecar 补充路径",
        "source_query": "主 provider 是主要记忆后端；sidecar 是补充经验层。排障时必须区分配置层、聚合层和注入层。",
        "content": """# Hermes Hindsight 有主存储路径和 sidecar 补充路径

Hermes 接入 Hindsight 时，要区分两条路径。

## 主 provider 路径
主 provider 是 Hermes 的主要记忆后端，负责常规 memory search / add / recall 的主链路。它决定 Hermes 默认从哪里读写记忆。

## sidecar 路径
sidecar 是旁路补充层，通常用于沉淀经验、反思结果或结构化知识。它不等同于主存储，也不应被当作唯一记忆来源。

## 排障时要分三层看
- 配置层：Hermes、OpenClaw、插件、sidecar 的配置是否写在正确位置
- 聚合层：多个 bank / provider 的内容是否被正确召回、过滤、合并
- 注入层：召回结果是否进入最终 prompt，且没有泄漏到用户可见输出

## 常见误判
- sidecar 有数据，不代表 Hermes 主存储已切换到 Hindsight
- 主 provider 正常，不代表 sidecar 注入正常
- 配置文件存在，不代表运行进程实际读取了新配置

## 验收标准
必须分别验证：主记忆读写、sidecar retain/recall、最终 prompt 注入、用户可见输出无内部上下文泄漏。
""",
    },
    "openclaw-model-source-of-truth-is-multi-file": {
        "name": "OpenClaw 生效模型来源跨多个文件",
        "source_query": "判断 OpenClaw 实际生效的模型和 provider 时，需要同时检查 /root/.openclaw/openclaw.json 与 /root/.openclaw/agents/main/agent/models.json；同名 provider 漂移可能导致运行态与文件态不一致。",
        "content": """# OpenClaw 生效模型来源跨多个文件

判断 OpenClaw 当前实际使用的模型和 provider，不能只看单个配置文件。

## 必查文件
1. 全局配置：`/root/.openclaw/openclaw.json`
2. Agent 级模型配置：`/root/.openclaw/agents/main/agent/models.json`

这两个文件都可能影响最终运行态。

## 风险点
- 同名 provider 在不同文件中定义不同参数
- fallback / current model 指向与实际可用 provider 不一致
- 文件配置已改，但运行进程仍使用旧状态
- Telegram `/models` 展示与实际模型来源存在偏差

## 排查方法
- 同时读取两个配置文件
- 对比 provider 名称、base_url、model、上下文长度、fallback 顺序
- 检查运行日志或实际请求路径，确认哪个 provider 被调用
- 修改后必须验证运行态，而不是只看文件内容

## 结论
OpenClaw 的模型来源是多文件、多层合成结果。排障时必须以“实际运行调用 + 两处配置一致性”为准。
""",
    },
}


def connect():
    url = os.environ.get("HINDSIGHT_API_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("HINDSIGHT_API_DATABASE_URL/DATABASE_URL is not set")
    if psycopg is not None:
        return psycopg.connect(url)
    if psycopg2 is not None:
        p = urlparse(url)
        return psycopg2.connect(
            host=p.hostname,
            port=p.port or 5432,
            user=unquote(p.username or ""),
            password=unquote(p.password or ""),
            dbname=(p.path or "/").lstrip("/"),
        )
    raise RuntimeError("Neither psycopg nor psycopg2 is available")


def main() -> int:
    if os.environ.get("HINDSIGHT_ZH_DISABLE_MENTAL_MODEL_SEED", "").lower() in {"1", "true", "yes"}:
        print("[hindsight-zh] mental model seed disabled")
        return 0
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                updated = 0
                for model_id, item in UPDATES.items():
                    cur.execute(
                        """
                        UPDATE mental_models
                        SET name = %s,
                            source_query = %s,
                            content = %s,
                            trigger = jsonb_set(COALESCE(trigger, '{}'::jsonb), '{refresh_after_consolidation}', 'false'::jsonb, true),
                            last_updated = now()
                        WHERE bank_id = %s AND id = %s
                        """,
                        (item["name"], item["source_query"], item["content"], BANK_ID, model_id),
                    )
                    updated += cur.rowcount or 0
                conn.commit()
        print(f"[hindsight-zh] localized mental models updated={updated} bank={BANK_ID}")
        return 0
    except Exception as exc:
        print(f"[hindsight-zh] mental model localization skipped: {exc}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
