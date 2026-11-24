---
title: "嵌套子页 A：排序前缀与 URL 纯净度权衡"
---

(sec-order-and-url)=
# 嵌套子页 A：排序前缀与 URL 纯净度权衡

在母版目录 `docs/04-directory/nested/` 中，文件名使用 `01-order-and-url.md` 以保证在 Git 与代码编辑器中按阅读先后顺序排列。在 Sphinx 体系中，章节阅读顺序与底部“上一篇 / 下一篇”翻页流**100% 由父级 `` ```{toctree} `` 中的书写顺序决定**，完全不依赖文件名前缀或 Frontmatter `order` 数字；配合 `dirhtml` 构建器，本页静态资源通过相对路径 `../../../_static/` 自动寻址，无需任何全局 `basePath` 重写配置。

- [返回母版《04. 目录结构与路由取舍》](../index.md)（或使用语义锚点 {ref}`sec-directory-overview`）
- [下一篇：《嵌套子页 B：多级子目录与侧边栏同步机制》](./02-sidebar-sync.md)（或使用角色 {doc}`02-sidebar-sync`）
