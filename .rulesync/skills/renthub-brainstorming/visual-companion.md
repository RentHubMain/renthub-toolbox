# 可视化伴侣指南

基于浏览器的可视化脑暴伴侣，用于展示线框、示意图与选项。

## 何时使用

按**问题**决定，而非按整场会话。检验标准：**用户是「看到」比「读到」更懂吗？**

**在以下情况使用浏览器**（内容本身是视觉的）：

- **UI 线框** — 线框图、版式、导航结构、组件设计
- **架构示意图** — 系统组件、数据流、关系图
- **并排视觉对比** — 对比两种版式、两种配色、两种设计方向
- **视觉打磨** — 问题涉及观感、间距、视觉层级时
- **空间关系** — 状态机、流程图、实体关系等以图呈现

**在以下情况使用终端**（内容为文字或表格）：

- **需求与范围问题** — 「X 指什么？」「哪些功能在范围内？」
- **概念性 A/B/C 选择** — 用文字描述的不同方案
- **取舍列表** — 利弊、对比表
- **技术决策** — API 设计、数据建模、架构选型
- **澄清性问题** — 答案主要是文字而非视觉偏好时

关于 UI 的提问**不自动**等于视觉题。「想要哪种向导？」偏概念——用终端。「这几种向导版式哪个更对味？」偏视觉——用浏览器。

## 工作原理

服务器监听目录中的 HTML 文件，并把最新的一个提供给浏览器。你把 HTML 内容写到 `screen_dir`，用户在浏览器中查看并可点击选择。选择会记录到 `state_dir/events`，你在下一轮读取。

**内容片段 vs 完整文档：** 若 HTML 以 `<!DOCTYPE` 或 `<html` 开头，服务器原样提供（仅注入辅助脚本）。否则服务器会自动用你的内容包进框架模板——加上页头、CSS 主题、选中指示条及全部交互基础设施。**默认写内容片段。** 仅当你需要完全控制页面时再写完整文档。

## 启动会话

```bash
# 启动服务器并持久化（线框保存到项目）
scripts/start-server.sh --project-dir /path/to/project

# 返回：{"type":"server-started","port":52341,"url":"http://localhost:52341",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

保存响应中的 `screen_dir` 与 `state_dir`。告知用户打开 URL。

**查找连接信息：** 服务器将启动 JSON 写入 `$STATE_DIR/server-info`。若在后台启动且未捕获 stdout，读取该文件以获取 URL 与端口。使用 `--project-dir` 时，在 `<project>/.superpowers/brainstorm/` 下查找会话目录。

**注意：** 传入项目根作为 `--project-dir`，线框会持久保存在 `.superpowers/brainstorm/` 并在服务器重启后仍在。不传则文件在 `/tmp` 且可能被清理。若尚未忽略，提醒用户将 `.superpowers/` 加入 `.gitignore`。

**按平台启动服务器：**

**Claude Code（macOS / Linux）：**
```bash
# 默认模式可用——脚本自行后台化服务器
scripts/start-server.sh --project-dir /path/to/project
```

**Claude Code（Windows）：**
```bash
# Windows 自动检测并使用前台模式，会阻塞工具调用。
# 在 Bash 工具调用上设置 run_in_background: true，使服务器在
# 多轮对话间保持运行。
scripts/start-server.sh --project-dir /path/to/project
```
通过 Bash 工具调用时设置 `run_in_background: true`。下一轮读取 `$STATE_DIR/server-info` 获取 URL 与端口。

**Codex：**
```bash
# Codex 会回收后台进程。脚本检测 CODEX_CI 并切到前台模式。
# 正常运行即可——无需额外参数。
scripts/start-server.sh --project-dir /path/to/project
```

**Gemini CLI：**
```bash
# 使用 --foreground，并在 shell 工具调用上设置 is_background: true
# 使进程在多轮间保持运行
scripts/start-server.sh --project-dir /path/to/project --foreground
```

**其他环境：** 服务器必须在多轮对话间保持后台运行。若环境会回收脱离的进程，使用 `--foreground` 并结合你平台的后台执行机制启动。

若从浏览器无法访问 URL（远程/容器环境常见），绑定非 loopback 主机：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

用 `--url-host` 控制返回 URL JSON 中打印的主机名。

## 循环

1. **确认服务器存活**，然后在 `screen_dir` 中**写入新 HTML 文件**：
   - 每次写入前确认 `$STATE_DIR/server-info` 存在。若不存在（或存在 `$STATE_DIR/server-stopped`），说明服务器已关闭——先用 `start-server.sh` 重启再继续。服务器在无活动约 30 分钟后自动退出。
   - 文件名要有语义：`platform.html`、`visual-style.html`、`layout.html`
   - **不要复用文件名** — 每个画面用新文件
   - 使用 Write 工具 — **不要用 cat/heredoc**（会在终端产生噪音）
   - 服务器自动提供最新文件（按修改时间）

2. **告知用户会看到什么并结束本轮：**
   - 每步提醒 URL（不只第一步）
   - 简短文字概括画面内容（例如「展示首页三种版式选项」）
   - 请用户在终端回复：「请看一下并告诉我想法。需要的话可以点击选择。」

3. **下一轮** — 用户在终端回复后：
   - 若存在则读取 `$STATE_DIR/events` — 其中是用户浏览器交互（点击、选择）的 JSON 行
   - 与用户终端文字合并理解反馈
   - 以终端消息为主反馈；`state_dir/events` 提供结构化交互数据

4. **迭代或推进** — 若反馈会改变当前画面，写新文件（如 `layout-v2.html`）。仅当当前步骤已确认后再进入下一题。

5. **回到终端时卸载** — 若下一步不需要浏览器（例如澄清问题、取舍讨论），推一屏等待画面以清除过时内容：

   ```html
   <!-- 文件名：waiting.html（或 waiting-2.html 等） -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">继续在终端中进行…</p>
   </div>
   ```

   避免用户盯着已过时选择而对话已前进。下一个视觉问题出现时照常推新内容文件。

6. 重复直至结束。

## 撰写内容片段

只写放进页面的内容。服务器会自动包进框架模板（页头、主题 CSS、选中指示条及全部交互基础设施）。

**最小示例：**

```html
<h2>哪种版式更好？</h2>
<p class="subtitle">请考虑可读性与视觉层级</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>单栏</h3>
      <p>干净、专注的阅读体验</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>双栏</h3>
      <p>侧栏导航与主内容区</p>
    </div>
  </div>
</div>
```

即可。不需要 `<html>`、自定义 CSS 或 `<script>`。服务器会提供这些。

## 可用 CSS 类

框架模板为内容提供以下 CSS 类：

### 选项（A/B/C 类选择）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>标题</h3>
      <p>说明</p>
    </div>
  </div>
</div>
```

**多选：** 在容器上添加 `data-multiselect`，用户可多选。每次点击切换选中状态。指示条显示数量。

```html
<div class="options" data-multiselect>
  <!-- 相同 option 结构 — 用户可多选/取消 -->
</div>
```

### 卡片（视觉稿）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- 线框内容 --></div>
    <div class="card-body">
      <h3>名称</h3>
      <p>说明</p>
    </div>
  </div>
</div>
```

### 线框容器

```html
<div class="mockup">
  <div class="mockup-header">预览：仪表盘版式</div>
  <div class="mockup-body"><!-- 你的线框 HTML --></div>
</div>
```

### 分栏（并排）

```html
<div class="split">
  <div class="mockup"><!-- 左侧 --></div>
  <div class="mockup"><!-- 右侧 --></div>
</div>
```

### 利弊

```html
<div class="pros-cons">
  <div class="pros"><h4>优点</h4><ul><li>收益</li></ul></div>
  <div class="cons"><h4>缺点</h4><ul><li>代价</li></ul></div>
</div>
```

### 线框元素（线框构建块）

```html
<div class="mock-nav">Logo | 首页 | 关于 | 联系</div>
<div style="display: flex;">
  <div class="mock-sidebar">导航</div>
  <div class="mock-content">主内容区</div>
</div>
<button class="mock-button">操作按钮</button>
<input class="mock-input" placeholder="输入框">
<div class="placeholder">占位区域</div>
```

### 排版与区块

- `h2` — 页面标题
- `h3` — 小节标题
- `.subtitle` — 标题下辅助文字
- `.section` — 带底部间距的内容块
- `.label` — 小号大写标签文字

## 浏览器事件格式

用户点击选项时，交互记录到 `$STATE_DIR/events`（每行一个 JSON 对象）。推送新画面时文件会自动清空。

```jsonl
{"type":"click","choice":"a","text":"选项 A - 简单版式","timestamp":1706000101}
{"type":"click","choice":"c","text":"选项 C - 复杂网格","timestamp":1706000108}
{"type":"click","choice":"b","text":"选项 B - 混合","timestamp":1706000115}
```

完整事件流反映用户的探索路径——可能在落定前点击多个选项。通常最后一个 `choice` 事件是最终选择，但点击模式可反映犹豫或偏好，值得追问。

若不存在 `$STATE_DIR/events`，说明用户未在浏览器中交互——仅使用其终端文字。

## 设计提示

- **保真度与问题匹配** — 版式用线框，打磨问题再提高完成度
- **每页说明在问什么** — 「哪种版式更专业？」而不只是「选一个」
- **推进前先迭代** — 若反馈会改变当前画面，写新版本
- **每屏最多 2–4 个选项**
- **重要时用真实内容** — 摄影作品集应用真实图片（如 Unsplash）。占位内容会掩盖设计问题。
- **线框保持简单** — 聚焦版式与结构，不必像素级完美

## 文件命名

- 语义化命名：`platform.html`、`visual-style.html`、`layout.html`
- 不要复用文件名 — 每屏须为新文件
- 迭代时加版本后缀：`layout-v2.html`、`layout-v3.html`
- 服务器按修改时间提供最新文件

## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

若会话使用了 `--project-dir`，线框文件保留在 `.superpowers/brainstorm/` 供日后查看。仅 `/tmp` 会话在停止时删除。

## 参考

- 框架模板（CSS 参考）：`scripts/frame-template.html`
- 辅助脚本（客户端）：`scripts/helper.js`
