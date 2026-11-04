# notes

纯笔记分支，只放 Markdown 和图片。构建与部署由 GitHub Actions 完成。

## 结构

```
_posts/            文章，子目录即分类
image/             图片，正文里用 ![[xxx.png]] 引用
.github/workflows/ 构建工作流（推送到本分支即触发）
```

## 写作约定

不要写 `title`，文件名就是标题；`date` 只到日：

```yaml
---
date: 2026-11-04
categories: 计算机网络
tags:
- 计算机网络
---
```

草稿在 front matter 写 `published: false`，构建时会被跳过（放进 `_drafts`）。

## 工作流

推送到 `notes` 分支 → Actions 检出 `site` 分支的 Hexo 工程 → 把本分支的
`_posts/`、`image/` 合并进 `source/` → `hexo generate` → 产物推送到 `master`。

站点源码（主题、`_config.yml`、构建脚本）在 `site` 分支。
