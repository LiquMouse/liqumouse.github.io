---
title: math-test
date: 2026-10-28 17:28:32
tags:
---

> 数学公式渲染测试页：覆盖行内/行间公式、常见 LaTeX 环境、Markdown 转义边界与扩展语法。构建后所有公式应为构建期生成的 SVG。

## 1. 行内公式

- 基础：$E = mc^2$
- 上下标：$x_1^2 + x_{i,j}^{n+1}$
- 希腊字母：$\alpha,\ \beta,\ \gamma,\ \Delta,\ \Omega$
- 常用符号：$\infty,\ \partial,\ \nabla,\ \forall,\ \exists,\ \emptyset$
- 分式：$\frac{a}{b}$、$\dfrac{a}{b}$、$\tfrac{a}{b}$
- 根式：$\sqrt{x}$、$\sqrt[3]{x}$
- 求和/积分/极限/连乘：$\sum_{i=1}^{n} i$、$\int_0^1 f(x)\,\mathrm{d}x$、$\lim_{x\to 0}\frac{\sin x}{x}$、$\prod_{k=1}^{n} k$
- 括号：$\left( \frac{a}{b} \right)$、$\left[ x \right]$、$\left\{ x \right\}$、字面大括号 $\{1,2,3\}$
- 关系符：$a \to b$、$a \Rightarrow b$、$x \neq y$、$x \leq y$、$x \geq y$、$x \approx y$、$x \equiv y$
- 重音与向量：$\vec{v}$、$\hat{x}$、$\bar{x}$、$\tilde{x}$、$\dot{x}$、$\ddot{x}$
- 字体：$\mathrm{d}x$、$\mathbf{A}$、$\mathcal{F}$、$\mathbb{R}$、$\boldsymbol{\alpha}$、$\text{中文 text}$
- 上下括号：$\underbrace{a+b}_{c}$、$\overbrace{a+b}^{c}$
- 组合与算子：$\binom{n}{k}$、$\operatorname{sgn}(x)$
- 定界符：$\lvert x \rvert$、$\lVert x \rVert$、$|x|$、$\|x\|$
- 区间与集合：$x \in [0,1]$、$\{x \mid x > 0\}$、$f^{-1}(x)$
- 上下标细节：$a~b$、$\sum\limits_{i=1}^{n} i$、$\sum_{\substack{i=1\\j=1}}^{n} a_{ij}$
- Markdown 敏感字符：$a*b*c$、$a_b$、$a\_b$、$a < b > c$、$a<b>c$、$a \& b$
- 转义字符：$\{ \} \_ \% \& \# \$ \backslash$
- 多个公式同行：$a$、$b$、$c$，以及紧贴中文：中文$x^2$中文。
- `\displaystyle` 行内：$\displaystyle \sum_{i=1}^{n} \frac{1}{i^2}$
- 行内 aligned：$\begin{aligned} a &= b \\ c &= d \end{aligned}$
- 行内 smallmatrix：$\left(\begin{smallmatrix} a & b \\ c & d \end{smallmatrix}\right)$
- Unicode 输入：$α + β = γ$
- 圆括号定界符：\(a^2 + b^2 = c^2\)、\(\begin{aligned} a &= b \\ c &= d \end{aligned}\)
- 源码跨行的行内公式（段落内换行）：

  $a +
  b = c$ 结束。

- 紧贴标点：$(a,b]$，$x=1$。

## 2. 行间公式

### 2.1 `$$ ... $$`

$$
f(x) = f(x_0) + f'(x_0)(x-x_0) + \frac{f''(x_0)}{2!}(x-x_0)^2 + \cdots
$$

### 2.2 `\[ ... \]`

\[
\int_{-\infty}^{+\infty} e^{-x^2}\,\mathrm{d}x = \sqrt{\pi}
\]

### 2.3 裸 `\begin{align} ... \end{align}`

\begin{align}
a &= b + c \\
d &= e - f \\
g &= h \cdot i
\end{align}

### 2.3.1 裸 `align*`

\begin{align*}
a &= b + c \\
d &= e - f
\end{align*}

### 2.4 `align`（包在 `$$` 内）

$$
\begin{align}
a &= b \\
x &= y
\end{align}
$$

### 2.5 `aligned`

$$
\begin{aligned}
f(x) &= x^2 \\
g(x) &= x + 1
\end{aligned}
$$

### 2.6 `gather`

$$
\begin{gather}
a + b = c \\
d + e = f
\end{gather}
$$

### 2.7 `cases`

$$
f(x) =
\begin{cases}
x^2, & x \ge 0, \\
-x,  & x < 0.
\end{cases}
$$

### 2.8 `equation` + `split`

\begin{equation}
\begin{split}
a &= b + c \\
  &= d + e
\end{split}
\end{equation}

### 2.9 矩阵

$$
A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix},\quad
B = \begin{bmatrix} a & b \\ c & d \end{bmatrix},\quad
C = \begin{vmatrix} 1 & 2 \\ 3 & 4 \end{vmatrix},\quad
D = \begin{matrix} 1 & 0 \\ 0 & 1 \end{matrix}
$$

### 2.10 `array` 与 `\hline`

$$
\begin{array}{c|c}
x & y \\
\hline
1 & 2 \\
3 & 4
\end{array}
$$

### 2.11 行距 `\\[6pt]`

$$
\begin{aligned}
a &= b \\[6pt]
c &= d
\end{aligned}
$$

### 2.12 装饰与箭头

$$
\boxed{E = mc^2},\quad
\overset{\text{def}}{=},\quad
\underset{x\to 0}{\lim},\quad
\stackrel{?}{=},\quad
A \xrightarrow{f} B
$$

### 2.13 源码跨行的行间公式

$$
f(x) = a_0 + a_1 x + a_2 x^2
 + a_3 x^3 + a_4 x^4
$$

### 2.14 中文与 `\text`

$$
\text{速度} = \frac{\text{位移}}{\text{时间}}, \quad v = \frac{\Delta x}{\Delta t}
$$

### 2.15 扩展语法（autoload）

$$
\color{red}{x^2} + \cancel{y} + \bbox[4pt,border:1px solid blue]{z}
$$

### 2.16 mhchem

$$
\ce{2H2 + O2 -> 2H2O}
$$

### 2.17 `\notag`

$$
\begin{align}
a &= b \notag \\
c &= d
\end{align}
$$

### 2.18 与文字同行的行间公式

行文中的行间公式 $$x = 1$$ 后面继续文字。

### 2.19 `\tag` 与局部宏

$$
E = mc^2 \tag{2.1}
$$

$$
\newcommand{\R}{\mathbb{R}} x \in \R, \quad \def\Z{\mathbb{Z}} \Z
$$

## 3. 与 Markdown 的交互

### 3.1 强调

**粗体文字 $x^2 + y^2$** 与 *斜体文字 $a + b$*

### 3.2 链接

[$E = mc^2$](https://example.com)、[$f(x_1) = \frac{a}{b}$](https://example.com)、[$x_1^2$](https://example.com)

以上三条链接的下划线应完整覆盖整条链接（含公式本身）。

### 3.3 列表

- 第一项 $a^2$
- 第二项 $b^2$

### 3.4 引用

> 引用中的公式 $c^2$。

### 3.5 表格（公式内含竖线）

| 公式 | 说明 |
| --- | --- |
| $|x|$ | 绝对值 |
| $\lvert x \rvert$ | 另一种绝对值 |
| $a \mid b$ | 整除 |

### 3.6 标题中的公式

#### 标题速度 $v = \frac{s}{t}$

### 3.7 行内代码

`$x + y$` 应保持原样，不渲染。

### 3.8 围栏代码块

```bash
echo "$5 and $10"
printf '%s\n' "$$x$$" "a\\b" "x\_y"
```

### 3.9 美元符号

- 字面美元（推荐）：价格 \$5 和 \$10 元。
- 正文中成对的裸 `$` 会被识别为行内公式，例如 `$5 和 $10`；需要字面美元时写 `\$`。

### 3.10 HTML 中的公式

<span>HTML 内联元素中的公式 $x^2$</span>。

### 3.11 连续多个公式

$a$、$b$、$c$ 都是公式；中文$x$中文。

### 3.12 波浪线代码块

~~~text
tilde: $x$ $$y$$ \\ \_
~~~

### 3.13 原始 HTML 代码元素

原始 HTML：<code>$x$</code> 应保持原样。

<pre>$y$</pre>

上面的 `<pre>` 也不应渲染。

### 3.14 块引用中的行间公式

> 块引用中的行间公式：
>
> $$
> a = b \\
> c = d
> $$
>
> 引用结束。

### 3.15 表格单元格中的多行公式

| 公式 | 说明 |
| --- | --- |
| $\begin{aligned} a &= b \\ c &= d \end{aligned}$ | 单元格内多行 |
| $|x|$ | 含竖线 |

## 4. 已知限制

- 公式内不要留空行：Markdown 会把空行拆成两个段落，公式会被截断。需要额外间距可用 `\\[1em]`。
- 自动编号已关闭（`tags: none`）；`\tag{...}` 仍可手动编号，但 `\label` / `\eqref` 跨公式不解析（显示 `???`）。
- `\newcommand` / `\def` 只在单个公式内生效，不会跨公式共享。
- 当前 MathJax 构建未编译 `\intertext`，该命令会报 "Undefined control sequence"。
- 正文中裸 `$...$` 成对会被当作公式；字面美元请写 `\$`。
- 公式内不要放 Markdown 反引号代码或链接语法。
- MathJax 不会继承外层 Markdown 的粗体/斜体，`**$x$**` 只影响公式周围的文字。
- 行文中直接写 `$$...$$` 会按块级公式换行显示，这是 HTML 中 display 公式的正常行为。

## 5. 检查清单

- [ ] 所有公式渲染为 SVG，没有红色错误框
- [ ] `align` / `aligned` / `gather` / `cases` 正确分行
- [ ] `\[...\]`、`\(...\)`、裸 `\begin{...}` 均可渲染
- [ ] 代码块与行内代码保持原样
- [ ] `\$` 显示为美元符号且不触发公式
- [ ] 表格中含 `|` 的公式不破坏表格
- [ ] 链接中的公式下划线完整覆盖整条链接
