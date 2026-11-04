/* global hexo */
'use strict';

// 把 Obsidian 风格的图片引用改写成站点内路径，源文件保持 Obsidian 可识别的写法。
//
// 支持的写法：
//   ![[xxx.png]]                     ← 按文件名在资源里找
//   ![[子目录/xxx.png]]               ← 带子目录
//   ![[xxx.png|300]]                 ← 数字别名视为宽度
//   ![说明](image/xxx.png)            ← 相对 source 根
//   ![说明](../image/xxx.png)         ← 文章挪过目录后遗留的写法，也能兜住
//   ![说明](/image/xxx.png)           ← 站点根绝对路径
//
// 目标必须是会被发布出去的资源（hexo 的 Asset 模型），因此只接受 source/ 下
// 非隐藏、非可渲染的文件；_posts 里的图片本来就不会进 public，指向它们没有意义。
// 找不到或重名时输出 warn，链接原样保留，不影响构建。
//
// 说明：本文件位于 scripts/，由 Hexo 启动时自动加载；优先级 10 晚于
// scripts/math-protect.js 与 hexo-filter-titlebased-link（均为 9）。

const path = require('path');

const FENCE_RE = /^ {0,3}([`~])\1{2,}[^\n]*\n[\s\S]*?^ {0,3}\1{2,}[^\n]*(?:\n|$)/gm;
const CODE_SPAN_RE = /(`+)(?:(?!\n[ \t]*\n)[\s\S])*?\1/g;

// ![说明](目标 "标题")；说明里不能有方括号，避免和 ![[...]] 混淆
const MD_IMAGE_RE = /!\[([^[\]\n]*)\]\(\s*(<[^>\n]+>|[^()\s]+)(\s+"[^"]*")?\s*\)/g;
// ![[目标]] / ![[目标|宽度]]
const WIKI_EMBED_RE = /!\[\[([^[\]\n]+?)\]\]/g;

let index = null;

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

// 只处理代码块/行内代码之外的片段
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

function getIndex() {
    if (index) return index;
    const byPath = new Map();
    const byName = new Map();

    const add = assetPath => {
        if (!assetPath) return;
        byPath.set(assetPath, assetPath);
        const name = path.posix.basename(assetPath);
        if (!byName.has(name)) byName.set(name, []);
        byName.get(name).push(assetPath);
    };

    // source/ 下的普通资源（image/ 等）
    hexo.model('Asset').find({}).forEach(asset => add(asset.path));

    // post_asset_folder: true 时图片挂在文章资源目录下，注册在 PostAsset 模型；
    // 其 path 是相对 public 的完整路径，直接可用。
    try {
        hexo.model('PostAsset').find({}).forEach(asset => add(asset.path));
    }
    catch (e) {
        /* 模型不存在时忽略 */
    }

    index = { byPath, byName };
    return index;
}

function resolveAsset(raw, fromDir, source) {
    let target = raw.trim();
    if (target.startsWith('<') && target.endsWith('>')) target = target.slice(1, -1);
    target = target.trim();

    // 外链、data URI、协议相对地址一律跳过
    if (/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(target) || target.startsWith('//')) return null;

    const clean = target.split('#')[0].split('?')[0].replace(/\\/g, '/');
    if (!clean) return null;

    const { byPath, byName } = getIndex();
    const candidates = [];

    if (clean.startsWith('/')) {
        candidates.push(clean.replace(/^\/+/, ''));
    }
    else {
        // 先按 Markdown 语义相对当前文章所在目录解析，再退回 source 根，
        // 这样文章挪过目录的历史写法（../image/...）也能命中。
        candidates.push(path.posix.normalize(path.posix.join(fromDir, clean)));
        candidates.push(path.posix.normalize(clean.replace(/^(\.\.\/)+/, '')));
    }

    for (const candidate of candidates) {
        if (byPath.has(candidate)) return candidate;
    }

    // 兜底：按文件名唯一匹配（和 Obsidian 的 ![[xxx.png]] 语义一致）
    const name = path.posix.basename(clean);
    if (!/\.[a-zA-Z0-9]+$/.test(name)) return null;

    const list = byName.get(name);
    if (!list || list.length === 0) {
        hexo.log.warn('%s: 找不到图片 "%s"', source, raw);
        return null;
    }
    if (list.length > 1) {
        hexo.log.warn('%s: "%s" 有多个同名图片（%s），请写完整路径', source, raw, list.join('、'));
        return null;
    }
    return list[0];
}

function assetUrl(assetPath) {
    const urlFor = hexo.extend.helper.get('url_for');
    return urlFor ? urlFor.call(hexo, assetPath) : '/' + assetPath;
}

function rewrite(text, fromDir, source) {
    return mapOutsideCode(text, segment => segment
        .replace(WIKI_EMBED_RE, (match, inner) => {
            const bar = inner.indexOf('|');
            const raw = (bar < 0 ? inner : inner.slice(0, bar)).trim();
            const width = bar < 0 ? '' : inner.slice(bar + 1).trim();

            const assetPath = resolveAsset(raw, fromDir, source);
            if (!assetPath) return match;

            const url = assetUrl(assetPath);
            // 数字别名在 Obsidian 里表示显示宽度，这里转成 img 的 width 属性
            if (/^\d+(px|%)?$/.test(width)) {
                return `<img src="${url}" width="${width.replace(/(px|%)$/, '')}">`;
            }
            return `![](${url})`;
        })
        .replace(MD_IMAGE_RE, (match, alt, target, title) => {
            const assetPath = resolveAsset(target, fromDir, source);
            if (!assetPath) return match;
            return `![${alt}](${assetUrl(assetPath)}${title || ''})`;
        })
    );
}

if (typeof hexo !== 'undefined') {
    hexo.extend.filter.register('before_generate', () => {
        index = null;
    }, 1);

    hexo.extend.filter.register('before_post_render', data => {
        if (!data || typeof data.content !== 'string' || !data.source) return data;
        if (!data.content.includes('![')) return data;

        const fromDir = path.posix.dirname(data.source);
        data.content = rewrite(data.content, fromDir, data.source);
        return data;
    }, 10);
}
