/* global hexo */
'use strict';

// 支持 Obsidian 的同页标题链接：[[#标题]] / [[#标题|别名]]
//
// 为什么需要单独处理：
//   hexo-filter-titlebased-link 的正则要求 [[ 后面必须有目标文件名（第一个捕获组
//   排除了 #），所以 [[#标题]] 不会被它接管，会原样漏到页面上。
//
// 锚点怎么算：
//   hexo-renderer-markdown-it 在 lib/anchors.js 里调用 hexo-util 的 slugize 生成
//   标题 id，这里用同一个函数、同一组参数（transform: 0 保留大小写、分隔符 -），
//   因此生成的 href 与页面上真实的 id 天然一致。
//
// 优先级取 9：必须早于 Hexo 内置的 backtick_code_block（优先级 10），
// 否则围栏代码块会先被替换成占位符，正则就匹配不到代码块，导致误伤。

const { slugize } = require('hexo-util');

const FENCE_RE = /^ {0,3}([`~])\1{2,}[^\n]*\n[\s\S]*?^ {0,3}\1{2,}[^\n]*(?:\n|$)/gm;
const CODE_SPAN_RE = /(`+)(?:(?!\n[ \t]*\n)[\s\S])*?\1/g;
// [[#标题]] / [[#标题|别名]]
const SAME_PAGE_RE = /\[\[#([^[\]\n|]+?)(?:\|([^[\]\n]+))?\]\]/g;

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

function mapOutsideCode(text, fn) {
  const fences = collect(FENCE_RE, text);
  const spans = [];
  for (const [start, end] of outside(text, fences)) {
    const segment = text.slice(start, end);
    for (const [s, e] of collect(CODE_SPAN_RE, segment)) {
      spans.push([start + s, start + e]);
    }
  }
  const code = fences.concat(spans);
  if (code.length === 0) return fn(text);

  let result = '';
  let pos = 0;
  for (const [start, end] of code.sort((a, b) => a[0] - b[0])) {
    if (start < pos) continue;
    result += fn(text.slice(pos, start)) + text.slice(start, end);
    pos = end;
  }
  return result + fn(text.slice(pos));
}

if (typeof hexo !== 'undefined') {
  hexo.extend.filter.register('before_post_render', data => {
    if (!data || typeof data.content !== 'string') return data;
    if (!data.content.includes('[[#')) return data;

    data.content = mapOutsideCode(data.content, segment => segment.replace(
      SAME_PAGE_RE,
      (match, heading, alias) => {
        const title = heading.trim();
        if (!title) return match;
        // 与渲染器保持完全一致：case 0（保留大小写）+ 分隔符 -
        const id = slugize(title, { transform: 0, separator: '-' });
        if (!id) return alias || title;
        return `<a href="#${id}">${(alias || title).trim()}</a>`;
      }
    ));

    return data;
  }, 9);
}
