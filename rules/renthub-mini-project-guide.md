---
targets: ["*"]
globs: ["**/*"]
description: RentHub 微信小程序项目开发规范
---

# RentHub 微信小程序规范

## 1. 项目定位
微信小程序主工程，包含前端小程序与 CloudBase 云函数。

## 2. 技术栈
- 微信原生框架（WXML、WXSS、JavaScript）
- CloudBase 云函数
- Jest（单测与 E2E）

## 3. 目录约定
- miniprogram：小程序前端
- cloudfunctions：云函数集合
- cloudfunctions/_shared：云函数共享能力
- shared/contracts：共享数据合约
- tests：测试代码

## 4. 开发规范
- 云函数公共能力统一沉淀到 _shared。
- 鉴权逻辑复用统一模块，避免重复实现。
- 合约变更同步更新调用方与测试。
- 页面逻辑遵循小程序生命周期约定。

## 5. 常用命令
- npm install
- npm test
- npm run test:e2e
- 云函数子目录按需单独安装依赖

## 6. 提交前检查
- 核心流程相关云函数具备最小测试覆盖。
- 不提交敏感配置与云函数依赖目录。
- 不提交小程序构建产物与本地私有配置。
