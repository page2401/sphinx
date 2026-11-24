---
title: "04. 目录结构与路由取舍"
description: "实测 Sphinx 显式 {toctree} 编译树契约、{doc}/{ref} 编译期交叉校验与 dirhtml 相对静态路径优势。"
myst:
  html_meta:
    description: "实测 Sphinx 显式 {toctree} 编译树契约、{doc}/{ref} 编译期交叉校验与 dirhtml 相对静态路径优势。"
---

(sec-directory-overview)=
# 04. 目录结构与路由取舍（Sphinx 显式 `{toctree}` 契约）

将母版 `docs/04-directory/` 的多级嵌套目录派生至 **Sphinx + MyST-Parser** 时，展现出了与前端文件系统路由（File-system Routing）截然不同的**出版级整书树（Doctree）哲学**：

1. **拒绝隐式猜测的显式 `{toctree}` 编译契约**：Sphinx 不会按字母序盲目把文件夹扫成侧边栏。每一篇文档都必须被某个父级 `` ```{toctree} `` 指令显式收录——否则编译器立刻发出 `WARNING: document isn't included in any toctree` 告警！因此仓库根目录的工程说明 `README.md` 需列入 `conf.py` 的 `exclude_patterns`（或为刻意独立的单页标注 `orphan: true`），从根本上消灭了 VitePress / Starlight 中常见的“隐形孤岛页”事故。
2. **双轨内部互链（标准 `.md` 相对路径 + `{doc}` / `{ref}` 语义角色）**：
   - 保留母版写法 `[...](./nested/01-order-and-url.md)` 时，MyST 会在编译期校验目标文件存在性并自动将其重写为 `dirhtml` 干净路径 `nested/01-order-and-url/`；
   - 使用 Sphinx 原生角色 {doc}`nested/01-order-and-url` 或跨页命名锚点 {ref}`sec-sidebar-sync` 时，甚至**无需硬编码链接文字**——目标文档一旦修改 `# H1` 标题，全站所有引用处的显示文本在下次构建时自动同步更新！
3. **`dirhtml` 构建器的天然子路径无关性（免配 `basePath`）**：执行 `sphinx-build -b dirhtml . _build/dirhtml` 后，Sphinx 为每个页面计算精确的相对静态前缀（如首页引用 `_static/...`、二级目录引用 `../_static/...`、三级目录引用 `../../_static/...`）。这意味着构建产物无需绑定域名根路径，直接挂载到 `/sphinx/` 或任意子路径即可零报错运行（注意在 GitHub Pages 部署时必须创建 `.nojekyll`，否则下划线开头的 `_static/` 目录会被 Jekyll 拦截导致样式 404！）。

## 母版嵌套子文档入口（相对 `.md` 链接与 `{doc}` 角色对照）

- 母版 `.md` 相对路径写法：[进入子文档 A：排序前缀与 URL 纯净度权衡](./nested/01-order-and-url.md)
- 母版 `.md` 相对路径写法：[进入子文档 B：多级子目录与侧边栏同步机制](./nested/02-sidebar-sync.md)
- Sphinx `{doc}` 自动提取标题角色：{doc}`nested/01-order-and-url` · {doc}`nested/02-sidebar-sync`

```{toctree}
:maxdepth: 1
:caption: 嵌套子章节 (nested)

nested/01-order-and-url
nested/02-sidebar-sync
```
