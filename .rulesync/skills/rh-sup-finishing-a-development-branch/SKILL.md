---
name: rh-sup-finishing-a-development-branch
description: 在实现已完成、测试全绿，需要决定如何合并、开 PR 或清理分支时使用；通过结构化选项引导收尾。
targets:
  - '*'
---
# 收尾开发分支（Finishing a Development Branch）

## 概述

通过展示清晰选项并执行所选工作流，引导开发工作收尾。

**核心原则：** 验证测试 → 展示选项 → 执行选择 → 清理。

**开始时声明：**「我正在使用 finishing-a-development-branch 技能来完成本工作。」

## 流程

### 步骤 1：验证测试

**在展示选项之前，确认测试通过：**

```bash
# 运行项目测试套件
npm test / cargo test / pytest / go test ./...
```

**若测试失败：**

```
Tests failing (<N> failures). Must fix before completing:

[展示失败信息]

在测试通过前不得继续合并/PR。
```

停止。不要进入步骤 2。

**若测试通过：** 进入步骤 2。

### 步骤 2：确定基线分支

```bash
# 尝试常见基线分支
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或询问：「本分支从 main 分出 — 是否正确？」

### 步骤 3：展示选项

**仅**展示以下 **4** 个选项：

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**不要附加解释** — 保持选项简短。

### 步骤 4：执行选择

#### 选项 1：本地合并

```bash
# 切换到基线分支
git checkout <base-branch>

# 拉取最新
git pull

# 合并功能分支
git merge <feature-branch>

# 在合并结果上验证测试
<test command>

# 若测试通过
git branch -d <feature-branch>
```

然后：清理 worktree（步骤 5）

#### 选项 2：推送并创建 PR

```bash
# 推送分支
git push -u origin <feature-branch>

# 创建 PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

然后：清理 worktree（步骤 5）

#### 选项 3：保持现状

汇报：「保留分支 `<name>`。Worktree 保留在 `<path>`。」

**不要**清理 worktree。

#### 选项 4：丢弃

**先确认：**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待用户**准确**输入确认。

若已确认：

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然后：清理 worktree（步骤 5）

### 步骤 5：清理 Worktree

**对选项 1、2、4：**

检查是否在 worktree 中：

```bash
git worktree list | grep $(git branch --show-current)
```

若是：

```bash
git worktree remove <worktree-path>
```

**对选项 3：** 保留 worktree。

## 速查

| 选项 | 合并 | 推送 | 保留 Worktree | 清理分支 |
|------|------|------|---------------|----------|
| 1. 本地合并 | ✓ | - | - | ✓ |
| 2. 创建 PR | - | ✓ | ✓ | - |
| 3. 保持现状 | - | - | ✓ | - |
| 4. 丢弃 | - | - | - | ✓（强制） |

## 常见错误

**跳过测试验证**

- **问题：** 合并坏代码、创建失败 PR
- **修复：** 提供选项前始终验证测试

**开放式提问**

- **问题：**「接下来做什么？」→ 含糊
- **修复：** 恰好展示 4 个结构化选项

**自动清理 worktree**

- **问题：** 在仍需要时删除 worktree（选项 2、3）
- **修复：** 仅对选项 1 和 4 清理

**丢弃无确认**

- **问题：** 误删工作
- **修复：** 要求键入 `discard` 确认

## 红线

**绝不：**

- 测试失败仍继续
- 合并不在结果上验证测试
- 无确认删除工作
- 未经明确要求 force-push

**务必：**

- 提供选项前验证测试
- 恰好展示 4 个选项
- 选项 4 需键入确认
- 仅对选项 1 与 4 清理 worktree

## 衔接

**由谁调用：**

- **`rh-sup-subagent-driven-development`**（流程末步）— 全部任务完成后
- **`rh-sup-executing-plans`**（步骤 5）— 全部批次完成后

**常与谁配合：**

- **`rh-sup-using-git-worktrees`** — 清理由该技能创建的 worktree
