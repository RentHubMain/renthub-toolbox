---
name: renthub-commit
description: "按 RentHub Conventional Commits 规范生成并执行高质量提交。"
targets: ["*"]
---

# renthub-commit

## 适用场景

当用户要求“帮我 commit / 生成 commit message / 提交代码”时使用。

## 标准流程

1. 读取改动

```bash
git status
git diff --staged
git diff
```

2. 判断提交粒度

- 同一目的：单个 commit
- 多个目的：先拆分暂存，再逐个 commit

3. 生成 message

格式：

```text
<type>(<scope>): <subject>

<body 可选>
```

`type`：`feat|fix|refactor|chore|docs|test|style`

4. 用户确认后执行提交

```bash
git commit -m "<message>"
```

PowerShell 多行：

```powershell
git commit -m "type(scope): subject`n`nbody"
```

5. 返回结果

- 输出 commit hash、最终 message，并提醒按需 `git push`

## 规则

- `subject` **中文**，动词开头、简洁明确，避免空泛描述。
- `body` **中文**，仅解释“为什么”，不重复“做了什么”。
- 禁止 AI 署名或工具归因文案。
- 未经用户确认，不自动 commit。
