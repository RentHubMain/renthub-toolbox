---
name: rh-sup-using-git-worktrees
description: 在开始需要与工作区隔离的功能开发，或在执行实现计划之前使用；通过目录优先级与安全校验创建隔离的 git worktree。
targets:
  - '*'
---
# 使用 Git Worktrees（Using Git Worktrees）

## 概述

Git worktree 在**同一仓库**下创建隔离工作区，可在多分支上同时工作而无需反复 `checkout` 切换。

**核心原则：** 系统化选择目录 + 安全校验 = 可靠隔离。

**开始时声明：**「我正在使用 using-git-worktrees 技能来建立隔离工作区。」

## 目录选择流程

按以下**优先级**执行：

### 1. 检查已有目录

```bash
# 按优先级检查
ls -d .worktrees 2>/dev/null     # 首选（隐藏）
ls -d worktrees 2>/dev/null      # 备选
```

**若存在：** 使用该目录。若两者都存在，**`.worktrees` 优先**。

### 2. 检查 CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**若写明偏好：** 直接使用，不必再问。

### 3. 询问用户

若既无目录也无 CLAUDE.md 偏好：

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## 安全校验

### 项目本地目录（`.worktrees` 或 `worktrees`）

**创建 worktree 之前必须确认目录已被忽略：**

```bash
# 检查是否被忽略（尊重本地、全局与系统 gitignore）
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**若未被忽略：**

按「坏了就立刻修」：

1. 在 `.gitignore` 中加入合适规则
2. 提交该变更
3. 再继续创建 worktree

**为何关键：** 避免误把 worktree 内容提交进仓库。

### 全局目录（`~/.config/superpowers/worktrees`）

完全在项目外，**无需** `.gitignore` 校验。

## 创建步骤

### 1. 检测项目名

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建 Worktree

```bash
# 确定完整路径
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# 新建分支并添加 worktree
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目安装

自动检测并执行合适安装：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 校验干净基线

运行测试，确认 worktree 从干净状态开始：

```bash
# 示例 — 换用项目实际命令
npm test
cargo test
pytest
go test ./...
```

**若测试失败：** 汇报失败，询问是否继续或先调查。

**若测试通过：** 汇报就绪。

### 5. 汇报位置

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 速查

| 情况 | 动作 |
|------|------|
| 存在 `.worktrees/` | 使用（并确认已忽略） |
| 存在 `worktrees/` | 使用（并确认已忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 都不存在 | 查 CLAUDE.md → 问用户 |
| 目录未忽略 | 写 `.gitignore` 并提交 |
| 基线测试失败 | 汇报失败并询问 |
| 无 package.json/Cargo.toml 等 | 跳过依赖安装 |

## 常见错误

### 跳过忽略校验

- **问题：** worktree 内容被跟踪，污染 `git status`
- **修复：** 项目本地 worktree 创建前**永远**跑 `git check-ignore`

### 假定目录位置

- **问题：** 不一致，违背项目约定
- **修复：** 遵守优先级：已有 > CLAUDE.md > 询问

### 测试失败仍硬上

- **问题：** 无法区分新 bug 与历史问题
- **修复：** 汇报失败，取得**明确**许可再继续

### 写死安装命令

- **问题：** 换工具栈就坏
- **修复：** 根据 `package.json` 等文件自动检测

## 示例工作流

```
你：我正在使用 using-git-worktrees 技能建立隔离工作区。

[检查 .worktrees/ — 存在]
[校验已忽略 — git check-ignore 确认 .worktrees/ 被忽略]
[创建：git worktree add .worktrees/auth -b feature/auth]
[运行 npm install]
[运行 npm test — 47 通过]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## 红线

**绝不：**

- 未校验「已忽略」就创建（项目本地）worktree
- 跳过基线测试验证
- 测试失败仍不问就继续
- 位置含糊时自作主张
- 跳过 CLAUDE.md 检查

**务必：**

- 遵守目录优先级：已有 > CLAUDE.md > 问
- 项目本地路径必须已忽略
- 自动检测并执行项目安装
- 校验干净测试基线

## 衔接

**由谁调用：**

- **`rh-sup-brainstorming`**（阶段 4）— 设计获批且将实施时 **必选**
- **`rh-sup-subagent-driven-development`** — 执行任务前 **必选**
- **`rh-sup-executing-plans`** — 执行任务前 **必选**
- 任何需要隔离工作区的技能

**常与谁配合：**

- **`rh-sup-finishing-a-development-branch`** — 工作完成后清理 worktree **必选**
