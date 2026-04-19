---
name: finishing-a-development-branch
description: 实现已完成、测试全绿，需要选择如何合并、开 PR 或清理分支时使用；通过结构化选项引导收尾。
targets:
  - '*'
---
# 收尾开发分支

在开发工作完成后，通过清晰选项引导用户选择工作流并执行所选路径。

**核心原则：** 先验证测试 → 再呈现选项 → 执行选择 → 最后清理。

**开场说明：** 「我正在使用收尾开发分支（finishing-a-development-branch）技能来完成本次工作。」

## 流程

### 第 1 步：验证测试

**在呈现任何选项之前，确认测试通过：**

```bash
# 运行项目测试套件（择一或替换为项目实际命令）
npm test / cargo test / pytest / go test ./...
```

**若测试失败：**

```text
当前有 <N> 个测试失败，必须先修复后才能继续收尾：

[展示失败信息]

在测试全绿之前，不得进行 merge / PR 等后续步骤。
```

停止，不要进入第 2 步。

**若测试通过：** 进入第 2 步。

### 第 2 步：确定基准分支（base）

```bash
# 尝试常见基准分支
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或询问用户：「本分支是从 main 拉出的吗？」（按项目实际主分支名调整。）

### 第 3 步：呈现选项

**只呈现以下 4 个选项，措辞保持简短：**

```text
实现已完成。接下来希望怎么做？

1. 在本地合并回 <base-branch>
2. push 并创建 Pull Request
3. 先保留本分支（稍后自行处理）
4. 丢弃本次工作

请选择 1–4。
```

**不要**在选项块外加长段解释。

### 第 4 步：执行选择

#### 选项 1：本地合并

```bash
# 切换到基准分支
git checkout <base-branch>

# 拉取最新
git pull

# 合并功能分支
git merge <feature-branch>

# 在合并结果上再跑测试
<test 命令>

# 若测试通过
git branch -d <feature-branch>
```

然后：执行第 5 步（清理 worktree）。

#### 选项 2：push 并创建 PR

```bash
# 推送分支
git push -u origin <feature-branch>

# 创建 PR（示例使用 GitHub CLI）
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2–3 条变更要点>

## Test Plan
- [ ] <验证步骤>
EOF
)"
```

然后：执行第 5 步（清理 worktree）。

#### 选项 3：原样保留

回复用户：「已保留分支 <name>。工作区路径：<path>。」

**不要**清理 worktree。

#### 选项 4：丢弃

**先确认：**

```text
以下将被永久删除：
- 分支 <name>
- 其上的全部提交：<commit-list>
- 位于 <path> 的 worktree

请键入 discard（全小写）以确认。
```

等待用户 **完全按上述字面** 确认。

若已确认：

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然后：执行第 5 步（清理 worktree）。

### 第 5 步：清理 worktree

**对选项 1、2、4：**

检查是否处于 worktree：

```bash
git worktree list | grep $(git branch --show-current)
```

若是：

```bash
git worktree remove <worktree-path>
```

**对选项 3：** 保留 worktree。

## 速查表

| 选项 | 本地合并 | push | 保留 worktree | 清理分支 |
|------|----------|------|---------------|----------|
| 1. 本地合并 | ✓ | — | — | ✓ |
| 2. 创建 PR | — | ✓ | ✓ | — |
| 3. 原样保留 | — | — | ✓ | — |
| 4. 丢弃 | — | — | — | ✓（强制） |

## 常见错误

**跳过测试验证**

- **问题：** 合并了坏代码或开出失败的 PR。
- **纠正：** 永远在给出选项前先确认测试通过。

**开放式提问**

- **问题：**「接下来干啥？」→ 意图不明。
- **纠正：** 始终只给出上述 **4 个** 结构化选项。

**自动清理 worktree**

- **问题：** 在选项 2、3 仍可能需要 worktree 时误删。
- **纠正：** 仅对选项 **1** 和 **4** 做清理（见第 5 步说明）。

**丢弃前无确认**

- **问题：** 误删工作成果。
- **纠正：** 选项 4 必须要求用户键入 `discard` 确认。

## 红灯 — 禁止行为

**绝不：**

- 在测试仍失败时继续收尾；
- 未在合并结果上验证测试就宣称完成；
- 未经确认删除工作；
- 未经用户明确要求进行 force-push。

**务必：**

- 给出选项前先验证测试；
- 始终只呈现 4 个选项；
- 选项 4 必须取得键入确认；
- 仅对选项 1 与 4 清理 worktree。

## 与其他流程的衔接

**可能被调用方：**

- **subagent-driven-development**（第 7 步）— 全部任务完成后；
- **executing-plans**（第 5 步）— 全部批次完成后。

**常配合：**

- **using-git-worktrees** — 清理由该技能创建的工作树。
