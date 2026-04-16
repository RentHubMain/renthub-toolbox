# RentHub Rulesync Toolbox

> 虽然每个人都希望可以一直使用一种 AI 工具，但是现实情况是开发过程中不可避免地需要切换或并用多个 AI。问题在于，不同工具有不同的约束文件和格式（例如 Copilot、Codex CLI、Claude Code、Cursor）。
>
> Rulesync 的价值，就是把这些分散的约束入口统一起来：只维护一套声明式源文件，然后为不同工具自动生成各自需要的配置。

## 1) Rulesync 是什么

Rulesync 是一个“AI 约束与上下文同步器”：

- 单一事实源（Single Source of Truth）：规则写一次，多工具复用。
- 多工具适配：将统一规则转换成各 AI 工具原生可识别的配置格式。
- 可审计输出：生成的是普通文本文件，可提交、可评审、可追踪。
- 模块化特性：可按需同步 rules、ignore、mcp、commands、subagents、skills、hooks。

参考官方文档：

- Installation: https://rulesync.dyoshikawa.com/getting-started/installation.html
- Quick Start: https://rulesync.dyoshikawa.com/getting-started/quick-start.html
- Why Rulesync: https://rulesync.dyoshikawa.com/guide/why-rulesync.html

## 2) 为什么需要 Rulesync

当团队同时使用 Copilot / Cursor / Claude / Codex CLI 等工具时，如果不用 Rulesync，通常会遇到：

- 规则重复维护：同一套规范要在多个文件里手工复制。
- 漂移与不一致：某个工具更新了，另一个忘记改，导致行为不一致。
- 新人上手慢：要学多套工具配置位置与格式。
- 工具切换成本高：更换助手时要重写约束。

Rulesync 解决方式：

- 把“团队规范”从“工具格式”里解耦。
- 统一在 .rulesync 下维护源文件。
- 通过 `rulesync generate` 面向目标工具输出最终配置。

## 3) 当前仓库的 Rulesync 资产（只看 Rulesync）

### 配置入口

- `rulesync.jsonc`
	- targets: `copilot`, `cursor`, `claudecode`, `codexcli`
	- features: `rules`, `ignore`, `mcp`, `commands`, `subagents`, `skills`, `hooks`
	- baseDirs: `.`
	- delete: `true`（生成时删除过期目标文件）
	- gitignoreTargetsOnly: `true`

### 目录结构与内容

- `.rulesync/.aiignore`
	- 统一忽略规则源。

- `.rulesync/rules/`
	- `overview.md`
	- `renthub-admin-project-guide.md`
	- `renthub-docs-project-guide.md`
	- `renthub-mini-project-guide.md`
	- `renthub-website-project-guide.md`

- `.rulesync/mcp.json`
	- 当前 `mcpServers` 为空对象（已预留 MCP 声明入口）。

- `.rulesync/commands/`
	- `review-pr.md`

- `.rulesync/subagents/`
	- `planner.md`

- `.rulesync/skills/`
	- `legal-version-release/`
	- `renthub-commit/`
	- `ui-ux-pro-max/`

- `.rulesync/hooks.json`
	- 当前 `hooks` 为空对象（已预留 Hook 声明入口）。

## 4) RentHub Toolbox 用法（Rulesync Edition）

### A. 安装

```bash
npm install -g rulesync
# 或
brew install rulesync

rulesync --version
rulesync --help
```

### B. 日常工作流

```bash
# 1) 修改 .rulesync 下的源文件（rules/skills/commands 等）

# 2) 生成目标工具配置（当前仓库常用）
rulesync generate --targets copilot --features skills

# 3) 或一次性生成所有目标 + 所有特性
rulesync generate --targets "*" --features "*"
```

### C. 从已有工具配置回收为统一源（可选）

```bash
rulesync import --targets claudecode
rulesync import --targets cursor
rulesync import --targets copilot
rulesync import --targets claudecode --features rules,mcp,commands,subagents
```

### D. 新项目初始化（可选）

```bash
rulesync init
rulesync fetch dyoshikawa/rulesync --features skills
```

## 5) 一句话总结

Rulesync 在 RentHub 的角色是：

“把多 AI 工具时代的约束管理，收敛为一个可维护、可审计、可迁移的统一工具箱。”
