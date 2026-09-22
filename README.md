# Codex Skills

这里集中维护可复用的 Codex Skills。

## 当前技能

| Skill | 用途 |
| --- | --- |
| `development-work-sync` | 将开发对话整理为结构化工作记录，并同步到项目管理 API |
| `dingtalk-dws-integration` | 设计、验证和安全部署钉钉 DWS CLI 集成 |
| `it-admin-frontend-design-system` | 复用 IT 后台系统的布局、组件、颜色和 CSS 视觉规范 |
| `particle-star-map-ui` | 构建粒子星图式关系网络界面 |
| `project-handoff` | 生成项目交接摘要和可复制迁移提示词 |

每个技能目录都包含自己的 `SKILL.md`，并可能包含 `references/`、`scripts/`、`assets/` 和 `agents/openai.yaml`。

## 本地使用

将需要的技能目录放到 Codex 的用户级 Skill 目录，或按目标环境的 Skill 安装方式使用。显式调用示例：

```text
使用 $it-admin-frontend-design-system，按这套规范实现后台页面。
```

技能是否允许自动匹配由各目录的 `agents/openai.yaml` 和宿主配置决定。
