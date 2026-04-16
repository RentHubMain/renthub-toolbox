---
targets: ["*"]
globs: ["**/*"]
description: RentHub 管理后台项目开发规范
---

# RentHub 管理后台规范

## 1. 项目定位
管理后台使用 React + Vite + TypeScript，面向内部运营与管理人员。

## 2. 技术栈
- React 18
- Vite 5
- TypeScript（严格模式）
- Zustand
- React Router v6
- Axios、Day.js、Recharts、Lucide React

## 3. 目录约定
- src/components：通用组件
- src/pages：页面与业务模块
- src/services：接口与请求封装
- src/store：状态管理
- src/types：全局类型定义

## 4. 开发命令
- npm install
- npm run dev
- npm run lint
- npm run build

## 5. 实施规范
- 请求统一经 src/services，不在页面直接散落调用。
- 路由集中管理，页面按功能分目录。
- 复杂类型放入 src/types，避免组件内堆叠类型定义。
- 保持 UI 组件可复用，避免一次性组件泛滥。

## 6. 提交前检查
- 本地通过类型检查与构建。
- 不提交 dist、node_modules、.env。
- 涉及接口改动时说明影响页面与回归范围。
