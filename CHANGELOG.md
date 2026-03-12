# Changelog

## v1.6.0 (2026-03-12)

### 新增：经验提炼 bot / skill distill bot 工作流

这次新增的重点不是单个命令，而是一套 **可复用的 OpenClaw 运营工作流**：

- 把 `main` 对话里反复验证过的结论，从聊天消息里抽出来
- 交给一个专门的 `skill-distill` / `经验提炼 bot`
- 输出结构化 skill / reference 更新草稿
- 再由人工确认是否落进产品级 skill

### 这个能力是干嘛的

适合处理这类内容：

- 多次踩坑后才稳定下来的配置规则
- 某个 provider / bot / cron / plugin 的排障结论
- 一次对话里已经说清楚、但未来还会反复用到的经验
- 本来散落在聊天消息里、需要沉淀进 `SKILL.md` 或 `references/*.md` 的稳定做法

它的目标不是“再造一个会聊天的 bot”，而是：

- **把零散对话变成结构化知识**
- **把临时经验变成可复用规则**
- **把主 bot 的长期聊天沉淀成 skill 资产**

### 什么时候用

推荐在下面几种情况触发：

- `main` 对话刚刚解决了一个会反复出现的问题
- 某次排障已经形成明确结论，值得写入长期规则
- 某个流程已经验证稳定，准备变成标准操作
- 你希望把“这次经验”整理给 AI，而不是继续埋在聊天历史里

不推荐在下面这些情况直接用：

- 结论还没验证
- 只是临时想法
- 输入材料很碎、很乱、没有明确结论
- 你希望它无审核直接改 skill 文件

### 怎么用

推荐做法是：

1. 新建一个专门 agent（例如 `skill-distill`）
2. 给它绑定一个专门 bot
3. 给它单独 workspace
4. 给它一个只负责“经验提炼”的私有 skill
5. 手动把经验摘要发给它，让它输出结构化草稿

这套模式已经补进：

- `SKILL.md`
- `references/bot-onboarding.md`
- `references/experience-distill-bot.md`

### 怎么发给 AI 提示词

推荐输入格式：

```text
来源：main bot
主题：本次想沉淀的经验主题
背景：发生了什么问题
最终结论：
1. ...
2. ...
3. ...

请输出：
1. 是否值得写进 skill
2. 应写进 SKILL.md 还是 references/*.md
3. 最终文案草稿
4. 验证方式
5. 不确定项
```

### 和之前相比有什么好处

之前的问题是：

- 有建 bot 的流程
- 有多 agent 的流程
- 有记忆插件
- 但没有“**如何把主对话经验沉淀成 skill**”的完整闭环

这次补完之后的好处是：

- `经验提炼` 不再是零散想法，而是一条明确流程
- bot onboarding 和 distill bot 的关系被打通了
- AI 知道什么时候该走这条路，不再只能靠人工临时发挥
- skill 更新从“聊天总结”升级成“结构化草稿”
- 更适合长期维护产品级 skill，而不是靠记忆堆内容

### 变更文件

- `SKILL.md`
- `references/bot-onboarding.md`
- `references/experience-distill-bot.md`

## v1.5.0 (2026-03-12)

### 更新
- `references/official.md` 同步到 OpenClaw `v2026.3.11`
- 补充本次最值得操作层关注的变化：
  - Gateway/WebSocket origin 安全修复
  - `openclaw doctor --fix` 对 legacy cron storage 的迁移要求
  - ACP `resumeSessionId`
  - `memorySearch` 对 `gemini-embedding-2-preview` 与多模态索引的支持
  - Ollama 新 onboarding 流程

### 调整
- 更新 `SKILL.md` 中 release-check 段落的版本示例，从 `v2026.2.19` 改为 `v2026.3.11`

## v1.4.0 (2026-03-11)

### 新增
- 新增 `references/memory-lancedb-pro.md`：memory-lancedb-pro 插件完整参考文档
  - GitHub 地址：https://github.com/win4r/memory-lancedb-pro
  - 与内置 memory-lancedb 的能力对比（BM25、Hybrid 检索、Cross-encoder 重排序、时间衰减等）
  - 安装方式（git clone + npm install + load path 注册，非 plugins install）
  - 完整 `openclaw.json` 配置示例（含 Jina embedding、hybrid retrieval、rerank 全参数）
  - 所有配置字段说明及当前默认值
  - 可用工具列表（memory_recall / memory_store / memory_forget / memory_update / self_improvement_log）
  - 每日自动更新 cron 任务说明（触发时机、升级流程、铁律同步逻辑）
  - 诊断命令及常见故障模式

### 解决问题
- 此前 skill 中 memory-lancedb-pro 仅有 3 处零散提及，无法指导配置或排查问题
- 补全后 AI 可从 skill 直接获取插件安装、配置、工具使用和故障排查全流程

### 变更文件
- `SKILL.md` — references 表新增 memory-lancedb-pro 条目
- `references/memory-lancedb-pro.md` — 新增

---

## v1.3.0 (2026-03-11)

### 新增 / 优化
- README 补充「具体功能」「重要亮点」「当前范围」章节
- 明确 skill 覆盖边界，强调来自真实环境、结论可直接执行

### 变更文件
- `README.md` — 内容扩充
- 全量同步本地 `~/.codex/skills/openclaw`，移除旧版 provider 专属脚本

---

## v1.2.0 (2026-03-01)

### 合并
- 合入 win4r/OpenClaw-Skill 上游社区通用文档
- 保留本地定制配置，处理合并冲突

---

## v1.1.0 (2026-02-26)

### 修复
- 明确 relay 模型白名单（model whitelist map）格式，修复 `/model` 命令显示异常问题

### 更新
- `references/official.md` 同步至 OpenClaw v2026.2.23 highlights

---

## v1.0.0 (2026-02-21)

### 初始化
- 创建仓库，建立双语 README（中文优先 + English）
- 建立持续更新策略（只同步本地有效内容，不保留 key/token 等敏感信息）
- 添加 403 账号重验流程协议
- 同步 `references/official.md` 至 OpenClaw v2026.2.21 / v2026.2.22
