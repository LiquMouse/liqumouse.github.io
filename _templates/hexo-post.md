<%*
// Hexo 文章 front matter
// date 精确到日；categories 取 _posts 下最底层目录；tags 打全部层级
const parts = tp.file.folder(true)
  .split("/")
  .filter(p => p && p !== "_posts");

const category = parts.length ? parts[parts.length - 1] : "";

let out = "date: " + tp.date.now("YYYY-MM-DD") + "\n";
if (category) out += "categories: " + category + "\n";
if (parts.length) {
  out += "tags:\n";
  for (const p of parts) out += "- " + p + "\n";
}

tR += "---\n" + out + "---\n";
_%>
