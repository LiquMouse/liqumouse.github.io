# Git / Minecraft 示意图脚本

- `render.py`：Minecraft 风格像素快照 / 人物渲染器。
- `generate_multibranch.py`：生成 `source/image/git-minecraft/minecraft-git-multibranch.png`。
- `generate_conflict.py`：生成 `source/image/git-minecraft/minecraft-git-conflict.png`。
- `generate_graph.py`：生成 `source/image/git-minecraft/minecraft-git-graph.png`。

运行单个脚本：

```bash
python source/scripts/git-minecraft/generate_multibranch.py
python source/scripts/git-minecraft/generate_conflict.py
python source/scripts/git-minecraft/generate_graph.py
```

说明：

- 输出均为透明背景 PNG。
- 图片中不包含标题、副标题和底部脚注；说明文字放在文章正文里。
- 文字使用正常字重 + 阴影，并选用在浅色和深色背景上都有对比度的颜色。

依赖：

- Python 3
- Pillow
- 仓库根目录下存在 `unifont-18.0.01.otf`（用于中文像素字体，不提交到仓库）
