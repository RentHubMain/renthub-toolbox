---
name: rh-sup-requesting-code-review
description: 在完成任务、实现较大功能或合并前，用于验证工作是否符合要求时使用。
targets:
  - '*'
---
# 请求代码评审（Requesting Code Review）

派发 **code-reviewer** 子代理，在问题扩散前拦截缺陷。评审者只获得精心裁剪的上下文 —— **绝不**塞入本会话历史。这样评审者聚焦工作产物，而非你的思路，你也保留语境继续干活。

**核心原则：** 早评审、勤评审。

## 何时请求评审

**必须：**

- **子代理驱动开发**中每个任务之后
- 完成较大功能之后
- 合并进 main 之前

**可选但很有价值：**

- 卡住时（换视角）
- 重构前（基线检查）
- 修完复杂缺陷后

## 如何请求

**1. 取得 git SHA：**

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派发 code-reviewer 子代理：**

使用 Task 工具，按本目录下 **`code-reviewer.md`** 模板填写。

**占位符：**

- `{WHAT_WAS_IMPLEMENTED}` — 你刚做了什么
- `{PLAN_OR_REQUIREMENTS}` — 应该达成什么
- `{BASE_SHA}` — 起始提交
- `{HEAD_SHA}` — 结束提交
- `{DESCRIPTION}` — 简短摘要

**3. 处理反馈：**

- **Critical** — 立即修
- **Important** — 继续前修掉
- **Minor** — 记下稍后
- 评审错了就反驳（附理由）

## 示例

```
[刚完成 Task 2：添加校验函数]

你：先请求代码评审再继续。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[派发 code-reviewer 子代理]
  WHAT_WAS_IMPLEMENTED: 会话索引的校验与修复函数
  PLAN_OR_REQUIREMENTS: docs/superpowers/plans/deployment-plan.md 的 Task 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: 新增 verifyIndex()、repairIndex()，覆盖 4 类问题

[子代理返回]：
  优点：结构清晰、有真实测试
  问题：
    Important: 缺进度提示
    Minor: 上报间隔魔数 100
  结论：可继续

你：[补上进度提示]
[进入 Task 3]
```

## 与工作流衔接

**子代理驱动开发：**

- **每个**任务后评审
- 在问题叠加前拦截
- 修完再进下一任务

**执行计划：**

- 每批（如 3 个任务）后评审
- 吸收反馈再继续

**临时开发：**

- 合并前评审
- 卡住时评审

## 红线

**绝不：**

- 因「很简单」跳过评审
- 忽略 **Critical**
- **Important** 未修就继续
- 对有效技术反馈抬杠

**若评审有误：**

- 用技术理由反驳
- 用代码/测试证明可行
- 请求澄清

模板路径：`requesting-code-review/code-reviewer.md`（相对本技能包目录）。
