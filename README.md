# openclaw-graduate

> 🌐 语言切换：**中文（当前）** | [English](./README.en.md)

这个仓库保存当前在本地使用的 `openclaw` skill，聚焦 OpenClaw 的安装、升级、模型 provider 配置、channels、multi-agent、relay/codex/Claude 切换、远端 Codespaces 部署与常见故障排查。

## 仓库内容

- `SKILL.md`：主技能说明
- `references/`：分主题操作参考
- `scripts/`：配套脚本
- `assets/`：技能附带素材

## 当前范围

- OpenClaw 安装、升级、Gateway 运维
- Telegram / WhatsApp / Slack 等 channel 配置
- 模型 provider 配置与切换
- 远端 Codespaces / github.dev 部署与诊断
- 常见故障排查：403/429、错模型、不回复、session 锁、插件注册异常

## 更新原则

- 只同步当前本地 `~/.codex/skills/openclaw` 的有效内容
- 提交前不保留真实 key / token / chat id 等敏感信息
