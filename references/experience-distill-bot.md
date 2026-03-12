# 经验提炼 bot / skill distill bot

> 这是一个 **运营模式 / 组织方式**，不是 OpenClaw 内置开关。
> 也就是说：OpenClaw 本身没有“自动把 main 对话变成 skill”的单一功能，但可以通过 **专门 agent + 专门 bot + 私有 skill + 手动或定时触发** 组成一条稳定流程。

## 适用场景

当你已经有一个主 bot（例如 `main`）长期对话、调参、排障、写配置时，常会出现这类需求：

- 把反复验证过的做法沉淀下来
- 把临时聊天里的经验提炼成长期规则
- 把“这次踩坑结论”写进 skill / reference，而不是继续散落在消息里

这时适合增加一个 **经验提炼 bot**（也可以叫 `skill-distill`、`经验整理 bot`、`经验归档 bot`）。

## 它能做什么

- 接收你贴给它的主对话内容、操作记录、结论摘要
- 提炼出：
  - 稳定做法
  - 配置规则
  - 排障结论
  - 新的验证流程
- 判断这些内容应放到：
  - `SKILL.md`
  - 某个 `references/*.md`
  - 单独的更新草稿
- 输出结构化的 skill 更新建议，而不是只给自然语言总结

## 它不能假装做到什么

以下能力 **不要在 skill 里写成默认已支持**：

- 自动读取所有 `main` 会话并无审批地改写 skill
- 自动从任意聊天消息直接生成可发布 skill 且保证正确
- 自动判断一条零碎对话就一定值得沉淀

这些都属于高风险动作。正确做法是：**显式提供输入，显式确认输出目标**。

## 推荐结构

### 1. 建一个专门 agent

示例：

- `agent_id`: `skill-distill`
- 默认模型：`codex/gpt-5.4` 或 `anthropic/claude-sonnet-4-6`
- 独立 workspace：`$HOME/.openclaw/workspace-skill-distill`

这个 agent 只做三件事：

1. 总结经验
2. 判断该写进哪个 skill/reference
3. 产出可审阅的更新草稿

### 2. 绑定一个专门 bot

给这个 agent 单独绑一个 Telegram bot / 频道账号。

这样做的好处：

- 跟主 bot 的日常对话隔离
- 输入更聚焦
- 不会把“执行任务”与“沉淀经验”混在一个 bot 里

### 3. 给它放私有 skill

私有 skill 路径建议：

```text
$HOME/.openclaw/workspace-skill-distill/skills/experience-distill/
```

再在该 agent 的配置里加入：

```json
"skills": ["experience-distill"]
```

这个私有 skill 的职责应该明确写死：

- 只接收已发生的对话 / 操作记录
- 只提炼“稳定、可复用”的经验
- 只输出结构化草稿，不直接发布

## 推荐输入格式

不要直接丢一句“你帮我整理一下”。建议固定成下面这种输入：

```text
来源：main bot
主题：memory-lancedb-pro 更新任务
背景：今天 10:00 cron 失败，原因是把 iron_zip 缺失当成 A 步硬失败
最终结论：
1. iron_zip 缺失本身不是失败条件
2. 只有本次变更确实包含 zip 且本地缺失，才允许失败
3. 当前更新任务模型为 codex/gpt-5.2

请输出：
1. 这条经验是否值得写进 skill
2. 应该写进 SKILL.md 还是 reference
3. 给出最终文案草稿
```

## 推荐输出格式

让它固定输出：

1. **是否沉淀**：是 / 否
2. **建议位置**：`SKILL.md` / `references/<name>.md`
3. **标题**
4. **新增或修改文案**
5. **验证方式**
6. **不确定项**

这样它产出的内容更像“变更提案”，而不是聊天总结。

## 是否要自动化

可以，但建议分层：

### 安全做法

- 主 bot 或你本人手动把对话摘要发给 `skill-distill` bot
- `skill-distill` 只输出草稿
- 人审后再改 skill 仓库

### 半自动做法

- 定时任务每天/每周提醒一次
- 由 `skill-distill` bot 读取你预先整理好的摘要文件
- 输出当天/当周应沉淀的经验项

### 不建议默认开启的做法

- 直接扫描主会话原始消息并自动改 skill 文件

这个风险太高，容易把噪声、误判和半成品写进产品级 skill。

## 最稳的落地原则

- **主 bot 负责干活**
- **distill bot 负责沉淀**
- **skill 更新必须可审阅**
- **没有明确输入，就不生成经验**
- **没有明确确认，就不落库/不改仓库**

## 与 memory-lancedb-pro 的关系

`memory-lancedb-pro` 可以帮你把“经验素材”留住，但它本身不是 skill 发布器。

更准确地说：

- `memory-lancedb-pro`：帮你记住对话内容和经验片段
- `skill-distill` bot：帮你把片段整理成结构化更新草稿
- 你的 skill 仓库：承接最终经过确认的沉淀结果

## 最小落地命令路径

如果你要手工做这套：

1. 新建 agent
2. 新建 bot
3. 绑定该 agent
4. 创建私有 skill
5. 用固定格式投喂经验摘要

其中第 1～3 步直接复用：

- `references/bot-onboarding.md`
- `references/multi_agent.md`

这个 reference 只补“经验提炼”这层产品模式，不重复 bot 接入基础流程。
