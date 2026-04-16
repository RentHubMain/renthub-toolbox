---
name: ui-ux-pro-max
description: 基于内置数据集快速生成可落地的 UI/UX 设计系统与实现建议。
targets: ["*"]
---

# ui-ux-pro-max

## 适用场景
用户要求设计、实现、优化、评审 UI/UX 时使用（Web/移动端均可）。

## 必要输入
- 产品类型（SaaS、电商、门户、仪表盘等）
- 行业/场景（医疗、金融、教育等）
- 风格关键词（如 minimal、professional、playful）
- 技术栈（未指定时默认 `html-tailwind`）

## 标准流程
1. 先生成设计系统（必选）
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product> <industry> <keywords>" --design-system -p "<Project Name>"
```
2. 需要跨会话复用时，持久化
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "<Project Name>"
```
3. 需要细化时，按域补充检索
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <product|style|typography|color|landing|chart|ux|react|web|prompt>
```
4. 输出栈相关实现建议（默认 `html-tailwind`）
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack <html-tailwind|react|nextjs|vue|svelte|swiftui|react-native|flutter|shadcn|jetpack-compose>
```

## 输出要求
至少包含：
- 设计方向（pattern/style）
- 色板与字体组合
- 页面结构与关键组件
- 交互/动效与可访问性要求
- 反模式（需要避免的问题）
- 技术栈落地要点

## 质量检查
- 不用 emoji 充当 UI 图标，统一 SVG 图标集。
- 交互元素具备 hover/focus 状态与 `cursor-pointer`。
- 亮色模式对比度达标，避免低可读文本。
- 验证 375/768/1024/1440 四档响应式，无横向滚动。
- 尊重 `prefers-reduced-motion`。

## 备注
- 输出格式可选：默认终端样式；文档场景可加 `-f markdown`。
- 若首轮结果不匹配，优先换关键词再检索。
