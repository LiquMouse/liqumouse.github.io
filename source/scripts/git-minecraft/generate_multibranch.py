"""Generate source/image/git-minecraft/minecraft-git-multibranch.png.

Story:
- A and B branch from C2 and both modify the same left wall.
- The creeper branch blows the house up.
- All three branches share the same C2 base.

The PNG has a transparent background and no embedded title/footnote.
Run:
    python source/scripts/git-minecraft/generate_multibranch.py
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import make_state, render_player, render_snapshot  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
FONT_PATH = ROOT / 'unifont-18.0.01.otf'
OUT_PATH = ROOT / 'source/image/git-minecraft/minecraft-git-multibranch.png'

W, H = 2200, 1220
BRANCH_X = 1450
CHAR_X = 1800
TRUNK_X = 1000


def main():
    if not FONT_PATH.exists():
        raise SystemExit(f'Missing font: {FONT_PATH}')

    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def text(xy, s, size=28, fill='#e2e8f0', anchor=None):
        f = ImageFont.truetype(str(FONT_PATH), size)
        # normal weight + drop shadow (no synthetic bold)
        d.text((xy[0] + 2, xy[1] + 2), s, font=f, fill=(0, 0, 0, 110), anchor=anchor)
        d.text((xy[0] + 1, xy[1] + 1), s, font=f, fill=(0, 0, 0, 55), anchor=anchor)
        d.text(xy, s, font=f, fill=fill, anchor=anchor)

    def arrow(points, color='#94a3b8', width=8, head=22):
        d.line(points, fill='#0b1020', width=width + 4, joint='curve')
        (x1, y1), (x2, y2) = points[-2], points[-1]
        ang = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - (head + 4) * math.cos(ang - 0.55), y2 - (head + 4) * math.sin(ang - 0.55))
        p2 = (x2 - (head + 4) * math.cos(ang + 0.55), y2 - (head + 4) * math.sin(ang + 0.55))
        d.polygon([(x2, y2), p1, p2], fill='#0b1020')
        d.line(points, fill=color, width=width, joint='curve')
        p1 = (x2 - head * math.cos(ang - 0.55), y2 - head * math.sin(ang - 0.55))
        p2 = (x2 - head * math.cos(ang + 0.55), y2 - head * math.sin(ang + 0.55))
        d.polygon([(x2, y2), p1, p2], fill=color)

    # main base
    text((70, 520), 'main / C2：你建好的大房子', size=36, fill='#94a3b8')
    img.paste(render_snapshot(make_state(foundation=True, walls=True), 4), (70, 580))
    builder = render_player('builder', 6)
    img.paste(builder, (250, 870), builder)
    text((250, 870 + builder.height + 4), '你', size=28, fill='#94a3b8')

    # branch trunk: longer main-to-trunk line, shorter branch arrows
    d.line([(390, 700), (TRUNK_X, 700)], fill='#0b1020', width=12)
    d.line([(390, 700), (TRUNK_X, 700)], fill='#94a3b8', width=8)
    d.line([(TRUNK_X, 320), (TRUNK_X, 920)], fill='#0b1020', width=12)
    d.line([(TRUNK_X, 320), (TRUNK_X, 920)], fill='#94a3b8', width=8)
    arrow([(TRUNK_X, 320), (BRANCH_X, 320)], color='#9acd32')
    arrow([(TRUNK_X, 620), (BRANCH_X, 620)], color='#eab308')
    arrow([(TRUNK_X, 920), (BRANCH_X, 920)], color='#ef4444')
    text((410, 740), '从 main 的 C2 节点建立分支', size=40, fill='#94a3b8')

    # branch A: tower
    text((BRANCH_X, 150), 'feature/tower：朋友 A 在左墙加塔楼', size=36, fill='#65a30d')
    img.paste(render_snapshot(
        make_state(foundation=True, walls=True, tower=True, roof=True, banner=True), 4),
        (BRANCH_X, 200))
    alex = render_player('alex', 6)
    img.paste(alex, (CHAR_X, 200), alex)
    text((CHAR_X, 200 + alex.height + 4), '朋友 A', size=28, fill='#65a30d')

    # branch B: garden + archway on the same left wall
    text((BRANCH_X, 450), 'feature/garden：朋友 B 在同一面左墙开拱门', size=36, fill='#d97706')
    img.paste(render_snapshot(
        make_state(foundation=True, walls=True, garden=True, arch='left'), 4),
        (BRANCH_X, 500))
    steve = render_player('steve', 6)
    img.paste(steve, (CHAR_X, 500), steve)
    text((CHAR_X, 500 + steve.height + 4), '朋友 B', size=28, fill='#d97706')

    # branch C: creeper
    text((BRANCH_X, 750), 'feature/boom：苦力怕炸房子', size=36, fill='#ef4444')
    img.paste(render_snapshot(make_state(foundation=True, walls=True, boom=True), 4),
              (BRANCH_X, 800))
    creeper = render_player('creeper', 6)
    img.paste(creeper, (CHAR_X, 800), creeper)
    text((CHAR_X, 800 + creeper.height + 4), '苦力怕', size=28, fill='#ef4444')

    # crop transparent margins
    bbox = img.getbbox()
    if bbox:
        pad = 40
        bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                min(W, bbox[2] + pad), min(H, bbox[3] + pad))
        img = img.crop(bbox)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PATH)
    print(f'saved {OUT_PATH} {img.size}')


if __name__ == '__main__':
    main()
