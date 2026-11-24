---
title: "02. 流程图与时序图"
description: "实测 Sphinx + MyST 的 {mermaid} 指令、myst_fence_as_directive 兼容机制与零外部 CDN 本地 Mermaid 12.3 渲染。"
myst:
  html_meta:
    description: "实测 Sphinx + MyST 的 {mermaid} 指令、myst_fence_as_directive 兼容机制与零外部 CDN 本地 Mermaid 12.3 渲染。"
---

# 02. 流程图与时序图（MyST `{mermaid}` 指令基准）

在 Sphinx + MyST 体系中，接入 `sphinxcontrib-mermaid` 后不仅可以使用显式支持 `:align:`、`:caption:` 与交叉引用锚点的 **```` ```{mermaid} ```` 指令**，还可在 `conf.py` 配置 `myst_fence_as_directive = ["mermaid"]` 兼容母版原生 ```` ```mermaid ```` 围栏。本子站更进一步通过 `mermaid_use_local` 将默认指向 `cdn.jsdelivr.net` 的模块入口重定向至本地 `_static/vendor/mermaid.min.js`（`12.3.0`），实现 100% 离线零外部 CDN 请求渲染。

## 1. 复杂子图与架构流程图（`flowchart TD`）

测试中文节点标签、子图嵌套（`subgraph`）、虚线边与条件分支：

```{mermaid}
:caption: 图 2-1：主仓库母版与 Sphinx 独立子仓库双分支发布拓扑

flowchart TD
    subgraph MainRepo["主仓库 page2401.github.io"]
        Master["母版 docs/*.md (Pure GFM)"]
        SubPtr["Git Submodule 指针 (sites/*)"]
        Workbench["对比工作台源码 (main)"]
    end

    subgraph SubRepo["各独立派生子仓库 (sites/<id>)"]
        SrcBranch["main 分支: 框架配置 + 派生适配版 *.md"]
        Actions{"GitHub Actions 构建"}
        PageBranch["page 孤儿分支: 纯静态产物 + .nojekyll"]
        SrcBranch --> Actions
        Actions -->|"自动构建发布"| PageBranch
    end

    Master -.->|"按各框架方言派生"| SrcBranch
    SubPtr -.->|"跟踪 main 分支"| SrcBranch
    Workbench -->|"对比母版与各派生版差异"| Portal["https://page.2401.xyz/"]
    PageBranch -->|"GitHub Organization Pages"| SubSite["https://page.2401.xyz/<id>/"]
```

## 2. 编译管线交互时序图（`sequenceDiagram`）

测试多参与者生命线、`alt` 分支块及激活框（`activate`/`deactivate`）：

```{mermaid}
:caption: 图 2-2：编译期 SSG 与运行时引擎构建发布交互时序

sequenceDiagram
    autonumber
    actor Author as 文档作者
    participant Master as 主仓母版 docs/*.md
    participant SubGit as 子模块 main 分支
    participant CI as GitHub Actions (Python 3.12 / Node 22)
    participant Pages as GitHub Pages (page 分支)

    Author->>Master: 编写标准 GFM 基准母版
    Master->>SubGit: 派生适配特定 SSG 版本语法
    SubGit->>CI: 触发 deploy-page.yml 工作流
    activate CI
    alt 编译型 SSG (Sphinx / VitePress / Starlight)
        CI->>CI: 预编译静态 HTML + 公式 + 图表挂载点
    else 运行时引擎 (Docsify v4 / v5)
        CI->>CI: 组装原始 *.md + _sidebar.md + 锁定版本 vendor
    end
    CI->>Pages: force_orphan 推送至孤儿分支 page
    deactivate CI
    Pages-->>Author: 同源子路径 /<id>/ 即刻生效
```

## 3. 子模块同步状态机（`stateDiagram-v2`）

测试状态机语法与状态迁移说明标签：

```{mermaid}
:caption: 图 2-3：母版更新驱动的子模块同步生命周期状态机

stateDiagram-v2
    [*] --> MasterEdited: 更新主仓母版 docs/*.md
    MasterEdited --> SubmoduleDerived: 同步派生适配至各子模块 *.md
    SubmoduleDerived --> SubmodulePushed: 子模块 commit & push origin main
    SubmodulePushed --> PageDeploying: 子仓库 Actions 自动更新 page 分支
    SubmodulePushed --> MainRepoUpdated: 主仓库更新子模块指针并构建对比数据
    PageDeploying --> LiveSynced: 线上渲染与母版源码差异视图全部就绪
    MainRepoUpdated --> LiveSynced: 计算相对母版改动行数完成
    LiveSynced --> [*]
```
