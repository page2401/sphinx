---
title: "嵌套子页 B：多级子目录与侧边栏同步机制"
---

(sec-sidebar-sync)=
# 嵌套子页 B：多级子目录与侧边栏同步机制

不同于把全站侧边栏集中塞进单一根配置文件的做法（如 `mkdocs.yml` 或 `.vitepress/config.mts`），Sphinx 采用**分布式 `{toctree}` 组合树**：顶层 `index.md` 仅需收录 `04-directory/index`，而子目录内部的层级与中文分组标题 `:caption: 嵌套子章节 (nested)` 由 `04-directory/index.md` 自治声明。一旦新增文件忘记写入任何 `{toctree}`，编译器立即告警拦截，彻底兼顾模块化自治与零孤岛页保障。

- [返回上一篇：《嵌套子页 A：排序前缀与 URL 纯净度权衡》](./01-order-and-url.md)（或使用语义锚点 {ref}`sec-order-and-url`）
- [返回母版《04. 目录结构与路由取舍》](../index.md)（或使用角色 {doc}`../index`）
