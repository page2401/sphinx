---
title: "00. 概览与版本档案 (Sphinx + MyST)"
description: "Python 科研与标准规范出版基石 Sphinx 9.1.1 + MyST-Parser 5.2.0 + Furo 2025.12.19 基准实测子站。"
myst:
  html_meta:
    description: "Python 科研与标准规范出版基石 Sphinx 9.1.1 + MyST-Parser 5.2.0 + Furo 2025.12.19 基准实测子站。"
---

# 00. 概览与版本档案（Sphinx + MyST 科学出版基准）

本子站（`sites/sphinx`）由 `page2401.github.io/docs/` 标准 GFM 母版派生适配至 **Python 科学计算与官方文档统治级引擎 Sphinx (`9.1.1`) + MyST-Parser (`5.2.0`) + Furo (`2025.12.19`)**。从 Python 官方文档、Linux 内核文档到 Jupyter Book / SciPy / PyTorch 学术生态，Sphinx 凭借底层 **Docutils 抽象语法树（Doctree AST）** 与编译期全局符号交叉引用体系独树一帜。

## 精确锁定依赖栈（Zero-CDN 纯本地闭环）

| 组件角色 | 包名 / 静态资源 | 锁定版本 | 核心职责说明 |
| :--- | :--- | :--- | :--- |
| 核心文档编译器 | `sphinx` | `9.1.1` | 基于 Docutils `0.22.4` 构建跨文档 `{toctree}`、公式编号与全局符号索引 |
| 科学 Markdown 解析器 | `myst-parser` | `5.2.0` | 基于 `markdown-it-py@4.3.0` 将 Markdown 角色/指令无损编译为 Docutils AST |
| 现代双栏自适应主题 | `furo` | `2025.12.19` | 零外部字体请求、原生亮暗色切换与粘性页内目录树 |
| 交互组件扩展 | `sphinx-design` | `0.8.0` | 提供 `{dropdown}` 折叠面板、网格卡片与 `{bdg-*}` 行内徽章角色 |
| 图表指令扩展 | `sphinxcontrib-mermaid` | `2.1.1` | 解析 `` ```{mermaid} `` 指令并桥接本地 `_static/vendor/mermaid.min.js` (`12.3.0`) |
| 数学排版引擎 | `sphinx.ext.mathjax` | `3.2.1` (Local) | 重定向 `mathjax_path = "vendor/tex-svg.js"` 至本地单文件 SVG 引擎，零 CDN 请求 |

## 母版六大标准章节派生对照

| 章节路径 | 测试维度 | 母版中立 GFM 语法 | Sphinx + MyST 派生改造与核心看点 |
| :--- | :--- | :--- | :--- |
| {doc}`01-annotations` | 专属标注与元数据 | YAML 头、`> [!NOTE]`、`<details>` | 反引号 `` ```{note} `` 与冒号围栏 `:::{admonition}` 双轨指令、`:::{dropdown}` 折叠块；开启 `alert` 扩展后原生直通五类 GFM Alerts |
| {doc}`02-diagrams` | 流程图与时序图 | ```` ```mermaid ```` 围栏代码块 | 科学出版风格 `` ```{mermaid} `` 指令（兼开 `myst_fence_as_directive` 兼容原样代码块）+ 本地 Mermaid `12.3.0` |
| {doc}`03-math` | 数学公式排版 | `$...$` 与 `$$...$$` | **杀手级学术特性**：公式自动编号 `:label:` / `(eq-id)` 与 `{eq}` 跨段交叉引用 + 本地 MathJax 3 SVG |
| {doc}`04-directory/index` | 目录结构与路由取舍 | `04-directory/index.md` + `nested/` | 强约束显式 `` ```{toctree} `` 编译树 + `{doc}` / `{ref}` 编译期死链强校验 + `dirhtml` 相对路径资产免 `basePath` |
| {doc}`05-code-blocks` | 高阶代码块与语法高亮 | ```` ```ts ````、```` ```diff ````、平铺列表 | Docutils 标准 `` ```{code-block} `` 指令（`:caption:`、`:linenos:`、`:emphasize-lines:`、`:name:` 交叉引用）+ `sphinx-design` `{tab-set}` 标签页 |

```{toctree}
:maxdepth: 2
:caption: 基准测试章节导航

00. 概览与版本档案 <self>
01-annotations
02-diagrams
03-math
04-directory/index
05-code-blocks
```
