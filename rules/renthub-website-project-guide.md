---
targets: ["*"]
globs: ["**/*"]
description: RentHub 官方网站项目开发规范
---

# RentHub 官网规范

## 1. 项目定位
官网为品牌与营销站点，强调信息展示、转化引导与多语言体验。

## 2. 技术栈
- React 18 + Vite 5
- TypeScript
- Tailwind CSS 与组件级 CSS
- React Router
- 动效库与滚动交互能力

## 3. 目录约定
- src/components：页面区块组件
- src/i18n：多语言资源与逻辑
- src/utils：工具函数
- App 与 main：布局与入口
- public：静态资源

## 4. 开发规范
- 路由保持语言前缀一致。
- 样式分层清晰，避免全局样式污染。
- 资源路径与别名使用统一。
- 动效优先服务信息层级，不做干扰性动画。

## 5. 常用命令
- npm install
- npm run dev
- npm run build
- npm run preview

## 6. 部署规范
- 默认使用静态托管发布 dist。
- Docker 部署时确保 SPA 路由回退配置正确。
- 发布前核对多语言路由与 SEO 关键页面。

## 7. 提交前检查
- 本地构建通过。
- 不提交 dist、node_modules 与敏感配置。
- 关键页面在移动端与桌面端均完成可用性检查。
