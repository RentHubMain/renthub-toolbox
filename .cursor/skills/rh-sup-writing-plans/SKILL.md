---
name: rh-sup-writing-plans
description: 在有多步任务的书面规格或需求、且尚未改代码时使用。
---
# 编写实现计划（Writing Plans）

## 概述

编写**完整**的实现计划，假定工程师对你们代码库**零语境**且品味可疑。写清他们需要的全部信息：每个任务要动哪些文件、示例代码、如何测试、可能要查的文档。把整件事拆成可一口吃掉的小步。DRY、YAGNI、TDD、频繁提交。

假定他们是熟练开发者，但几乎不了解你们的工具链与问题域，也不太懂好的测试设计。

**开始时声明：**「我正在使用 writing-plans 技能来编写实现计划。」

**语境：** 宜在独立 worktree 中运行（由脑暴等流程创建）。

**计划保存路径：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`  
（若用户指定其他位置，以用户偏好为准。）

## 范围检查

若规格覆盖多个**彼此独立**的子系统，应在脑暴阶段已拆成子规格。若未拆分，建议拆成**多份计划** —— 每个子系统一份；每份计划单独应能产出可运行、可测试的软件。

## 文件结构

在拆任务之前，先列出将**创建/修改**的文件及各自职责。分解决策在此锁定。

- 边界清晰、接口明确的单元；每个文件职责单一。
- 你能一次记在脑子里的代码最好推理；文件越小越聚焦，改动越可靠。
- **一起变的文件放一起**；按职责拆分，不要按技术层硬拆。
- 在既有仓库里遵循既有模式；若仓库习惯大文件，不要单方面大重构 —— 但若你正在改的文件已臃肿，在计划里包含拆分是合理的。

该结构决定任务分解；每个任务应产生**自成一体**、单独也说得通的变更。

## 任务粒度

**每一步是一个动作（约 2～5 分钟）：**

- 「写失败测试」— 一步  
- 「运行并确认失败」— 一步  
- 「写最少实现使测试通过」— 一步  
- 「再跑测试确认全绿」— 一步  
- 「提交」— 一步  

## 计划文档头部

**每份计划必须以如下头部开头：**

```markdown
# [功能名] 实现计划

> **面向代理执行者：** 必选子技能：使用 **`rh-sup-subagent-driven-development`**（推荐）或 **`rh-sup-executing-plans`**，按任务逐项实施。步骤使用 `- [ ]` 复选框跟踪。

**目标：** [一句话说明要做出什么]

**架构：** [2～3 句说明做法]

**技术栈：** [主要技术/库]

---
```

## 任务结构

````markdown
### Task N：[组件名]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1：写失败测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2：运行测试确认失败**

Run: `pytest tests/path/test.py::test_name -v`  
Expected: FAIL，且信息含「function not defined」等预期原因

- [ ] **Step 3：写最少实现**

```python
def function(input):
    return expected
```

- [ ] **Step 4：运行测试确认通过**

Run: `pytest tests/path/test.py::test_name -v`  
Expected: PASS

- [ ] **Step 5：提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 禁止占位

每一步都必须包含工程师**真正需要**的内容。下列属于**计划失败**，禁止出现：

- `TBD`、`TODO`、`implement later`、`fill in details`
- 「加合适错误处理」「加校验」「处理边界」等空话
- 「为上面写测试」却**不给**具体测试代码
- 「与 Task N 类似」（工程师可能乱序读任务 —— **重复写出**所需代码）
- 只写做什么、不写怎么做（涉及代码的步骤**必须有**代码块）
- 引用未在任何任务中定义的类型、函数或方法

## 牢记

- 路径永远写全、写准  
- 凡改代码的步骤都要有**完整**代码块  
- 命令写全，并写清**期望输出**  
- DRY、YAGNI、TDD、频繁提交  

## 自检

写完整份计划后，用新眼光对照规格自检（由你自己执行，**不要**派子代理代劳）。

**1. 规格覆盖：** 扫一遍规格每节/每条需求，能否指到**具体任务**？列出缺口。  
**2. 占位扫描：** 全文搜「TBD」「TODO」「稍后」等，按上一节规则改掉。  
**3. 命名一致：** 后文出现的函数名、类型、属性是否与前面任务一致？Task 3 叫 `clearLayers()`、Task 7 却叫 `clearFullLayers()` 就是 bug。

发现问题就内联修改；不必整套重审。若某条规格无任务承接，**补任务**。

## 执行交接

保存计划后，向执行方提供选择：

**「计划已保存至 `docs/superpowers/plans/<filename>.md`。两种执行方式：**

**1. 子代理驱动（推荐）** — 每任务新子代理，任务间复核，迭代快  

**2. 本会话串行** — 在本会话用 **`rh-sup-executing-plans`** 批量执行并设检查点  

**选哪一种？」**

**若选子代理驱动：**

- **必选子技能：** `rh-sup-subagent-driven-development`  
- 每任务新子代理 + 两阶段评审  

**若选本会话串行：**

- **必选子技能：** `rh-sup-executing-plans`  
- 批量执行 + 检查点审阅  
