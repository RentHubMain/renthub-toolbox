---
targets: ["*"]
globs: ["**/*"]
description: RentHub 文档站项目开发规范
---

# RentHub 文档站规范

## 1. 项目定位
文档站基于 Docusaurus 3，承载产品、研发、设计、管理与法律等文档内容。

## 2. 技术栈
- Docusaurus 3（React + MDX）
- TypeScript（配置与主题扩展）
- Markdown（文档正文）
- npm 构建与部署流程

## 3. 目录约定
- docs：文档内容主目录
- src/pages：站点页面
- src/theme：主题覆盖与 swizzle 组件
- src/css：全站样式
- static 与 assets/images：静态资源

## 4. 文档写作规范
- 全部使用中文，术语可保留英文原词。
- 每篇文档必须包含 front matter 与 title。
- 章节结构优先：概述、主体说明、示例、注意事项。
- 文档链接使用站点绝对路径，避免相对路径漂移。

## 5. 导航维护规范
- 新增文档后同步更新父级索引与侧边栏。
- 新增板块后同步更新首页入口、侧边栏与必要导航配置。
- 重命名文件时同步修复所有引用链接。

## 6. 本地验证
- npm install
- npm start
- npm run build
- npm run serve

## 7. 提交前检查
- 构建通过且无断链。
- 目录结构与侧边栏一致。
- 不引入无效链接或过期版本指向。
