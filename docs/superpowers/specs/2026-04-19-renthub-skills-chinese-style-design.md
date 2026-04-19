# RentHub：`.cursor/skills` 下 SKILL 中文与版式统一

**状态**：已定稿，待实现  
**日期**：2026-04-19  
**范围**：仅 `d:\Projects\RentHub\.cursor\skills\` 下各技能包根目录的 `SKILL.md`

---

## 1. 背景与目标

仓库内 RentHub 相关技能分散在 `.cursor/skills/` 与 `.rulesync/skills/` 等处，部分 `SKILL.md` 为英文正文，部分为中文；标题、YAML 与语气也不完全一致。需要在**不扩大功能、不重组流程步骤**的前提下，统一为可读、可执行的中文说明，并统一 Markdown 版式。

**非目标**：本次不修改 `.rulesync/skills/`（交给后续脚本或手工同步）。

---

## 2. 范围与源文件

### 2.1 纳入范围

以下 **7 个文件**（路径均为相对于仓库根）：

| 目录 | `SKILL.md` |
|------|------------|
| `.cursor/skills/renthub-brainstorming/` | ✓ |
| `.cursor/skills/renthub-commit/` | ✓ |
| `.cursor/skills/renthub-finishing-a-development-branch/` | ✓ |
| `.cursor/skills/renthub-legal-version-release/` | ✓ |
| `.cursor/skills/renthub-systematic-debugging/` | ✓ |
| `.cursor/skills/renthub-test-driven-development/` | ✓ |
| `.cursor/skills/renthub-ui-ux-pro-max/` | ✓ |

### 2.2 明确排除

- `.rulesync/skills/**/SKILL.md` 及其中任意附属 `.md`（本次不编辑）。
- 各技能包内非 `SKILL.md` 的文件（如 `test-*.md`、`CREATION-LOG.md`、`scripts/` 等），除非实现时发现 **SKILL 内嵌引用** 必须与标题一致且仅改一处即可修复的明显笔误（仍须避免「顺手大改」）。

### 2.3 与 rulesync 的关系

- **正文与结构的权威源**：本次实现以 **`.cursor/skills/`** 为准。
- 后续同步 rulesync 时，应以此目录下对应 `SKILL.md` 为蓝本，再补上 rulesync 所需的 YAML 字段（如 `targets`），避免两套长期各写各的。

---

## 3. 内容原则（不大改实质）

1. **步骤与逻辑**：不增删阶段、不合并/拆分章节；不新增「功能」或新流程。
2. **语言**：叙述、列表说明、小节标题以 **现代汉语** 为主，语气与现有中文技能（如 `renthub-commit`、脑暴、TDD）**同级**：简洁、可执行、少口号堆砌。
3. **保留英文或原文的情形**（不强行翻译）：
   - 代码块、shell 命令、文件路径、URL；
   - Graphviz `dot` 源码及其中 **为渲染服务** 的英文 label（若译成中文不影响图意，可译；若易破坏布局或歧义，保留英文）；
   - 约定型标签名，如 `<HARD-GATE>`、`<Good>`、`<Bad>` 等 **保持英文标签字面**，仅 surrounding 说明用中文；
   - 开发者通用术语在句中可保留 **commit / PR / merge / rebase** 等，避免生硬翻译。
4. **两篇英文正文** 须整体改为中文：
   - `renthub-finishing-a-development-branch/SKILL.md`
   - `renthub-systematic-debugging/SKILL.md`
5. **已是中文的 SKILL**：以 **术语统一、标题层级、标点、粗体用法、代码块语言标签** 为主做对齐，不重写故事线。

---

## 4. YAML frontmatter

- **字段**：
  - 保留现有 `name` 的**取值不变**（与 README 等说明一致，避免工具或文档引用断裂）。
  - `description`：**一句中文**，概括「何时用 / 做什么」（与正文不矛盾）。
- **格式**：`---` 分隔；字段顺序统一为 `name` 然后 `description`（若仅有这两项）。
- **不引入** 本仓库 `.cursor` 侧当前不存在的字段（如 `targets`）；那是 rulesync 侧 concern。

---

## 5. 标题与正文版式

1. **一级标题 `#`**：使用 **简短中文名**；若与目录名不易对应，可采用 **「中文名（缩写或说明）」**，与现有 `# 测试驱动开发（TDD）` 风格一致。
2. **二级及以下**：中文标题；原英文小节标题译为中文，**一一对应**，不合并。
3. **强调**：关键原则、铁律、禁止项继续用 **粗体**；保留原有「检查清单」「流程」等结构。
4. **Markdown**：列表、有序步骤、围栏代码块与 **语言标签**（如 `bash`、`powershell`、`text`、`dot`）齐全；中英文标点不混排到难以阅读（以中文语境为主句读）。

---

## 6. README（可选）

若 README 中某处暗示「唯一 SKILL 路径在 rulesync」且与「以 `.cursor/skills` 为编辑源」**明显矛盾**，允许 **一句** 澄清（例如说明 Cursor 侧为当前维护源、rulesync 由同步流程更新）。**若无不矛盾，则不改 README。**

---

## 7. 验收标准

1. 上述 **7 个** `SKILL.md` 通读：无未完成占位（TBD/TODO 等），无内部矛盾。
2. 每个文件：`name` 未改；`description` 为中文；正文主体为中文且可照做。
3. **不修改** `.rulesync/skills/` 下任何文件（本次 PR/提交可单独只含 `.cursor` 与 `docs/superpowers/specs/`）。

---

## 8. 实现之后（流程衔接）

本仓库 **未发现** `writing-plans` skill。实现本规格时：

- 由执行者自拟 **简短任务清单**（按文件逐个：英译中 / 中文润色与版式 / 自检）即可；
- 若日后引入 `writing-plans`，可将本文件作为输入生成更细粒度补丁计划。

---

## 9. 规格自检（定稿前已执行）

| 检查项 | 结果 |
|--------|------|
| 占位符 / 未完成节 | 无 |
| 与「只维护 .cursor」是否一致 | 一致 |
| 与「name 不改」是否一致 | 一致 |
| 范围是否可单次完成 | 是（7 文件 + 可选 README 一句） |
| 歧义 | 「全中文」以第 3 节边界为准；代码与标签字面除外 |

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-04-19 | 初稿：脑暴确认 A（正文中文）、仅 `.cursor/skills/`、rulesync defer |
