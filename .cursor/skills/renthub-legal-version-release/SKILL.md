---
name: renthub-legal-version-release
description: 在 `renthub-docs/legal/` 协议定稿后发布新版本：归档旧版、升级现行版、更新导航与配置并验证构建。
---
# 法律文档版本发布（renthub-legal-version-release）

## 适用场景

当 `renthub-docs/legal/` 协议修订完成，需要发布新版本并保留历史版本时使用。

## 必要输入

- 旧版本号（如 `0.0.2`）
- 新版本号（如 `0.0.3`）
- 生效日期（`YYYY-MM-DD`）

## 标准流程

1. 归档旧版本

```bash
npx docusaurus docs:version:legal <旧版本号>
```

2. 修正归档副本（`legal_versioned_docs/version-<旧版本号>/`，不含 `index.md`）

- `status` 统一为 `archived`
- 顶部提示改为“历史版本（已失效）”，并指向 `/legal`

3. 修正归档首页链接（`index.md`）

- 目录链接改为 `/legal/<旧版本号>/<doc-slug>`，避免跳回现行版

4. 升级现行 `legal/` 协议（不含 `index.md`）

- front matter 更新为新版本号与生效日期
- 顶部提示改为“当前版本（现行有效）”

5. 更新配置

- `docusaurus.config.ts` 中 legal 插件 `versions.current.label = <新版本号>`
- Navbar 的现行入口固定为 `/legal/`
- Navbar 增加旧版本入口 `/legal/<旧版本号>/`

6. 构建验证

```bash
npm run build
```

## 输出要求

返回发布摘要，至少包含：

- 新增归档目录与 sidebar 文件
- `legal_versions.json` 更新
- 现行 `legal/` 元数据升级
- `docusaurus.config.ts` 与 navbar 更新
- 构建结果（成功/失败）

## 约束

- 未拿到 3 项必要输入前，不执行发布步骤。
- 不修改协议正文语义，仅处理版本化与导航一致性。
- 若构建失败，先报告错误并给出修复建议，再等待确认。
