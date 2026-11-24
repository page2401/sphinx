---
title: "05. 高阶代码块与语法高亮"
description: "实测 Sphinx 9.1 + MyST-Parser 5.2 + Pygments 2.21 + sphinx-design 0.8 的 {code-block} 指令（:caption: / :linenos: / :emphasize-lines:）与 {tab-set} 标签页。"
myst:
  html_meta:
    description: "实测 Sphinx 9.1 + MyST-Parser 5.2 + Pygments 2.21 + sphinx-design 0.8 的 {code-block} 指令（:caption: / :linenos: / :emphasize-lines:）与 {tab-set} 标签页。"
---

# 05. 高阶代码块与语法高亮（MyST `{code-block}` + `{tab-set}`）

技术文档中超过 40% 的篇幅由代码块构成，但标准 CommonMark / GitHub Flavored Markdown **仅定义了围栏语言标识（```` ```ts ````）**，并未定义文件名标题栏、指定行高亮、带语法着色的行级 Diff 以及多语言 Tab 代码组。本文件由标准 GFM 母版派生适配至 **Sphinx (`9.1.1`) + MyST-Parser (`5.2.0`) + Pygments (`2.21.0`)** {bdg-primary}`Pygments 2.21` {bdg-info}`sphinx-design`。

## 1. 代码块文件名标题栏与基础语法高亮（`{code-block}` 指令）

不同于前端框架在围栏首行拼接 `title="..."` 的非标写法，Sphinx + MyST 将代码块视为一等公民的学术出版构件——使用 ```` ```{code-block} ts ```` 指令配合 `:caption:`、`:linenos:`、`:emphasize-lines:` 乃至 `:name:`（支持在正文中通过 {ref}`code-resolve-route` 编译期交叉引用该代码清单！）：

````{code-block} ts
:caption: scripts/resolve-route.ts
:name: code-resolve-route
:linenos:
:emphasize-lines: 3,7-9

export interface RouteContext {
  basePath: string
  slug: string
  cleanUrls: boolean
}

export function formatDocRoute(ctx: RouteContext): string {
  const prefix = ctx.basePath.endsWith('/') ? ctx.basePath : `${ctx.basePath}/`
  const normalized = ctx.slug.replace(/^\/+|\/+$/g, '')
  if (!normalized || normalized === 'index') return prefix
  return ctx.cleanUrls ? `${prefix}${normalized}/` : `${prefix}${normalized}.html`
}
````

## 2. 关键行聚焦与高亮（`:emphasize-lines: 3,7-9`）

当需要在长配置中引导读者注意第 `3` 行与第 `7–9` 行时，Docutils / Sphinx 原生 `:emphasize-lines: 3,7-9` 选项在构建期直接向 Pygments 传递 `hl_lines=[3, 7, 8, 9]`，并支持 `:lineno-start:` 自定义起始行号（若区间越界，Sphinx 编译器会直接抛出构建告警以防文档重构后行号漂移）：

```{code-block} json
:caption: bench.config.json
:linenos:
:emphasize-lines: 3,7-9

{
  "id": "ssg-benchmark",
  "routeStyle": "clean",
  "strictZeroCdn": true,
  "markdown": {
    "mathEngine": "katex",
    "diagramEngine": "mermaid",
    "lineHighlight": true,
    "codeTransformers": ["diff", "focus"]
  }
}
```

## 3. 代码增删对比着色（Pygments `diff` 词法着色）

标准 GFM 使用独立的 `diff` 语言标识表达补丁增删；Sphinx 底层调用 Pygments `DiffLexer` 直接兼容原样 ```` ```diff ```` 围栏（或升级为带 `:caption:` 的 `{code-block} diff`），在 Furo 亮暗双主题下自动呈现高对比红绿增删背景：

```{code-block} diff
:caption: scripts/mount-subsite.patch

 export function mountSubsite(baseDir: string, subPath: string): string | null {
-  const cleanRel = decodeURIComponent(subPath).replace(/\.\./g, '')
-  return `${baseDir}/${cleanRel}`
+  const resolvedBase = path.resolve(baseDir)
+  const target = path.resolve(resolvedBase, decodeURIComponent(subPath).replace(/^\/+/, ''))
+  return target.startsWith(`${resolvedBase}${path.sep}`) ? target : null
 }
```

## 4. 多语言运行时命令组（`sphinx-design` `::::{tab-set}`）

借助官方生态标配的 `sphinx-design` 扩展与 MyST `colon_fence` 语法，使用外层四冒号 `::::{tab-set}` 嵌套内层三冒号 `:::{tab-item}`（还可追加 `:sync: node` 实现整站同名标签联动切换），编译为纯 CSS `<input type="radio">` 无脚本交互组件：

::::{tab-set}

:::{tab-item} Node.js
:sync: node

```bash
npm ci && npm run build
```
:::

:::{tab-item} Deno 2
:sync: deno

```bash
deno task build
```
:::

:::{tab-item} Python
:sync: python

```bash
pip install -r requirements.txt && sphinx-build -b dirhtml . _build/dirhtml
```
:::

:::{tab-item} Ruby
:sync: ruby

```bash
bundle install && bundle exec jekyll build
```
:::

::::

## 5. 四大底层高亮引擎能力对照小结

| 高亮引擎代表 | 典型采用框架 | 构建期零运行时 JS | 原生行号 / 行高亮 | 保留词法着色的 Diff |
| :--- | :--- | :--- | :--- | :--- |
| **Shiki / Expressive Code** | VitePress、Starlight、Fumadocs、Nextra、Rspress、Nuxt、Quartz | ✅ 纯静态内联样式 | ✅ `{1,3-5}` / `[!code highlight]` | ✅ `// [!code ++]` |
| **Prism.js** | Docusaurus、VuePress、Eleventy (plugin)、Gatsby | ✅ 静态 Token 类名 | ✅ `{1,3-5}` / 魔法注释 | ⚠️ 需配 diff-highlight 插件 |
| **Pygments / Rouge** | MkDocs Material、Sphinx、Pelican、Jekyll | ✅ Python/Ruby 编译直出 | ✅ `hl_lines` / `emphasize-lines` | ⚠️ 仅标准 `diff` 块红绿 |
| **Chroma / Giallo / hljs** | Hugo (Go Chroma)、Zola (Rust Giallo)、mdBook (hljs) | ✅ (mdBook 为客户端 hljs) | ✅ Hugo/Zola 原生 `hl_lines` | ⚠️ 仅标准 `diff` 块红绿 |
