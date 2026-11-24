---
title: "03. 数学公式排版"
description: "实测 Sphinx + MyST 杀手级学术特性：$...$/$$...$$ 定界符、:label: 公式自动编号、{eq} 交叉引用与本地 MathJax 3 SVG。"
myst:
  html_meta:
    description: "实测 Sphinx + MyST 杀手级学术特性：$...$/$$...$$ 定界符、:label: 公式自动编号、{eq} 交叉引用与本地 MathJax 3 SVG。"
---

# 03. 数学公式排版（MyST 公式编号与 `{eq}` 交叉引用）

在学术论文、数值计算手册与机器学习文档领域，**Sphinx + MyST-Parser** 拥有绝大多数前端 SSG 难以企及的杀手级能力：**原生公式标签（`$$...$$ (label)` 或 `` ```{math} `` `:label:`）与编译期 `{eq}` 编号交叉引用校验**。本子站开启 `dollarmath` 与 `amsmath` 扩展，并将 `mathjax_path` 指向本地 `_static/vendor/tex-svg.js`（MathJax `3.2.1` 矢量 SVG 单文件包），彻底杜绝运行时外部 CDN 与字体请求。

## 1. 行内公式与中英文混排基线对齐

考察重点：行内公式在中文字号下的缩放比例、上下标是否撑乱行高，以及分数与根号在行内的紧凑度。

- 质能方程 $E = mc^2$ 与欧拉恒等式 $e^{i\pi} + 1 = 0$ 嵌入在连续中文段落中的视觉基线表现。
- 归并排序的平均时间复杂度为 $\mathcal{O}(n \log n)$，而空间复杂度为 $\Theta(n)$；当输入规模满足 $n \ge 2^{16}$ 时，常数因子差异显著。
- 贝叶斯条件概率公式行内排印：$P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}$，以及带根号的欧氏距离 $d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{i=1}^{n}(x_i - y_i)^2}$。

## 2. 多行等式对齐推导（`aligned` 环境 + `(eq-gaussian)` 标签）

启用 `myst_dmath_allow_labels = True` 后，只需在 `$$` 闭合行尾追加 `(eq-gaussian)`，Sphinx 即自动生成右侧公式序号并允许在正文任意位置通过角色 {eq}`eq-gaussian` 生成可点击跳转的编号链接：

$$
\begin{aligned}
I^2 &= \left( \int_{-\infty}^{+\infty} e^{-x^2}\,\mathrm{d}x \right) \left( \int_{-\infty}^{+\infty} e^{-y^2}\,\mathrm{d}y \right) \\
    &= \iint_{\mathbb{R}^2} e^{-(x^2 + y^2)}\,\mathrm{d}x\,\mathrm{d}y \\
    &= \int_{0}^{2\pi} \int_{0}^{+\infty} e^{-r^2} r\,\mathrm{d}r\,\mathrm{d}\theta \\
    &= 2\pi \cdot \left[ -\frac{1}{2} e^{-r^2} \right]_{0}^{+\infty} = \pi \implies I = \sqrt{\pi}
\end{aligned}
$$ (eq-gaussian)

## 3. 矩阵运算与注意力机制（`` ```{math} `` `:label:` 与 `bmatrix` 环境）

除美元符号外，MyST 同样支持标准 Sphinx `` ```{math} `` 指令并通过 `:label:` 声明锚点（如缩放点积注意力公式 {eq}`eq-attention` 与雅可比矩阵 {eq}`eq-jacobian`）：

```{math}
:label: eq-attention

\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
```

$$
\mathbf{J}_{\mathbf{f}}(\mathbf{x}) =
\begin{bmatrix}
\dfrac{\partial f_1}{\partial x_1} & \dfrac{\partial f_1}{\partial x_2} & \cdots & \dfrac{\partial f_1}{\partial x_n} \\[6pt]
\dfrac{\partial f_2}{\partial x_1} & \dfrac{\partial f_2}{\partial x_2} & \cdots & \dfrac{\partial f_2}{\partial x_n} \\[4pt]
\vdots & \vdots & \ddots & \vdots \\[4pt]
\dfrac{\partial f_m}{\partial x_1} & \dfrac{\partial f_m}{\partial x_2} & \cdots & \dfrac{\partial f_m}{\partial x_n}
\end{bmatrix}
$$ (eq-jacobian)

## 4. 分段函数与优化目标（`cases` 环境 + 跨公式汇总引用）

测试 Huber Loss 分段函数 {eq}`eq-huber` 与花括号对齐——回顾上文高斯积分推导 {eq}`eq-gaussian`、注意力权重 {eq}`eq-attention` 与雅可比矩阵 {eq}`eq-jacobian`，一旦删除或拼错任一标签名，`sphinx-build` 会在编译期直接抛出断链告警：

$$
\mathcal{L}_{\delta}(y, \hat{y}) =
\begin{cases}
\dfrac{1}{2}(y - \hat{y})^2, & \text{if } |y - \hat{y}| \le \delta, \\[8pt]
\delta \cdot \left(|y - \hat{y}| - \dfrac{1}{2}\delta\right), & \text{otherwise.}
\end{cases}
$$ (eq-huber)

## 5. 字面量美元符号 `\$` 转义边界测试

在启用 `$...$` 行内数学公式后，同一段落出现两个价格数字（例如基础套餐 \$29/月 与专业版 \$99/月）时，若未正确转义 `\$` 会把中间的中文误解析为斜体公式；而在反引号代码片段中编写环境变量 `$HOME` 或 `awk '{print $1}'` 则应原样保留，无需反斜杠转义。
