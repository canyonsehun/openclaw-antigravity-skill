<div align="center">

# 🦞 openclaw-graduate · OpenClaw 运维 Skill 仓库

**一个面向真实环境的 OpenClaw 配置、部署、排障与运营手册仓库**

*把本地 macOS、远端 Codespaces、Telegram Bot、Claude Code / Codex / Relay / Jina / memory-lancedb-pro 的实战经验，整理成可直接执行的 skill 与参考文档。*

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/canyonsehun/openclaw-graduate)
[![Operations](https://img.shields.io/badge/Focus-Operations%20%26%20Troubleshooting-6f42c1)](https://github.com/canyonsehun/openclaw-graduate)
[![Codespaces](https://img.shields.io/badge/Remote-Codespaces-24292f)](https://github.com/features/codespaces)
[![Telegram](https://img.shields.io/badge/Channel-Telegram-26A5E4)](https://telegram.org/)
[![Claude Code](https://img.shields.io/badge/Tool-Claude%20Code-D97706)](https://www.anthropic.com/claude-code)
[![Codex](https://img.shields.io/badge/Tool-Codex-0F766E)](https://openai.com/)

**中文（当前）** | [English](./README.en.md)

</div>

---

## ✨ 为什么有这个仓库

OpenClaw 官方文档很全，但很多内容偏通用。这个仓库更像一份 **“已经在真实机器上踩过坑、确认能跑通”** 的运维手册：  
它记录的是我们本地与远端环境里，真正用过、改过、验证过的流程和结论。

| 场景 | 这个仓库提供什么 |
|---|---|
| 🛠️ **初次安装 / 修复** | `openclaw setup`、`doctor --repair`、Gateway 启停、基本健康检查 |
| 🤖 **多 Bot / 多 Agent 路由** | Telegram Bot 接入、agent 绑定、默认模型、`/model` 目录维护 |
| 🧠 **模型切换** | `codex`、`anthropic / Claude`、relay、OpenAI-compatible provider 的接法与验证 |
| ☁️ **远端部署** | GitHub Codespaces / github.dev 的启动方式、环境变量、远端 Gateway 习惯用法 |
| 🔍 **排障** | 403 / 429、Cloudflare challenge、错模型、不回复、JSON 写错、session 锁、插件异常 |
| 🧩 **记忆插件联动** | `memory-lancedb-pro` 的安装、配置、更新检查与运行诊断 |

---

## 🚀 这个仓库能帮你什么

- **安装与修复**：覆盖 `openclaw setup`、`openclaw doctor --repair`、`gateway start/restart/status`、`channels status`、`agents list`
- **模型与厂商切换**：整理 `codex`、`anthropic / Claude`、OpenAI-compatible relay 的接法、默认模型、fallback 与 smoke test
- **Bot 与频道接入**：支持 Telegram Bot 接入、agent 绑定、默认模型指定、多 bot 路由和 `/model` 可选目录维护
- **远端部署**：包含 GitHub Codespaces / github.dev 的启动方式、`~/.secrets/openclaw.env` 约定与远端 Gateway 启动思路
- **插件与记忆排查**：覆盖 `memory-lancedb-pro` 注册、Jina embedding 探针、插件加载异常、session 锁等问题
- **Claude Code 联动**：记录 Claude Code 可用时如何作为 OpenClaw 的后备执行入口，以及最小冒烟验证方法
- **诊断与回归验证**：给出 403 / 429、Cloudflare challenge、错模型、不回复、配置写死、JSON 配错、路由异常等排查路径

---

## 🧭 快速导航

| 文档 | 用途 |
|---|---|
| `SKILL.md` | 主技能说明，适合直接给 Agent 执行 |
| `references/official.md` | OpenClaw 官方行为、版本更新、命令参考 |
| `references/providers.md` | `codex` / Claude / 其他 provider 配置方法 |
| `references/channels.md` | Telegram / WhatsApp / Slack 等 channel 配置 |
| `references/multi_agent.md` | 多 Agent、绑定与路由说明 |
| `references/memory-lancedb-pro.md` | `memory-lancedb-pro` 插件配置、工具、cron 更新任务与诊断 |
| `references/experience-distill-bot.md` | 经验提炼 bot / skill distill bot：把 `main` 对话里的稳定结论整理成 skill/reference 草稿 |
| `scripts/provision_telegram_bot.py` | 一键接入 Telegram Bot |
| `scripts/sync_relay_models.py` | 同步 relay 模型目录 |

---

## 🧠 memory-lancedb-pro 插件来源与作者

这个仓库里收录了 `memory-lancedb-pro` 的集成说明，但 **插件代码本身不属于本仓库**。

- **当前来源仓库**：[`CortexReach/memory-lancedb-pro`](https://github.com/CortexReach/memory-lancedb-pro)
- **历史公开仓库路径**：[`win4r/memory-lancedb-pro`](https://github.com/win4r/memory-lancedb-pro)（现已迁移/跳转）
- **当前 GitHub 作者 / 维护者**：`CortexReach`
- **我们在这里维护的内容**：OpenClaw 侧的安装、接入、更新检查、排障和使用说明

如果你要改插件源码，应回到上游仓库处理；本仓库负责的是 **“怎么把它在 OpenClaw 里用好”**。

---

## 🌟 这个仓库的亮点

- **来自真实环境**：不是纯文档摘抄，而是本地 macOS、远端 Codespaces、真实 provider 与 bot 配置踩坑后的可用方案
- **结论可直接执行**：尽量给出命令、配置路径、验证方式和失败信号，不写空泛说明
- **本地与远端分开讲**：明确区分本地可用、远端受限、Cloudflare 拦截、Claude fallback 等不同场景
- **聚焦运维与排障**：重点放在“为什么不能用”“该改哪里”“怎么确认修好”
- **保留可复用脚本**：仓库里有 Telegram Bot 接入脚本和 relay 模型同步脚本，适合直接复用

---

## 📦 仓库结构

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 主技能说明 |
| `references/` | 分主题操作参考 |
| `scripts/` | 辅助脚本 |
| `CHANGELOG.md` | 仓库自身更新记录 |

---

## ⚡ 快速开始

### 1. 直接阅读主 Skill

```bash
open /Users/shmily/.codex/skills/openclaw/SKILL.md
```

### 2. 常用验证命令

```bash
openclaw --version
openclaw gateway status
openclaw channels status
openclaw agents list --json
```

### 3. 无 channel 的最小冒烟测试

```bash
openclaw agent --local --agent main --message "reply only: ok" --json
```

---

## 当前范围

- OpenClaw 安装、升级、Gateway 运维
- Telegram / WhatsApp / Slack 等 channel 配置
- 模型 provider 配置与切换
- 远端 Codespaces / github.dev 部署与诊断
- 常见故障排查：403 / 429、错模型、不回复、session 锁、插件注册异常

## 更新原则

- 只同步当前本地 `~/.codex/skills/openclaw` 的有效内容
- 只保留对操作者有价值的流程、命令、配置与排障结论
- 提交前不保留真实 key / token / chat id 等敏感信息

---

## 🧠 memory-lancedb-pro 插件使用指南

**GitHub**：[`CortexReach/memory-lancedb-pro`](https://github.com/CortexReach/memory-lancedb-pro)  
**历史来源**：[`win4r/memory-lancedb-pro`](https://github.com/win4r/memory-lancedb-pro)  
**当前 GitHub 作者 / 维护者**：`CortexReach`

### 插件是做什么的

OpenClaw 自带一个基础记忆插件 `memory-lancedb`，只支持向量检索。`memory-lancedb-pro` 是它的增强替代版，解决的核心问题是：**Agent 的长期记忆太容易"找错"或"找不到"**。

具体来说，插件做了以下几件事：

**① 混合检索（Hybrid Retrieval）**
同时跑向量检索和 BM25 关键词检索，再把两路结果融合。向量检索擅长语义相似（"怎么重启"能匹配到"如何重开"），BM25 擅长精确关键词（专有名词、命令名不会被语义模糊掉）。两者互补，比单纯向量检索漏召率低很多。

**② Cross-encoder 重排序（Rerank）**
融合后的候选结果，再用 Jina Reranker（或其他服务）做一轮精排，把"语义沾边但其实不相关"的噪声结果踢掉，让最终注入上下文的记忆精准度更高。

**③ 时间衰减 + 近期加权**
旧记忆分数随时间自动衰减（默认半衰期 60 天），近期记忆额外加权（半衰期 14 天）。防止几个月前过时的信息压过最新的配置变更。被频繁召回的记忆衰减更慢（强化因子 0.5），相当于"越用越重要"。

**④ 自动捕获 + 自动注入**
对话过程中自动识别重要信息存入数据库（`autoCapture`），每轮对话开始前自动检索相关记忆注入上下文（`autoRecall`），无需手动调用工具，Agent 开箱即有长期记忆能力。

**⑤ 噪声过滤 + 长度归一化**
自动过滤 Agent 的拒答、元问题、模板套话等无意义内容，避免污染记忆库。超长条目得分会被适度惩罚，防止一条超长记忆霸占所有召回名额。

**⑥ 多 Scope 隔离**
可以给不同 Agent 或不同业务域划分独立的记忆空间（Scope），互不干扰。默认使用 `global` 共享知识库，也可以给每个 Agent 单独分配 Scope 并设置访问权限。

**⑦ 长文档自动分块**
存入超出 Embedding 上下文限制的长文档时，自动切块分别 embedding，不会因为文档太长而失败或截断。

**⑧ Self-improvement 自我改进**
插件会在 Agent 对话重置（`/new`、`/reset`）前提醒记录本轮学到的内容，并在 Agent 重新启动时注入历史学习文件，让 Agent 的能力随使用积累而持续提升。

**与内置插件对比：**

| 能力 | 内置 `memory-lancedb` | `memory-lancedb-pro` |
|---|---|---|
| 向量检索 | ✅ | ✅ |
| BM25 全文检索 | ❌ | ✅ |
| 混合检索融合 | ❌ | ✅ |
| Cross-encoder 重排序 | ❌ | ✅ |
| 时间衰减 / 近期加权 | ❌ | ✅ |
| 噪声过滤 | ❌ | ✅ |
| 长度归一化 | ❌ | ✅ |
| MMR 多样性选择 | ❌ | ✅ |
| 多 Scope 隔离 | ❌ | ✅ |
| 长文档自动分块 | ❌ | ✅ |
| Self-improvement 自我改进 | ❌ | ✅ |

---

### 需要什么

| 依赖 | 说明 |
|---|---|
| OpenClaw | 已安装并能正常启动 Gateway |
| Node.js | 用于安装插件依赖 |
| Git | 用于 clone 插件仓库 |
| Jina API Key | 免费注册即可，用于 embedding 和重排序（也可替换为其他 OpenAI-compatible embedding 服务） |

### 三步完成安装

**第一步：clone 插件**

```bash
# macOS / Linux
git clone https://github.com/CortexReach/memory-lancedb-pro ~/.openclaw/plugins/memory-lancedb-pro
cd ~/.openclaw/plugins/memory-lancedb-pro && npm install

# Windows（PowerShell）
git clone https://github.com/CortexReach/memory-lancedb-pro $env:USERPROFILE\.openclaw\plugins\memory-lancedb-pro
cd $env:USERPROFILE\.openclaw\plugins\memory-lancedb-pro && npm install
```

**第二步：在 `openclaw.json` 里注册插件**

```json
"plugins": {
  "allow": ["memory-lancedb-pro"],
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
          "rerank": "cross-encoder",
          "rerankProvider": "jina",
          "rerankApiKey": "${JINA_API_KEY}",
          "rerankModel": "jina-reranker-v3"
        },
        "dbPath": "~/.openclaw/memory/lancedb-pro",
        "autoCapture": true,
        "autoRecall": true
      }
    }
  }
}
```

**第三步：重启 Gateway 验证**

```bash
openclaw gateway restart
openclaw plugins info memory-lancedb-pro   # 看到 status: loaded 即成功
```

### 插件提供的工具

Agent 安装后可直接调用以下工具：

| 工具 | 用途 |
|---|---|
| `memory_store` | 存储一条记忆 |
| `memory_recall` | 根据语义检索相关记忆 |
| `memory_update` | 更新已有记忆 |
| `memory_forget` | 删除指定记忆 |
| `self_improvement_log` | 记录自我改进日志 |

### 让 Agent 自动完成安装

不想手动操作？把这个 skill 丢给你的 Agent，让他照着做即可：

> 请阅读 skill 中的 `references/memory-lancedb-pro.md`，按照「安装方式」和「当前实际配置」章节，在本机完成 memory-lancedb-pro 插件的安装、配置和验证，完成后告诉我 `openclaw plugins info memory-lancedb-pro` 的输出结果。

Agent 会自动 clone 仓库、安装依赖、写入配置、重启 Gateway 并验证结果。

---

## 📝 开发者与社区

### 版本演进 (Changelog)

#### v1.6.0 (2026-03-12)

- **[新增] 经验提炼 bot / skill distill bot 工作流**
  - 新增 `references/experience-distill-bot.md`
  - 明确这套模式是 **OpenClaw 的运营工作流**，不是内置开关
  - 说明了它 **用来干嘛**：把 `main` 对话里的稳定经验沉淀成 skill / reference 草稿
  - 说明了它 **什么时候用**：当配置结论、排障结果、稳定流程值得长期复用时使用
  - 说明了它 **怎么用**：专门 agent + 专门 bot + 私有 skill + 人审后落库
  - 说明了它 **怎么发提示词**：固定输入“来源 / 主题 / 背景 / 最终结论 / 输出要求”
  - 说明了它 **相比之前的好处**：把零散聊天总结升级成结构化可审阅草稿，补齐了“主对话经验 → skill 沉淀”的闭环
  - 同时将这套模式接入 `SKILL.md` 主流程，并与 `references/bot-onboarding.md` 打通

#### v1.5.0 (2026-03-12)

- **[更新] official.md 同步至 OpenClaw v2026.3.11**
  - 补充 Gateway/WebSocket 安全修复
  - 补充 `openclaw doctor --fix` 对 legacy cron storage 的迁移要求
  - 补充 ACP `resumeSessionId`
  - 补充 `memorySearch` 对 `gemini-embedding-2-preview` 与多模态索引的支持
  - 补充 Ollama 新 onboarding 流程

#### v1.4.0 (2026-03-11)

- **[新增] memory-lancedb-pro 插件完整参考文档**
  - 新增 `references/memory-lancedb-pro.md`，首次完整收录该插件的配置与用法
  - 覆盖：GitHub 地址、安装方式、与内置插件的能力对比、完整 `openclaw.json` 配置示例、所有配置字段说明、可用工具列表
  - 新增每日自动更新 cron 任务说明（触发时机、升级流程、铁律同步逻辑、手动触发命令）
  - 新增诊断命令及常见故障模式（Cloudflare 403 特征识别、gateway/plugin 分层排查）
  - SKILL.md references 表新增对应条目

#### v1.3.0 (2026-03-11)

- **[优化] README 内容扩充**
  - 补充「具体功能」「重要亮点」「当前范围」章节，明确 skill 覆盖边界
  - 强调来自真实环境踩坑、结论可直接执行、本地与远端场景区分等核心定位

- **[同步] 当前本地 openclaw skill 全量同步**
  - 替换仓库内容为最新本地 `~/.codex/skills/openclaw`
  - 移除不再使用的旧版 provider 专属参考与脚本

#### v1.2.0 (2026-03-01)

- **[合并] 合入 win4r/OpenClaw-Skill 通用文档**
  - 将上游社区通用参考内容合并入本仓库
  - 保留本地定制配置，解决与上游文档的冲突

#### v1.1.0 (2026-02-26)

- **[修复] relay 模型白名单格式说明**
  - 明确 model whitelist map 格式，避免配置后 `/model` 命令显示异常

- **[更新] official.md 同步至 OpenClaw v2026.2.23**
  - 更新 v2026.2.23 版本 highlights

#### v1.0.0 (2026-02-22 ~ 2026-02-21)

- **[初始化] 仓库创建与基础内容建立**
  - 创建双语 README（中文优先）
  - 添加 403 账号重验流程协议（`references/relay-tools.md`）
  - 同步 official.md 至 OpenClaw v2026.2.21 / v2026.2.22
  - 建立持续更新策略说明
