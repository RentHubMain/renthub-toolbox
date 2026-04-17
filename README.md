# RentHub Rulesync Toolbox

> 团队里往往同时用多种 AI 工具（Copilot、Codex CLI、Claude Code、Cursor 等），但各工具的约定文件格式不同，容易重复维护、漂移不一致。  
> **Rulesync** 把规则、命令、skills 等收敛成**单一源码树**（本仓库中的 `.rulesync/`），再按需生成到各工具的配置目录。

## 1) Rulesync 是什么

Rulesync 是 **AI 约定同步器**：

- **单一事实来源**：在 `.rulesync/` 里写一次，多工具复用。
- **多目标导出**：生成到 Cursor / Claude Code / Copilot 等各自识别的路径与格式。
- **可版本管理**：源码是普通文本，适合 Git 与 Code Review。
- **模块化**：可按需启用 rules、ignore、mcp、commands、subagents、**skills**、hooks 等。

官方文档：

- [Installation](https://rulesync.dyoshikawa.com/getting-started/installation.html)
- [Quick Start](https://rulesync.dyoshikawa.com/getting-started/quick-start.html)
- [Why Rulesync](https://rulesync.dyoshikawa.com/guide/why-rulesync.html)

## 2) 为什么需要 Rulesync

在多人、多工具并行时，Rulesync 有助于：

- 避免同一套规范散落在多个目录、各改各的。
- 减少「某个工具更新了、另一个没跟上」的漂移。
- 新人只需理解 **`.rulesync/` 的布局**，而不是每个 IDE 各一套位置。

典型工作流：

- 在 **`.rulesync/`** 维护源文件。
- 执行 `rulesync generate`，把产物写到各工具约定位置。

## 3) 本仓库的 Rulesync 资产

### 根配置

- **`rulesync.jsonc`**
  - `targets`: `copilot`, `cursor`, `claudecode`, `codexcli`
  - `features`: `rules`, `ignore`, `mcp`, `commands`, `subagents`, `skills`, `hooks`
  - `baseDirs`: `.`
  - `delete`: `true`（生成时可删除旧目标文件）
  - `gitignoreTargetsOnly`: `true`

### 目录结构（节选）

- **`.rulesync/.aiignore`** — 统一忽略规则源文件  
- **`.rulesync/rules/`** — 各子项目指南（overview、admin、docs、mini、website 等）  
- **`.rulesync/mcp.json`** — MCP 服务器配置（可按需填充）  
- **`.rulesync/commands/`** — 例如 `review-pr.md`  
- **`.rulesync/subagents/`** — 例如 `planner.md`  
- **`.rulesync/skills/`** — **Agent Skills（见下一节）**  
- **`.rulesync/hooks.json`** — Hooks（可按需填充）

## 4) Agent Skills（`.rulesync/skills/`）

Skills 是写给 **AI 代理** 的操作说明：何时启用、按什么步骤做、有哪些硬约束。  
**源码目录**：`.rulesync/skills/<skill 文件夹>/`，入口一般为 **`SKILL.md`**。

**你怎么用：**

1. **生成到工具**：在项目根执行 `rulesync generate`（或指定 `--targets` / `--features skills`），让 Cursor / Claude 等加载生成后的 skill。  
2. **在对话里显式引用**：在支持 `@` 引用路径的客户端中，可 **`@.rulesync/skills/.../SKILL.md`**（或生成后的等价路径），让当前会话按该 skill 执行。  
3. **人工阅读**：直接打开对应 `SKILL.md` 了解流程与命令。

以下为 **RentHub 当前内置的 5 个 skill**（文件夹名 = 目录名；YAML 里的 `name` 为 skill 逻辑名）。

---

### `renthub-brainstorming`（`name: brainstorming`）

| 项目 | 说明 |
|------|------|
| **何时用** | 在写代码/脚手架/改行为之前，做任何**创造性或规格级**工作前：**新功能、新组件、改交互、改架构**等。 |
| **怎么用** | 按 `SKILL.md` 流程：摸清上下文 → 必要时提供「可视化伴侣」→ 逐条澄清 → 给出 2–3 方案 → 分节设计并获批准 → 写设计文档到 `docs/superpowers/specs/` → 规格自检与用户审阅 → 再进入实现（文档中约定下一步为 **writing-plans**，**禁止**在设计批准前写实现代码）。 |
| **配套文件** | `visual-companion.md`（浏览器可视化脑暴）、`spec-document-reviewer-prompt.md`（子代理审规格模板）、`scripts/`（本地预览服务器等）。 |

---

### `renthub-commit`（`name: renthub-commit`）

| 项目 | 说明 |
|------|------|
| **何时用** | 用户说「帮我 commit / 写 commit message / 提交」或需要按 **Conventional Commits** 规范提交时。 |
| **怎么用** | `git status` / `git diff` 判断粒度 → 按 `type(scope): subject` 起草中文 subject（与可选 body）→ **经用户确认后再** `git commit`；禁止未确认自动提交；禁止 AI 署名式废话。 |

---

### `renthub-legal-version-release`（`name: legal-version-release`）

| 项目 | 说明 |
|------|------|
| **何时用** | **`renthub-docs/legal/`** 协议修订完成，需要**发新版本**并**保留历史版本**（归档 + 现行版升级 + 导航）。 |
| **怎么用** | 先拿到 **旧版号、新版号、生效日期** 三项输入；再按 `SKILL.md` 执行 Docusaurus 版本化、归档文档与 `index` 链接修正、现行版 front matter、navbar / `docusaurus.config.ts`、`npm run build` 等；**不改正文语义**，只做版本与导航一致性。 |

---

### `renthub-test-driven-development`（`name: test-driven-development`）

| 项目 | 说明 |
|------|------|
| **何时用** | **实现任何功能或修 bug 之前**；新功能、缺陷、重构、行为变更都应默认遵循（文档列出的少数例外需与协作方确认）。 |
| **怎么用** | 严格 **红 → 绿 → 重构**：先写**失败测试**并看到失败 → 最少实现通过 → 再整理；禁止先写生产代码再补测试。Mock / 测试坏味道见同目录 **`testing-anti-patterns.md`**。 |

---

### `renthub-ui-ux-pro-max`（`name: ui-ux-pro-max`）

| 项目 | 说明 |
|------|------|
| **何时用** | 要做 **UI/UX 设计、实现、优化或评审**（Web / 移动端均可）时。 |
| **怎么用** | 准备 **产品类型、行业/场景、风格关键词、技术栈**；在仓库内用 Python 跑 **`scripts/search.py`**（路径：`.rulesync/skills/renthub-ui-ux-pro-max/scripts/search.py`）生成设计系统、按域/栈检索；输出需覆盖方向、色板字体、结构组件、交互与 a11y、反模式、落地要点等（详见 `SKILL.md`）。 |

---

## 5) RentHub Toolbox 用法（Rulesync）

### 安装

```bash
npm install -g rulesync
# 或
brew install rulesync

rulesync --version
rulesync --help
```

### 日常同步

```bash
# 1) 编辑 .rulesync/ 下源文件（rules、skills、commands 等）

# 2) 仅同步 skills 到某目标（示例：Copilot）
rulesync generate --targets copilot --features skills

# 3) 全量生成（按 rulesync.jsonc 配置）
rulesync generate --targets "*" --features "*"
```

### 从已有工具配置反向导入（可选）

```bash
rulesync import --targets claudecode
rulesync import --targets cursor
rulesync import --targets copilot
rulesync import --targets claudecode --features rules,mcp,commands,subagents
```

### 新项目初始化（可选）

```bash
rulesync init
rulesync fetch dyoshikawa/rulesync --features skills
```

### 文本编码与乱码排查

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

## 6) 一句话总结

**Rulesync 在 RentHub 里的角色**：把多工具、多格式的 AI 约定收成 **一份可维护的 `.rulesync/` 源码**，需要时再生成到各工具，**Skills 集中在 `.rulesync/skills/`，由 `SKILL.md` 定义何时用、怎么用。**
