# openclaw-antigravity-skill

> 🌐 语言切换：**中文（当前）** | [English](./README.en.md)

这是一个面向实战的 OpenClaw + Antigravity Tools 技能仓库，目标是让多 Bot 场景下的配置、运维与排障可复制、可验证、可持续迭代。

## 这个 Skill 用来做什么

- 稳定配置与运维 OpenClaw 的 agents/channels。
- 新增或更新 Telegram Bot，并绑定正确的 agent / model。
- 维护 Antigravity 模型目录与 `/model` 可选项行为。
- 运行可靠的 cron 工作流（采集、汇总、投递）。
- 快速排障：模型错路由、不回复、403/429、warmup 混淆、投递失败等。

## 仓库结构

- `SKILL.md`：主流程与操作规范。
- `references/official.md`：OpenClaw 官方行为与命令参考。
- `references/antigravity-tools.md`：Antigravity Tools 实操与排障补充。
- `references/antigravity-models.md`：Antigravity 模型与同步规则。
- `references/bot-onboarding.md`：Bot 接入参考说明。
- `scripts/provision_telegram_bot.py`：Bot 一键接入脚本。
- `scripts/sync_antigravity_models.py`：模型目录同步脚本。

## 什么时候补充新内容

这个仓库是**持续维护**的：会随着 OpenClaw 与 Antigravity Tools 的版本更新进行例行检查。  
但只在出现**可操作能力变化**时补充，核心是写清楚“新功能怎么用”。

1. OpenClaw 出现新能力（新命令、新配置入口、新工作流）时，补充具体用法、配置步骤、验证方法。
2. Antigravity Tools 出现新能力（影响模型选择、反代调用、账号调度、路由/warmup 规则）时，补充规则、步骤和注意事项。
3. 旧流程因版本变化失效时，替换为新流程，并标注失效原因与迁移方式。

## 什么时候不补充

以下情况默认不补充到 skill（除非会改变实际操作结论）：

- 纯 bug 修复
- 纯性能/稳定性优化
- UI 微调、文案变更
- 不改变操作流程的安全补丁说明

## 更新策略（OpenClaw + Antigravity）

当满足补充条件时，按“可落地执行”标准补充：

1. 改了什么、会影响谁、在什么场景会触发。
2. 如何使用（命令 + 配置路径 + 必要参数/前置条件）。
3. 如何验证成功（日志/状态/输出 + 失败信号）。
4. 写到哪里（`SKILL.md` 与对应 `references/*`），并在 `CHANGELOG.md` 记录一次变更。
5. 内容取向：优先补“新功能怎么用”，不堆叠无操作价值的信息。

## 安全规则

- 禁止提交真实 token / API key / chat id / 凭证。
- 只保留占位符（如 `<bot_token>`、`<api_key>`）。
- 示例里若出现敏感信息，提交前必须脱敏。

## Changelog 规则

`CHANGELOG.md` 只记录对操作者有价值的变更：

- 新增可操作能力
- 现有流程调整
- 排障流程新增或修正

纯样式/文案修改可不记。
