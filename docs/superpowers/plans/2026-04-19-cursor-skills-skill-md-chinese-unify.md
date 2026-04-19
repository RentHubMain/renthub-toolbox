# Cursor 技能 `SKILL.md` 中文与版式统一 — 实现计划

> **面向代理执行者：** 建议 REQUIRED SUB-SKILL：使用 **`rh-sup-subagent-driven-development`**（推荐）或 **`rh-sup-executing-plans`**，按下方任务逐项实施。步骤使用 `- [ ]` 复选框跟踪进度。

**目标：** 在 `.cursor/skills/` 下，对规格 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §2.1 所列 **15** 个根目录 `SKILL.md` 完成中文翻译或中文对齐、YAML 与 Markdown 版式统一，且不触碰 `.rulesync/skills/`。

**做法概要：** 以规格第 3～5 节为唯一内容准则；每个文件独立分支或独立提交，便于审阅与回滚。先处理体量较小或已是中文的文件，将长文技能（如脑暴、TDD、`using-superpowers`）放在中段；**将 `rh-sup-writing-plans/SKILL.md` 的翻译放在倒数第二或最后**，以便执行前半段任务时仍可参照英文版 writing-plans 原文。

**技术栈：** Git、Markdown、PowerShell（仓库默认 shell）、可选 `rg`（ripgrep）。

---

## 文件与职责映射（实施前锁定）

| 职责 | 路径 |
|------|------|
| 规格（只读输入） | `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` |
| 本轮必改 `SKILL.md`（15） | 见规格 §2.1 表格 `#1`～`#15` |
| 可选扩展（本轮计划不执行） | 规格 §2.2 六个 `renthub-*`（除非产品方明确要求并入同一 PR） |
| 禁止编辑 | `.rulesync/skills/**` 及任意非根 `SKILL.md` 附属文档（规格 §2.4） |

---

### Task 0：开工检查与基线

**Files:**

- Read: `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md`
- Modify: 无（若 README 与「真源在 `.cursor/skills`」明显矛盾，才按规格 §6 改 **一句**；否则跳过）

- [ ] **Step 1：确认 15 个目标文件均存在**

Run:

```powershell
Set-Location "d:\Projects\RentHub"
$paths = @(
  ".cursor/skills/renthub-ui-ux-pro-max/SKILL.md",
  ".cursor/skills/rh-sup-brainstorming/SKILL.md",
  ".cursor/skills/rh-sup-dispatching-parallel-agents/SKILL.md",
  ".cursor/skills/rh-sup-executing-plans/SKILL.md",
  ".cursor/skills/rh-sup-finishing-a-development-branch/SKILL.md",
  ".cursor/skills/rh-sup-receiving-code-review/SKILL.md",
  ".cursor/skills/rh-sup-requesting-code-review/SKILL.md",
  ".cursor/skills/rh-sup-subagent-driven-development/SKILL.md",
  ".cursor/skills/rh-sup-systematic-debugging/SKILL.md",
  ".cursor/skills/rh-sup-test-driven-development/SKILL.md",
  ".cursor/skills/rh-sup-using-git-worktrees/SKILL.md",
  ".cursor/skills/rh-sup-using-superpowers/SKILL.md",
  ".cursor/skills/rh-sup-verification-before-completion/SKILL.md",
  ".cursor/skills/rh-sup-writing-plans/SKILL.md",
  ".cursor/skills/rh-sup-writing-skills/SKILL.md"
)
$paths | ForEach-Object { if (-not (Test-Path $_)) { throw "Missing: $_" } }
"All 15 paths exist."
```

Expected: 输出 `All 15 paths exist.` 且无 `Missing` 异常。

- [ ] **Step 2：确认工作区未误暂存 `.rulesync`**

Run:

```powershell
git diff --name-only --cached
```

Expected: 若列表中出现 `.rulesync/` 下路径，执行 `git restore --staged <path>` 移出暂存，直到暂存区不含 `.rulesync/`。

- [ ] **Step 3：（可选）README 矛盾检查**

Run:

```powershell
Select-String -Path "README.md" -Pattern "rulesync","\.cursor/skills" -SimpleMatch -ErrorAction SilentlyContinue
```

若 README 明确写「唯一维护源仅为 `.rulesync/skills`」等与规格 §2.5 冲突，按规格 §6 用 **一句** 澄清；否则不改 `README.md`。

---

### Task 1：`renthub-ui-ux-pro-max` 中文对齐

**Files:**

- Modify: `.cursor/skills/renthub-ui-ux-pro-max/SKILL.md`

- [ ] **Step 1：记录不可变字段**

Run：

```powershell
Select-String -Path ".cursor/skills/renthub-ui-ux-pro-max/SKILL.md" -Pattern '^name:\s*' | ForEach-Object { $_.Line }
```

Expected: 输出现有 `name:` 行；后续编辑后该行字节级一致。

- [ ] **Step 2：按规格 §5 补齐围栏语言标签**

人工编辑：将所有无语言标签的 ``` 围栏改为 ```bash / ```text 等恰当标签；不改动 `python3 ...` 命令字面。

- [ ] **Step 3：`description` 与标题润色**

确保 `description` 为 **一句中文**（规格 §4）；`#` 一级标题保持简短中文；二级标题用词与 `renthub-commit` 等中文技能一致（规格 §5）。

- [ ] **Step 4：自检**

Run：

```powershell
git diff ".cursor/skills/renthub-ui-ux-pro-max/SKILL.md"
```

Expected: 无 `TBD`/`TODO` 新占位；无对 `scripts/`、`data/` 路径的错误改写。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/renthub-ui-ux-pro-max/SKILL.md"
git commit -m "docs(skills): 对齐 renthub-ui-ux-pro-max SKILL 版式与描述"
```

---

### Task 2：`rh-sup-dispatching-parallel-agents` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-dispatching-parallel-agents/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段**

在编辑器中复制 frontmatter 中 `name:` 行到剪贴板备用；完成全文编辑后须与 Step 1 完全一致。

- [ ] **Step 2：翻译正文与标题**

对照规格 §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>` 等标签字面；代码块、路径、URL 不译；小节标题全部译为中文并与原英文小节一一对应。

- [ ] **Step 3：`description` 中文化**

`description:` 一句中文，概括「何时触发 / 做什么」，与正文「何时使用」一致（规格 §4）。

- [ ] **Step 4：验证 frontmatter**

Run：

```powershell
$content = Get-Content ".cursor/skills/rh-sup-dispatching-parallel-agents/SKILL.md" -Raw
if ($content -notmatch '(?s)^---\r?\nname:\s+\S+') { throw "frontmatter name missing" }
if ($content -notmatch 'description:\s*[\p{IsCJKUnifiedIdeographs}]') { throw "description should be Chinese" }
"frontmatter OK"
```

Expected: 输出 `frontmatter OK`。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-dispatching-parallel-agents/SKILL.md"
git commit -m "docs(skills): rh-sup-dispatching-parallel-agents SKILL 中文化"
```

---

### Task 3：`rh-sup-executing-plans` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-executing-plans/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-executing-plans/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：验证**

Run：

```powershell
Select-String -Path ".cursor/skills/rh-sup-executing-plans/SKILL.md" -Pattern '^##\s+[A-Za-z]{3,}' 
```

Expected: **无输出**（二级标题不应再以纯英文短语开头；合法缩写如 `CI` 出现在标题内可接受，若出现整行英文标题应改中文）。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-executing-plans/SKILL.md"
git commit -m "docs(skills): rh-sup-executing-plans SKILL 中文化"
```

---

### Task 4：`rh-sup-finishing-a-development-branch` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-finishing-a-development-branch/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-finishing-a-development-branch/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：保留交互选项结构**

若正文含 `AskQuestion` / 多选项列表，仅译说明文字，**不**改选项机器可读 id（若有）；若无 id 则整段中文化。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-finishing-a-development-branch/SKILL.md"
git commit -m "docs(skills): rh-sup-finishing-a-development-branch SKILL 中文化"
```

---

### Task 5：`rh-sup-receiving-code-review` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-receiving-code-review/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-receiving-code-review/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：验证 frontmatter**

Run：

```powershell
$content = Get-Content ".cursor/skills/rh-sup-receiving-code-review/SKILL.md" -Raw
if ($content -notmatch '(?s)^---\r?\nname:\s+\S+') { throw "frontmatter name missing" }
if ($content -notmatch 'description:\s*[\p{IsCJKUnifiedIdeographs}]') { throw "description should be Chinese" }
"frontmatter OK"
```

Expected: 输出 `frontmatter OK`。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-receiving-code-review/SKILL.md"
git commit -m "docs(skills): rh-sup-receiving-code-review SKILL 中文化"
```

---

### Task 6：`rh-sup-requesting-code-review` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-requesting-code-review/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-requesting-code-review/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：子路径引用**

若正文引用 `code-reviewer.md` 等相对路径，仅译说明句，**不**改路径字符串。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-requesting-code-review/SKILL.md"
git commit -m "docs(skills): rh-sup-requesting-code-review SKILL 中文化"
```

---

### Task 7：`rh-sup-using-git-worktrees` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-using-git-worktrees/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-using-git-worktrees/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：shell 示例**

所有 `bash`/`sh` 围栏保持 **语言标签** `bash`，命令字面不译；仅译围栏上方说明。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-using-git-worktrees/SKILL.md"
git commit -m "docs(skills): rh-sup-using-git-worktrees SKILL 中文化"
```

---

### Task 8：`rh-sup-verification-before-completion` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-verification-before-completion/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-verification-before-completion/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：验证 frontmatter**

Run：

```powershell
$content = Get-Content ".cursor/skills/rh-sup-verification-before-completion/SKILL.md" -Raw
if ($content -notmatch '(?s)^---\r?\nname:\s+\S+') { throw "frontmatter name missing" }
if ($content -notmatch 'description:\s*[\p{IsCJKUnifiedIdeographs}]') { throw "description should be Chinese" }
"frontmatter OK"
```

Expected: 输出 `frontmatter OK`。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-verification-before-completion/SKILL.md"
git commit -m "docs(skills): rh-sup-verification-before-completion SKILL 中文化"
```

---

### Task 9：`rh-sup-writing-skills` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-writing-skills/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-writing-skills/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：验证 frontmatter**

Run：

```powershell
$content = Get-Content ".cursor/skills/rh-sup-writing-skills/SKILL.md" -Raw
if ($content -notmatch '(?s)^---\r?\nname:\s+\S+') { throw "frontmatter name missing" }
if ($content -notmatch 'description:\s*[\p{IsCJKUnifiedIdeographs}]') { throw "description should be Chinese" }
"frontmatter OK"
```

Expected: 输出 `frontmatter OK`。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-writing-skills/SKILL.md"
git commit -m "docs(skills): rh-sup-writing-skills SKILL 中文化"
```

---

### Task 10：`rh-sup-subagent-driven-development` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-subagent-driven-development/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-subagent-driven-development/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：长文档分块提交（可选）**

若单 diff 过大，可先提交「前半译稿」再提交「后半」，但同一文件禁止留下半英文半中文的 **发布态**；合并前保持分支内连续提交即可。

- [ ] **Step 5：提交（或两次提交）**

```powershell
git add ".cursor/skills/rh-sup-subagent-driven-development/SKILL.md"
git commit -m "docs(skills): rh-sup-subagent-driven-development SKILL 中文化"
```

---

### Task 11：`rh-sup-systematic-debugging` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-systematic-debugging/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-systematic-debugging/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：保留附录式文件名引用**

对 `test-pressure-1.md` 等仅出现在叙述中的文件名：译周围文字，**不**改文件名。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-systematic-debugging/SKILL.md"
git commit -m "docs(skills): rh-sup-systematic-debugging SKILL 中文化"
```

---

### Task 12：`rh-sup-test-driven-development` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-test-driven-development/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-test-driven-development/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：代码块内英文保留**

示例中的 `pytest`、`assert`、函数名保持英文；围栏外说明用中文。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-test-driven-development/SKILL.md"
git commit -m "docs(skills): rh-sup-test-driven-development SKILL 中文化"
```

---

### Task 13：`rh-sup-using-superpowers` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-using-superpowers/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-using-superpowers/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。**另外**遵循规格 §3 第 6 条：口号式英文译为中文时保持力度，可用粗体短句。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：`dot` 流程图**

图内节点 label：若译中文不损布局则译；否则保留英文 label，在图前用中文说明图意。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-using-superpowers/SKILL.md"
git commit -m "docs(skills): rh-sup-using-superpowers SKILL 中文化"
```

---

### Task 14：`rh-sup-brainstorming` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-brainstorming/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-brainstorming/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：流程图与 HARD-GATE**

保留 `<HARD-GATE>` 块与 `dot` 源码结构；检查清单章节顺序不变。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-brainstorming/SKILL.md"
git commit -m "docs(skills): rh-sup-brainstorming SKILL 中文化"
```

---

### Task 15：`rh-sup-writing-plans` 英译中

**Files:**

- Modify: `.cursor/skills/rh-sup-writing-plans/SKILL.md`

- [ ] **Step 1：冻结 `name` 字段** — 打开 `.cursor/skills/rh-sup-writing-plans/SKILL.md`，在编辑前将 frontmatter 中 `name:` 行完整复制到笔记；编辑结束后该行须与笔记逐字一致（规格 §4）。

- [ ] **Step 2：翻译标题与正文** — 对照 `docs/superpowers/specs/2026-04-19-renthub-skills-chinese-style-design.md` §3：保留 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 等标签字面；代码块、路径、URL 不译；`##` / `###` 译为中文并与原英文小节一一对应；不增删流程阶段（规格 §3、§5）。

- [ ] **Step 3：`description` 中文化** — `description:` 为一句中文，概括「何时触发 / 做什么」，与正文「何时使用」或等价段落一致；不新增 YAML 字段（规格 §4）。

- [ ] **Step 4：本实现计划文件**

译完本 skill 后，执行者若需更新 `docs/superpowers/plans/2026-04-19-cursor-skills-skill-md-chinese-unify.md` 内对 writing-plans 的英文引用句，仅译 **说明文字**，**不**改本计划文件路径与日期文件名。

- [ ] **Step 5：提交**

```powershell
git add ".cursor/skills/rh-sup-writing-plans/SKILL.md"
git commit -m "docs(skills): rh-sup-writing-plans SKILL 中文化"
```

---

### Task 16：整体验收（规格 §7.1）

**Files:**

- Read: 规格 §7.1；15 个 `SKILL.md`

- [ ] **Step 1：扫描占位符**

Run：

```powershell
Set-Location "d:\Projects\RentHub"
rg -n "TBD|TODO|FIXME" .cursor/skills/rh-sup-*/SKILL.md .cursor/skills/renthub-ui-ux-pro-max/SKILL.md
```

Expected: **无输出** 或仅命中允许位置（应无）。

- [ ] **Step 2：扫描 `name:` 被误改**

对每个文件执行 `git diff origin/master -- .cursor/skills/.../SKILL.md`（或合并基线）确认 `name:` 行未变；若 `origin/master` 无该文件则与 Task 0 备份或首 commit 比较。

- [ ] **Step 3：确认未触碰 `.rulesync`**

Run：

```powershell
git diff --name-only origin/master | Select-String "\.rulesync/"
```

Expected: **无输出**（相对合并基线不应出现 `.rulesync` 变更；若基线无分支则检查工作区 `git status` 无 `.rulesync` 修改）。

- [ ] **Step 4：人工通读**

按规格 §7.1 通读 15 文件各一遍，确认无内部矛盾、描述与正文一致。

---

## 计划自检（对照规格，已执行）

| 规格章节 | 计划覆盖 |
|----------|----------|
| §2.1 十五路径 | Task 0 校验 + Task 1～15 各文件 |
| §2.4 排除 rulesync 与附属 | Task 0 Step 2；各任务仅列根 `SKILL.md` |
| §3 内容原则 | Task 2 为范例；Task 3～15 各含完整 Step 1～3；Task 13 Step 2、Task 14 Step 4 强调特殊条 |
| §4 YAML | 每文件 Task 内 `description` / `name` 步骤 |
| §5 版式 | Task 1、Task 3 Step 4 |
| §6 README | Task 0 Step 3 |
| §7.1 验收 | Task 16 |

**占位符扫描：** 本计划正文无 `TBD`/`TODO`/`implement later`。  
**一致性：** Task 3～15 各自重复写明 Step 1～3（冻结 `name`、译正文与标题、`description` 中文化），仅文件路径与少数附加句（如 Task 13 Step 2）不同，避免跨任务跳转引用。

---

## 执行交接

**计划已保存至：** `docs/superpowers/plans/2026-04-19-cursor-skills-skill-md-chinese-unify.md`

**两种执行方式（二选一）：**

1. **子代理驱动（推荐）** — 每个 Task 派新子代理执行，任务间人工或代理复核；配合 **`rh-sup-subagent-driven-development`**。  
2. **本会话串行** — 在同一会话按 Task 顺序改文件并提交；任务间设检查点；配合 **`rh-sup-executing-plans`**。

你更倾向哪一种？
