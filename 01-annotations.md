---
title: "01. 专属标注与元数据"
description: "实测 Sphinx 9.1 + MyST-Parser 5.2 的 Docutils 元数据、{note}/:::{admonition} 双轨指令、{dropdown} 与 GFM Alerts 原生解析。"
myst:
  html_meta:
    description: "实测 Sphinx 9.1 + MyST-Parser 5.2 的 Docutils 元数据、{note}/:::{admonition} 双轨指令、{dropdown} 与 GFM Alerts 原生解析。"
---

# 01. 专属标注与元数据（MyST 指令角色体系）

不同静态网站生成器对“提示框 / 标注（Callouts / Admonitions）”和页面元数据的语法约定存在显著分歧。本文件由标准 GFM 母版派生适配至 **Sphinx (`9.1.1`) + MyST-Parser (`5.2.0`)** {bdg-primary}`Docutils AST` {bdg-success}`MyST 5.2`。

## 1. Frontmatter 元数据机制（Docutils `docinfo` 与 `myst.html_meta`）

不同于把 YAML `title` 直接当作网页一级标题的轻量 SSG，Sphinx 严格区分**文档章节树标题（由首个 `# H1` 决定）**与**文档级元数据（`env.metadata`）**：

- **顶层 YAML 字段**：`title: "01. 专属标注与元数据"` 与 `description: "..."` 会被 MyST 转换为 Docutils `field_list` 并存入 Sphinx 编译环境的 `env.metadata[docname]`（默认不污染正文渲染；若需屏蔽未入树单页可声明 `orphan: true`）。
- **HTML `<meta>` 注入**：通过嵌套 `myst.html_meta` 字典即可在构建期精确生成 `<meta name="description" content="...">` 标签。
- **行内角色（MyST Roles）**：启用 `attrs_inline` 与 `sphinx-design` 后，无需混写 JSX/Vue 组件，直接用 `` {bdg-primary}`标签` `` 即可输出语义化行内徽章。

## 2. 标准提示语义块（MyST `` ```{directive} `` 与 `:::` 冒号围栏双轨语法）

MyST（Markedly Structured Text）的核心设计是将 reStructuredText 强大的 `.. note::` 指令无损映射为反引号指令围栏 `` ```{note} ``（或开启 `colon_fence` 后的 `:::{admonition}`）：

```{note}
默认信息提示块：静态站点对比平台的每个子模块均独立维护 `main`（源码）与 `page`（构建产物）双分支，互不污染提交历史。
```

:::{admonition} 性能优化建议（自定义标题语义）
:class: tip

在 MyST 体系中，标准 `` ```{tip} `` 指令自动生成本地化“提示”标题；若需**完全自定义标题文本**并复用 `tip` 视觉样式，地道写法是使用冒号围栏 `:::{admonition} 自定义标题` 并附带 `:class: tip` 选项。
:::

```{warning}
**版本边界注意**：注意区分各派系关键字命名——Sphinx / Docutils 内置完整九类语义告示（`attention`、`caution`、`danger`、`error`、`hint`、`important`、`note`、`tip`、`warning`），远比普通前端文档框架丰富。
```

```{danger}
**不可逆分支覆盖警告**：自动化流水线在向 `page` 分支推送构建产物时会启用 `force_orphan: true`，切勿在 `page` 分支直接手工修改代码！
```

## 3. 可折叠详情容器（`sphinx-design` `{dropdown}` 与原生 `<details>`）

在科研文档中，既可使用 `sphinx-design` 提供的带图标配色 `:::{dropdown}` 指令，也可直接使用标准 HTML `<details>` 与 `<summary>` 标签：

::::{dropdown} 点击展开查看 MyST 折叠容器源码结构（`{dropdown}` 指令）
:color: info

```markdown
:::{admonition} 自定义标题
:class: tip

支持任意嵌套代码块、列表、表格与行内公式 $f(x) = x^2 + 1$。
:::
```

除了代码块，折叠容器内同样支持列表、表格与数学公式 $f(x) = x^2 + 1$（注：外层冒号围栏嵌套含 `:::` 的代码块时，外层须递增为四冒号 `::::{dropdown}` 以防提前闭合！）。
::::

<details>
<summary>点击展开对比原生 HTML &lt;details&gt; 直通表现</summary>

原生 HTML `<details>` 标签在 MyST-Parser 中同样无需额外插件即可保留折叠交互，内部行内公式 $g(x) = e^{-x^2}$ 也能由本地 MathJax 3 正常渲染。

</details>

## 4. GitHub 风格引用警报（GFM Alerts）跨框架直通测试

以下三段**保持母版原文一字不改**。实测惊喜发现：在 **`myst-parser 5.2.0`（底层 `mdit-py-plugins 0.7.0`）** 中，官方已内置 `"alert"` 扩展！只需在 `conf.py` 的 `myst_enable_extensions` 中加入 `"alert"`，下方五类 GitHub 警报即可零改造自动映射为原生 Docutils 告示节点（`nodes.note` / `nodes.important` / `nodes.caution`）：

> [!NOTE]
> 这是一段标准的 GitHub Flavored Markdown `[!NOTE]` 警报文本，用于检验各生成器对母版语法的零改造直通能力。

> [!IMPORTANT]
> 跨平台迁移 Markdown 文档时，是否原生兼容 `> [!IMPORTANT]` 与 `> [!WARNING]` 直接决定了母版文档的派生改造成本。

> [!CAUTION]
> 若目标生成器未内置 GFM Alert 解析器（如 VuePress v1、Starlight 默认配置、Docsify v4 旧插件），上方标记会退化为普通引用块并原样露出 `[!CAUTION]` 字符串。
