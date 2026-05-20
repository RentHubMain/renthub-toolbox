# RentHub Toolbox

> RentHub 团队在 Cursor、Claude Code、Codex、Copilot 等 AI 工具上共用一套 **Agent Skills**、规则与命令。本仓库是这些约定的**单一源码**，通过 [skills CLI](https://github.com/vercel-labs/skills) 安装到各工具。

## 快速开始：安装 Skills

在**你的业务项目根目录**（例如 `renthub-admin-panel/`）执行：

```bash
npx skills add RentHubMain/renthub-toolbox
```

CLI 会检测本机已安装的 AI 工具，将 `skills/` 下的技能包安装到对应目录（如 Cursor 的 `.agents/skills/`、Claude Code 的 `.claude/skills/` 等）。交互过程中可选择：

- **安装范围**：项目内（默认，便于团队共享）或全局（`-g`）
- **安装方式**：符号链接（推荐，便于 `npx skills update`）或复制（`--copy`）

### 常用命令

**列出本仓库提供的技能（不安装）：**
```bash
npx skills add RentHubMain/renthub-toolbox --list
```

**只安装指定技能：**
```bash
npx skills add RentHubMain/renthub-toolbox --skill renthub-commit --skill rh-sup-brainstorming
```

**指定目标工具（例如 Cursor）：**
```bash
npx skills add RentHubMain/renthub-toolbox -a cursor
```

**非交互安装（CI / 脚本）：**
```bash
npx skills add RentHubMain/renthub-toolbox -y
```

**更新已安装技能：**
```bash
npx skills update
```

**查看已安装技能：**
```bash
npx skills list
```

安装后会在项目根生成 `skills-lock.json`（本地锁文件，已纳入本仓库 `.gitignore`，勿提交）。

更多选项见 [vercel-labs/skills](https://github.com/vercel-labs/skills) 文档。

## 本仓库结构

| 路径 | 说明 |
|------|------|
| **`skills/`** | Agent Skills 源码，入口为各子目录下的 `SKILL.md` |
| **`rules/`** | 各子项目指南（overview、admin、docs、mini、website） |
| **`commands/`** | 自定义命令（如 `review-pr.md`） |
| **`subagents/`** | 子代理定义（如 `planner.md`） |

`skills/` 由 `npx skills add` 自动分发；`rules/`、`commands/`、`subagents/` 目前需在对应工具中按需引用或手动配置（各客户端路径不同）。

## Agent Skills（`skills/`）

Skills 是写给 **AI 代理** 的操作说明：何时启用、按什么步骤做、有哪些硬约束。  
**源码目录**：`skills/<skill 文件夹>/`，入口为 **`SKILL.md`**。

**你怎么用：**

1. **安装**：`npx skills add RentHubMain/renthub-toolbox`（见上文）。
2. **在对话里引用**：在支持 `@` 的客户端中，可 `@` 已安装路径下的 `SKILL.md`，让当前会话按该 skill 执行。
3. **人工阅读**：直接打开本仓库 `skills/.../SKILL.md` 了解流程。

以下为 **RentHub 当前内置技能**（YAML `name` 与目录名一致）。

### RentHub 业务技能（`renthub-*`）

| 技能 | 何时用 |
|------|--------|
| **`renthub-commit`** | 按 Conventional Commits 起草中文提交说明并确认后提交 |
| **`renthub-legal-version-release`** | `renthub-docs/legal/` 协议发版、归档与导航更新 |
| **`renthub-ui-ux-pro-max`** | UI/UX 设计系统检索与实现要点（Web/移动端） |

### Superpowers 流程技能（`rh-sup-*`）

| 技能 | 何时用 |
|------|--------|
| **`rh-sup-using-superpowers`** | 每次对话开始时：发现与加载相关技能 |
| **`rh-sup-brainstorming`** | 新功能/改行为前的创意与规格澄清 |
| **`rh-sup-writing-plans`** | 有多步需求、尚未写代码时撰写实现计划 |
| **`rh-sup-executing-plans`** | 在单独会话中按检查点执行书面计划 |
| **`rh-sup-subagent-driven-development`** | 本会话中执行彼此独立的实现任务 |
| **`rh-sup-dispatching-parallel-agents`** | 2 个以上可并行、无共享状态的任务 |
| **`rh-sup-test-driven-development`** | 实现功能或修 bug 前：红→绿→重构 |
| **`rh-sup-systematic-debugging`** | 缺陷/测试失败：先根因再修复 |
| **`rh-sup-verification-before-completion`** | 声称完成前必须跑验证命令 |
| **`rh-sup-requesting-code-review`** | 完成功能或合并前请求评审 |
| **`rh-sup-receiving-code-review`** | 收到评审意见后落实建议 |
| **`rh-sup-finishing-a-development-branch`** | 实现完成、测试通过后决定合并/PR |
| **`rh-sup-using-git-worktrees`** | 需要与工作区隔离的功能开发 |
| **`rh-sup-writing-skills`** | 新建或编辑 Agent Skill |

各技能细节见对应 `skills/<name>/SKILL.md`。

## 维护本仓库

在 **RentHub Toolbox 仓库根目录** 修改 `skills/` 后，推送到 `RentHubMain/renthub-toolbox`；业务项目内执行 `npx skills update` 即可拉取更新。

```bash
# 在业务项目中更新来自本仓库的技能
npx skills update
```

## 文本编码与乱码排查

仓库中文文档应为 **UTF-8**。若在编辑器里看到 **U+FFFD 替换符**、问号方块或「汉字变西欧符号」，常见原因是文件曾被存成 **GBK** 或 UTF-8 被破坏。

- **检查**：在项目根执行  
  `python scripts/check_text_encoding.py`  
  可列出非 UTF-8 文件、含 Unicode 替换字节（U+FFFD）的路径、以及仍使用 CRLF 的文本文件（默认跳过 `node_modules`、`miniprogram_npm` 等）。
- **换行**：`python scripts/check_text_encoding.py --fix-crlf` 将扫描到的文本改为 LF（会改写文件，建议先提交或备份）。
- **GBK → UTF-8**：若确认某 `.md` / `.txt` 实为 GBK 编码，可用  
  `python scripts/check_text_encoding.py --try-gbk-to-utf8`  
  尝试转写为 UTF-8（**有误判风险**，务必先 Git 备份）。
- **根目录 `README.md`**：若曾被以 ANSI/GBK 保存，可执行  
  `python scripts/check_text_encoding.py --repair-readme`  
  将其规范为 UTF-8（LF）；等价于用编辑器「另存为 UTF-8」。

## 一句话总结

**RentHub Toolbox**：在 GitHub 上维护统一的 Agent Skills 与配套约定；业务项目用 **`npx skills add RentHubMain/renthub-toolbox`** 安装，用 **`npx skills update`** 保持同步。
