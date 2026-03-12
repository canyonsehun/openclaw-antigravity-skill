# memory-lancedb-pro 插件

**GitHub**: https://github.com/CortexReach/memory-lancedb-pro
**历史公开路径**: https://github.com/win4r/memory-lancedb-pro
**当前 GitHub 作者 / 维护者**: `CortexReach`
**推荐本地路径**: `~/.openclaw/plugins/memory-lancedb-pro`

## 简介

OpenClaw 的增强型长期记忆插件，替代内置 `memory-lancedb`。核心能力：

| 能力 | 内置 memory-lancedb | memory-lancedb-pro |
|---|---|---|
| 向量检索 | ✅ | ✅ |
| BM25 全文检索 | ❌ | ✅ |
| Hybrid 融合（向量 + BM25） | ❌ | ✅ |
| Cross-encoder 重排序 | ❌ | ✅ |
| 时间衰减 / 近期加权 | ❌ | ✅ |
| 长度归一化 / 噪声过滤 | ❌ | ✅ |
| MMR 多样性选择 | ❌ | ✅ |
| 多 Scope 隔离 | ❌ | ✅ |

## 安装方式

插件通过 git clone 直接加载（非 `openclaw plugins install`），然后在 `openclaw.json` 中 load path 方式注册：

```bash
git clone https://github.com/CortexReach/memory-lancedb-pro ~/.openclaw/plugins/memory-lancedb-pro
cd ~/.openclaw/plugins/memory-lancedb-pro && npm install
```

## 参考配置模板（openclaw.json）

```json
"plugins": {
  "allow": ["memory-lancedb-pro", "telegram"],
  "load": {
    "paths": ["~/.openclaw/plugins/memory-lancedb-pro"]
  },
  "slots": { "memory": "memory-lancedb-pro" },
  "entries": {
    "memory-lancedb-pro": {
      "enabled": true,
      "config": {
        "embedding": {
          "apiKey": "${JINA_API_KEY}",
          "model": "jina-embeddings-v5-text-small",
          "baseURL": "https://api.jina.ai/v1",
          "dimensions": 1024,
          "taskQuery": "retrieval.query",
          "taskPassage": "retrieval.passage",
          "normalized": true
        },
        "retrieval": {
          "mode": "hybrid",
          "vectorWeight": 0.7,
          "bm25Weight": 0.3,
          "minScore": 0.3,
          "rerank": "cross-encoder",
          "rerankProvider": "jina",
          "rerankApiKey": "${JINA_API_KEY}",
          "rerankModel": "jina-reranker-v3",
          "rerankEndpoint": "https://api.jina.ai/v1/rerank",
          "candidatePoolSize": 20,
          "recencyHalfLifeDays": 14,
          "recencyWeight": 0.1,
          "filterNoise": true,
          "lengthNormAnchor": 500,
          "hardMinScore": 0.35,
          "timeDecayHalfLifeDays": 60,
          "reinforcementFactor": 0.5,
          "maxHalfLifeMultiplier": 3
        },
        "dbPath": "~/.openclaw/memory/lancedb-pro",
        "autoCapture": true,
        "autoRecall": true,
        "sessionMemory": { "enabled": false },
        "enableManagementTools": false,
        "scopes": {
          "default": "global",
          "definitions": { "global": { "description": "共享知识库" } }
        }
      }
    }
  }
}
```

## 关键配置项说明（推荐值示例）

### Embedding（必填）

| 字段 | 说明 | 推荐值示例 |
|---|---|---|
| `apiKey` | Jina / OpenAI 兼容 API Key，支持数组轮转 | `${JINA_API_KEY}` |
| `model` | Embedding 模型名 | `jina-embeddings-v5-text-small` |
| `baseURL` | OpenAI-compatible endpoint | `https://api.jina.ai/v1` |
| `dimensions` | 向量维度 | `1024` |
| `taskQuery` / `taskPassage` | Jina 特有任务类型区分 | `retrieval.query` / `retrieval.passage` |

### Retrieval（检索）

| 字段 | 说明 | 推荐值示例 |
|---|---|---|
| `mode` | `hybrid`（向量+BM25）或 `vector` | `hybrid` |
| `vectorWeight` / `bm25Weight` | 融合权重，相加应为 1 | 0.7 / 0.3 |
| `rerank` | `cross-encoder` / `lightweight` / `none` | `cross-encoder` |
| `rerankProvider` | `jina` / `siliconflow` / `voyage` / `pinecone` / `vllm` | `jina` |
| `hardMinScore` | 所有评分阶段后的硬截止分数 | 0.35 |
| `timeDecayHalfLifeDays` | 时间衰减半衰期（天），0=禁用 | 60 |
| `recencyHalfLifeDays` | 近期加权半衰期（天） | 14 |

### 其他重要开关

| 字段 | 说明 | 推荐值示例 |
|---|---|---|
| `autoCapture` | 自动捕获对话中的重要信息 | `true` |
| `autoRecall` | 每轮自动注入相关记忆 | `true` |
| `sessionStrategy` | `memoryReflection` / `systemSessionMemory` / `none` | `none`（reflection 禁用） |
| `enableManagementTools` | 启用 memory_list / memory_stats 等管理工具 | `false` |

## 提供的工具

- `memory_recall` — 主动检索记忆
- `memory_store` — 存储新记忆
- `memory_forget` — 删除记忆
- `memory_update` — 更新记忆
- `self_improvement_log` — 记录自我改进日志

CLI 命令：`openclaw memory-pro`

## 推荐的每日更新任务模式

如果当前环境需要自动跟踪插件更新，推荐的 cron 流程是：

- `git fetch` 检查远端是否有新提交
- 有更新时：`git restore .` → `git pull --ff-only` → `npm install` → `openclaw gateway restart`
- 若你的环境额外依赖某个 zip / 规则包文件，应把它视为**可选增强项**，不要在前置检查阶段把“文件缺失”直接判成硬失败
- 结果可以投递到群、Webhook 或仅内部记录，具体取决于当前环境策略

手动触发可统一通过当前环境里的 cron job id 执行，例如：

```bash
openclaw cron run --id <job_id>
```

当前环境如果真的启用了自动更新任务，请以 `openclaw cron list --json` 的实时结果为准，不要把某个 job id / 时间 / 投递目标写死到产品说明里。

## 诊断

```bash
openclaw plugins info memory-lancedb-pro   # 查看状态 / 版本
openclaw plugins doctor                    # 插件健康检查
```

常见诊断模式：gateway healthy + lancedb-pro 注册成功 + Jina embedding 返回 200，但推理仍失败 → 排查上游模型的网络访问（可能被 Cloudflare 拦截，特征：HTTP 403 + `cf-mitigated: challenge`）。

## 注意事项

- **不要直接改插件源码**来实现业务功能（如 Telegram reaction），升级时会被覆盖。
- Telegram ack（👀）问题属于 channel 层，不是 LanceDB 问题，通过 `channels.telegram.reactionLevel` 配置解决。
- 若当前环境还有额外规则包、zip 包、铁律包等配套文件，请单独写到环境运维说明，不要混进插件通用能力说明。
