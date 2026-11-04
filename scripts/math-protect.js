/* global hexo */
'use strict';

// hexo-renderer-marked 会按 Markdown 规则吞掉公式里的反斜杠转义：`\\`（换行）
// 变成 `\`，`\{` / `\_` / `\*` 等变成去掉了反斜杠的字符，导致 align、
// aligned 等多行环境被合并成一行。这里在 Markdown 渲染前把公式整段替换成
// 占位符，等 Markdown 处理完、hexo-filter-mathjax（after_post_render 优先级
// 5）运行前再原样还原，公式内容不再经过 Markdown，写 LaTeX 时无需额外转义。
//
// 支持的写法：$$...$$、\[...\]、裸 \begin{env}...\end{env}、
// $...$、\(...\)，以及正文里的 \$。
//
// 注意：本文件位于 scripts/，由 Hexo 启动时自动加载。

const crypto = require('crypto');

const STORE = new Map();
const MARK = '@@MATHJAX-';
const PLACEHOLDER_RE = /@@MATHJAX-([0-9a-f]{16})-(\d+)@@/g;

// 围栏代码块（``` 或 ~~~，允许最多 3 个空格缩进）
const FENCE_RE = /^ {0,3}([`~])\1{2,}[^\n]*\n[\s\S]*?^ {0,3}\1{2,}[^\n]*(?:\n|$)/gm;
// 行内代码（支持 ``` 多反引号包围）
const CODE_SPAN_RE = /(`+)(?:(?!\n[ \t]*\n)[\s\S])*?\1/g;
// 公式不跨空行：空行会被 Markdown 拆成不同段落，MathJax 也就无法跨段匹配
const NO_BLANK_LINE = '(?:(?!\\n[ \\t]*\\n)[\\s\\S])*?';
// 行间公式定界符：$$...$$、\[...\]
const DISPLAY_RES = [
  new RegExp('(?<!\\\\)\\$\\$' + NO_BLANK_LINE + '\\$\\$', 'g'),
  new RegExp(String.raw`(?<!\\)\\\[` + NO_BLANK_LINE + String.raw`\\\]`, 'g')
];
// 行内公式定界符：$...$（\$ 不作为定界符）、\(...\)
const INLINE_RES = [
  new RegExp('(?<![\\\\$])\\$(?!\\$)(?:\\\\[\\s\\S]|(?!\\n[ \\t]*\\n)[^\\\\$])*?\\$', 'g'),
  new RegExp(String.raw`(?<!\\)\\\(` + NO_BLANK_LINE + String.raw`\\\)`, 'g')
];
// 裸的 \begin{env}...\end{env}（优先级低于定界符，避免把 $...$ 里的
// aligned/cases 等环境单独切出来）
const ENV_RE = /(?<!\\)\\begin\{([a-zA-Z*]+)\}(?:(?!\n[ \t]*\n)[\s\S])*?\\end\{\1\}/g;
// 正文里的 \$（MathJax 的 processEscapes 会把它输出为字面 $，且不触发公式）
const ESCAPED_DOLLAR_RE = /(?<!\\)\\\$/g;

function collect(re, text) {
  const ranges = [];
  re.lastIndex = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    ranges.push([m.index, m.index + m[0].length]);
    if (m[0].length === 0) re.lastIndex++;
  }
  return ranges;
}

function outside(text, ranges) {
  const segments = [];
  let pos = 0;
  for (const [start, end] of ranges.slice().sort((a, b) => a[0] - b[0])) {
    if (start > pos) segments.push([pos, start]);
    if (end > pos) pos = end;
  }
  if (pos < text.length) segments.push([pos, text.length]);
  return segments;
}

const overlaps = (ranges, start, end) => ranges.some(([s, e]) => start < e && end > s);

// 公式原文是在 Markdown 之后直接插回 HTML 的，尖括号和 & 必须转义，
// 否则 $a<b>c$ 里的 <b> 会被浏览器当成标签。HTML 解析器会在交给 MathJax
// 之前把 &amp;/&lt; 还原成对应的字符。
const escapeHtmlText = str => str.replace(/[&<>]/g, ch => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;'
}[ch]));

// 块引用里的行间公式会把后续行的 "> " 前缀一起包进来，还原前去掉，
// 否则 MathJax 会把 ">" 当成关系符。仅当所有非空续行都以 ">" 开头时才处理。
function stripQuotePrefix(text) {
  const lines = text.split('\n');
  if (lines.length < 2) return text;
  const rest = lines.slice(1).filter(line => line.trim() !== '');
  if (rest.length === 0 || !rest.every(line => /^[ \t]*>/.test(line))) return text;
  return lines.map((line, i) => i === 0 ? line : line.replace(/^(?:[ \t]*>[ \t]?)+/, '')).join('\n');
}

// 返回 { parts }，没有公式时 parts 为 null。
function extract(text, token) {
  const fences = collect(FENCE_RE, text);

  // 行内代码只在非围栏区域识别，避免反引号跨越代码块配对
  const spans = [];
  for (const [start, end] of outside(text, fences)) {
    const segment = text.slice(start, end);
    for (const [s, e] of collect(CODE_SPAN_RE, segment)) {
      spans.push([start + s, start + e]);
    }
  }

  const code = fences.concat(spans);

  // 公式只在代码之外识别，避免 $ 跨代码块配对
  const math = [];
  const regions = outside(text, code);
  for (const [start, end] of regions) {
    const segment = text.slice(start, end);
    const local = [];
    const add = ranges => {
      for (const [s, e] of ranges) {
        if (!overlaps(local, s, e)) local.push([s, e]);
      }
    };
    DISPLAY_RES.forEach(re => add(collect(re, segment)));
    INLINE_RES.forEach(re => add(collect(re, segment)));
    add(collect(ENV_RE, segment));
    for (const [s, e] of local) math.push([start + s, start + e]);
  }

  // 正文中的 \$ 也要保护，否则 Markdown 会去掉反斜杠，MathJax 反而把它当公式
  const escaped = [];
  for (const [start, end] of regions) {
    const segment = text.slice(start, end);
    for (const [s, e] of collect(ESCAPED_DOLLAR_RE, segment)) {
      if (!overlaps(math, start + s, start + e)) escaped.push([start + s, start + e]);
    }
  }

  const entries = math.concat(escaped).sort((a, b) => a[0] - b[0]);
  if (entries.length === 0) return { parts: null };

  const parts = entries.map(([s, e]) => stripQuotePrefix(text.slice(s, e)));

  let result = text;
  for (let i = entries.length - 1; i >= 0; i--) {
    const [s, e] = entries[i];
    result = result.slice(0, s) + `${MARK}${token}-${i}@@` + result.slice(e);
  }

  return { parts, text: result };
}

if (typeof hexo !== 'undefined') {
  // 早于 Hexo 内置的代码块过滤（默认优先级 10），处理原始 Markdown
  hexo.extend.filter.register('before_post_render', data => {
    if (!data || typeof data.content !== 'string' || !/[$\\]/.test(data.content)) return data;

    let token = crypto.randomBytes(8).toString('hex');
    while (data.content.includes(MARK + token)) token = crypto.randomBytes(8).toString('hex');

    const { parts, text } = extract(data.content, token);
    if (!parts) return data;

    STORE.set(token, parts);
    data.content = text;
    data._mathjaxProtectToken = token;
    return data;
  }, 9);

  // 早于 hexo-filter-mathjax（优先级 5）
  hexo.extend.filter.register('after_post_render', data => {
    const token = data && data._mathjaxProtectToken;
    if (!token) return data;
    delete data._mathjaxProtectToken;

    const parts = STORE.get(token);
    STORE.delete(token);
    if (!parts || typeof data.content !== 'string') return data;

    data.content = data.content.replace(PLACEHOLDER_RE, (match, found, index) => {
      if (found !== token) return match;
      const value = parts[Number(index)];
      return value === undefined ? match : escapeHtmlText(value);
    });

    // 标题里的公式会参与 anchor id 的生成（marked 会把占位符去 @ 后写进 id），
    // 这里把残留的 token 从 id / href 中清掉，避免锚点随每次构建变化。
    data.content = data.content.replace(new RegExp(`-?MATHJAX-${token}-\\d+`, 'gi'), '');
    return data;
  }, 4);
}
