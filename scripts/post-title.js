/* global hexo */
'use strict';

// 文章 front matter 里没写 title 时，用文件名兜底，避免页面标题为空。
//
// 背景：Hexo 的 title 只来自两处——front matter 的 `title`，或
// `use_slug_as_post_title: true` 时的 slug（此时会带上 _posts 下的目录前缀，
// 例如 “测试/这是一条测试博客”，不好看）。两者都没有就留空，主题只会渲染出
// 一个空标题，<title> 标签也会退化成站点名。
//
// 这里取 slug 的最后一段（即文件名），既与 permalink 的 :title 段一致，
// 也符合“文件名即标题”的写作约定。想自定义标题时，直接在 front matter
// 写 title 即可，本过滤器不会覆盖已有的值。
//
// 注意：本文件位于 scripts/，由 Hexo 启动时自动加载。

hexo.extend.filter.register('before_post_render', data => {
    if (!data) return data;
    if (typeof data.title === 'string' && data.title.trim() !== '') return data;

    const slug = typeof data.slug === 'string' ? data.slug : '';
    if (!slug) return data;

    data.title = slug.split('/').pop();
    return data;
}, 9);
