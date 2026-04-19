# RentHub：`.cursor/skills` 下 SKILL 中文与版式统一

**状态**：已定稿，待实现  
**日期**：2026-04-19（2026-04-19 修订：纳入 `rh-sup-*` 与本轮验收范围）  
**范围**：仅 `d:\Projects\RentHub\.cursor\skills\` 下各技能包根目录的 `SKILL.md`

---

## 1. 背景与目标

仓库内 RentHub 相关技能分散在 `.cursor/skills/` 与 `.rulesync/skills/` 等处，部分 `SKILL.md` 为英文正文，部分为中文；标题、YAML 与语气也不完全一致。需要在**不扩大功能、不重组流程步骤**的前提下，统一为可读、可执行的中文说明，并统一 Markdown 版式。

**非目标**：本次不修改 `.rulesync/skills/`（交给 rulesync 从真源生成或后续同步流程）。

---

## 2. 范围与源文件

### 2.1 本轮实施与验收范围（脑暴确认）

以下 **15** 个 `SKILL.md`（路径均为相对于仓库根）为本轮**必须**完成翻译（或中文对齐）、版式统一与验收的对象：

| # | 路径 |
|---|------|
| 1 | `.cursor/skills/renthub-ui-ux-pro-max/SKILL.md` |
| 2 | `.cursor/skills/rh-sup-brainstorming/SKILL.md` |
| 3 | `.cursor/skills/rh-sup-dispatching-parallel-agents/SKILL.md` |
| 4 | `.cursor/skills/rh-sup-executing-plans/SKILL.md` |
| 5 | `.cursor/skills/rh-sup-finishing-a-development-branch/SKILL.md` |
| 6 | `.cursor/skills/rh-sup-receiving-code-review/SKILL.md` |
| 7 | `.cursor/skills/rh-sup-requesting-code-review/SKILL.md` |
| 8 | `.cursor/skills/rh-sup-subagent-driven-development/SKILL.md` |
| 9 | `.cursor/skills/rh-sup-systematic-debugging/SKILL.md` |
| 10 | `.cursor/skills/rh-sup-test-driven-development/SKILL.md` |
| 11 | `.cursor/skills/rh-sup-using-git-worktrees/SKILL.md` |
| 12 | `.cursor/skills/rh-sup-using-superpowers/SKILL.md` |
| 13 | `.cursor/skills/rh-sup-verification-before-completion/SKILL.md` |
| 14 | `.cursor/skills/rh-sup-writing-plans/SKILL.md` |
| 15 | `.cursor/skills/rh-sup-writing-skills/SKILL.md` |

说明：`renthub-ui-ux-pro-max` 已在正文中为中文时，以**术语、层级、标点、代码块语言标签**与本轮其余文件对齐为主，不重写流程。

### 2.2 同原则下的可选扩展批次（非本轮必选验收）

下列 **6** 个 `renthub-*` 技能与 §2.1 **不重复**（不含已在 §2.1 的 `renthub-ui-ux-pro-max`）。若后续希望全仓库「仅 `.cursor/skills/` 根目录 `SKILL.md`」风格一致，可按第 3～5 节同一标准执行，但**不纳入本轮 PR 的必选验收计数**。

| 路径 |
|------|
| `.cursor/skills/renthub-brainstorming/SKILL.md` |
| `.cursor/skills/renthub-commit/SKILL.md` |
| `.cursor/skills/renthub-finishing-a-development-branch/SKILL.md` |
| `.cursor/skills/renthub-legal-version-release/SKILL.md` |
| `.cursor/skills/renthub-systematic-debugging/SKILL.md` |
| `.cursor/skills/renthub-test-driven-development/SKILL.md` |

### 2.3 去重后的「一次做完」全量参考

若将 §2.1 与 §2.2 **合并一次做完**，共 **21** 个互不重复的 `SKILL.md`（15 + 6）。本轮文档以 §2.1 为必选、§2.2 为可选。

### 2.4 明确排除

- `.rulesync/skills/**/SKILL.md` 及其中任意附属 `.md`（本次不编辑）。
- 各技能包内非根目录 `SKILL.md` 的文件（如 `test-*.md`、`CREATION-LOG.md`、`scripts/`、`references/` 等），除非实现时发现 **SKILL 内嵌引用** 必须与标题一致且仅改一处即可修复的明显笔误（仍须避免「顺手大改」）。

### 2.5 与 rulesync 的关系

- **正文与结构的权威源**：实现与日常维护以 **`.cursor/skills/`** 为准。
- 后续由 rulesync 生成或更新 `.rulesync/skills/` 时，应以此目录下对应 `SKILL.md` 为蓝本，再补上 rulesync 所需的 YAML 字段（如 `targets`），避免两套长期各写各的。

---

## 3. 内容原则（不大改实质）

1. **步骤与逻辑**：不增删阶段、不合并/拆分章节；不新增「功能」或新流程。若英文版有检查清单、流程图、`<HARD-GATE>` 等结构，译后**一一保留**对应块与顺序。
2. **语言**：叙述、列表说明、小节标题以 **现代汉语** 为主，语气与现有中文技能（如 `renthub-commit`、脑暴、TDD）**同级**：简洁、可执行、少口号堆砌。
3. **保留英文或原文的情形**（不强行翻译）：
   - 代码块、shell 命令、文件路径、URL；
   - Graphviz `dot` 源码及其中 **为渲染服务** 的英文 label（若译成中文不影响图意，可译；若易破坏布局或歧义，保留英文）；
   - **约定型标签字面**保持英文：如 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>`、`<Good>`、`<Bad>` 等；**其上下说明**用中文；
   - 开发者通用术语在句中可保留 **commit / PR / merge / rebase / CI** 等，避免生硬翻译；
   - 各环境工具名（如 `Skill` / `TodoWrite`）以「中文说明 + 必要时括号保留英文名」为主，避免读者找不到原文档。
4. **主体为英文的 SKILL.md`**（含各 `rh-sup-*` 及 §2.2 中尚未充分本土化的 `renthub-*`）须整体译为中文，边界同上。
5. **已是中文的 SKILL**（含 `renthub-ui-ux-pro-max`）：以 **术语统一、标题层级、标点、粗体用法、代码块语言标签** 为主做对齐，不重写故事线。
6. **偏口号或强调的英文块**（常见于 `rh-sup-using-superpowers` 等）：译为中文时保留**力度**（铁律、禁止项），可改为**粗体**或短句，避免弱化或堆砌口号。

---

## 4. YAML frontmatter

- **字段**：
  - 保留现有 `name` 的**取值不变**（与 README 等说明一致，避免工具或文档引用断裂）。
  - `description`：**一句中文**，概括「何时用 / 做什么」（与正文不矛盾）。
- **格式**：`---` 分隔；字段顺序统一为 `name` 然后 `description`（若仅有这两项）。
- **不引入** 本仓库 `.cursor/skills` 侧当前不存在的字段（如 `targets`）；那是 rulesync 侧 concern。

---

## 5. 标题与正文版式

1. **一级标题 `#`**：使用 **简短中文名**；可采用 **「中文名（缩写或说明）」**，与现有 `# 测试驱动开发（TDD）` 风格一致。
2. **二级及以下**：中文标题；原英文小节标题译为中文，**一一对应**，不合并。
3. **强调**：关键原则、铁律、禁止项继续用 **粗体**；保留原有「检查清单」「流程」等结构。
4. **Markdown**：列表、有序步骤、围栏代码块与 **语言标签**（如 `bash`、`powershell`、`text`、`dot`、`md`）齐全；中英文标点不混排到难以阅读（以中文语境为主句读）。

---

## 6. README（可选）

若 README 中某处暗示「唯一 SKILL 路径在 rulesync」且与「以 `.cursor/skills` 为编辑源」**明显矛盾**，允许 **一句** 澄清（例如说明 Cursor 侧为当前维护源、rulesync 由同步流程更新）。**若无不矛盾，则不改 README。**

---

## 7. 验收标准

### 7.1 本轮必选

1. §2.1 所列 **15** 个 `SKILL.md` 通读：无未完成占位（TBD/TODO 等），无内部矛盾。
2. 每个文件：`name` 未改；`description` 为中文；正文主体为中文且可照做（第 3 节保留边界除外）。
3. **不修改** `.rulesync/skills/` 下任何文件（本轮 PR/提交可单独只含 `.cursor/skills/` 与 `docs/superpowers/specs/`）。

### 7.2 可选扩展

若执行 §2.2：共 **6** 个文件，标准与 §7.1 相同，可在单独提交或同一 PR 的独立提交中完成。

---

## 8. 实现之后（流程衔接）

仓库 **已存在** `.cursor/skills/rh-sup-writing-plans/SKILL.md`。实现本规格时建议：

1. 在完成 §2.1 正文修改前或分段完成后，**可选**使用 `rh-sup-writing-plans` 将本规格与目标文件列表作为输入，生成补丁级或按文件拆分的实现计划；
2. 若未使用 writing-plans，由执行者自拟 **简短任务清单**（按文件逐个：英译中 / 中文润色与版式 / 自检）亦可。

---

## 9. 规格自检（本轮写入后已执行）

| 检查项 | 结果 |
|--------|------|
| 占位符 / 未完成节 | 无 |
| 与「只维护 `.cursor/skills`」是否一致 | 一致 |
| 与「`name` 不改」是否一致 | 一致 |
| 本轮范围是否可数且明确 | 是（§2.1 共 15 个路径） |
| 与历史「7 个 renthub」关系是否说清 | 是（§2.2 可选 + §2.3 全量 21） |
| 歧义 | 「全中文」以第 3 节边界为准；代码与标签字面除外 |

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-04-19 | 初稿：脑暴确认（正文中文）、仅 `.cursor/skills/`、rulesync defer |
| 2026-04-19 | 修订：纳入 `rh-sup-*` 共 14 与 `renthub-ui-ux-pro-max` 本轮 15 文件清单；扩展第 3 节标签与语气；更新验收与 §8（`rh-sup-writing-plans` 已存在）；区分可选 `renthub-*` 六件套 |
