"""Generate source/image/git-minecraft/minecraft-git-conflict.png.

Story:
- M1 has A's tower on the left wall.
- B changed the same left wall into an archway.
- Merging B creates a conflict; the conflict is resolved in M2.
- The creeper branch is rejected and deleted.

The PNG has a transparent background and no embedded title/footnote.
Run:
    python source/scripts/git-minecraft/generate_conflict.py
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import make_state, render_player, render_snapshot  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
FONT_PATH = ROOT / 'unifont-18.0.01.otf'
OUT_PATH = ROOT / 'source/image/git-minecraft/minecraft-git-conflict.png'

W, H = 1800, 1420


def main():
    if not FONT_PATH.exists():
        raise SystemExit(f'Missing font: {FONT_PATH}')

    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def text(xy, s, size=28, fill='#e2e8f0', anchor=None, shadow=True):
        f = ImageFont.truetype(str(FONT_PATH), size)
        # normal weight + optional drop shadow
        if shadow:
            d.text((xy[0] + 2, xy[1] + 2), s, font=f, fill=(0, 0, 0, 110), anchor=anchor)
            d.text((xy[0] + 1, xy[1] + 1), s, font=f, fill=(0, 0, 0, 55), anchor=anchor)
        d.text(xy, s, font=f, fill=fill, anchor=anchor)

    def arrow(points, color='#eab308', width=8, head=22):
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

    def crop_zoom(state, box, out_size, scale=6):
        snap = render_snapshot(state, scale)
        x0, y0, x1, y1 = [v * scale for v in box]
        return snap.crop((x0, y0, x1, y1)).resize(out_size, Image.NEAREST)

    m1 = make_state(foundation=True, walls=True, tower=True, roof=True, banner=True)
    b1 = make_state(foundation=True, walls=True, garden=True, arch='left')
    m2 = make_state(foundation=True, walls=True, tower=True, roof=True,
                    banner=True, garden=True, arch='right')

    text((50, 180), 'M1：已合并 A（左侧塔楼）', size=34, fill='#94a3b8')
    img.paste(render_snapshot(m1, 6), (50, 230))
    text((1270, 180), 'feature/garden / B：左墙开拱门', size=34, fill='#d97706')
    img.paste(render_snapshot(b1, 6), (1270, 230))

    # conflict panel: transparent inside, red outline only
    d.rectangle([570, 180, 1230, 790], fill=(15, 23, 42, 238), outline='#ef4444', width=4)
    text((600, 200), '同一面左墙，两种改法', size=40, fill='#ef4444', shadow=False)
    text((610, 250), 'M1：这里是塔楼', size=28, fill='#d97706', shadow=False)
    text((980, 250), 'B：这里是拱门', size=28, fill='#d97706', shadow=False)

    left_crop = crop_zoom(m1, (6, 8, 34, 44), (200, 250), 6)
    right_crop = crop_zoom(b1, (6, 8, 34, 44), (200, 250), 6)
    img.paste(left_crop, (610, 290))
    img.paste(right_crop, (980, 290))
    d.rectangle([610, 290, 810, 540], outline='#f59e0b', width=3)
    d.rectangle([980, 290, 1180, 540], outline='#f59e0b', width=3)
    d.rectangle([870, 370, 950, 450], fill='#7f1d1d', outline='#ef4444', width=4)
    text((910, 410), '冲突', size=28, fill='#fee2e2', anchor='mm', shadow=False)

    # conflict markers; no opaque background
    d.rectangle([600, 575, 1200, 725], outline='#94a3b8', width=2)
    code_lines = ['<<<<<<< HEAD', '左侧塔楼', '=======', '左侧拱门', '>>>>>>> feature/garden']
    for i, line in enumerate(code_lines):
        color = '#3b82f6' if line.startswith(('<<<', '===', '>>>')) else '#94a3b8'
        text((625, 584 + i * 28), line, size=28, fill=color, shadow=False)

    arrow([(540, 410), (565, 410)])
    arrow([(1265, 410), (1235, 410)])
    arrow([(900, 795), (900, 895)], color='#ef4444')

    # resolved result
    img.paste(render_snapshot(m2, 6), (660, 900))
    text((660, 1275), 'main / M2：保留塔楼，把拱门移到右墙，并保留花园', size=34,
         fill='#94a3b8')

    # rejected creeper branch
    creeper = render_player('creeper', 6)
    img.paste(creeper, (1250, 900), creeper)
    for a, b in [((1330, 890), (1360, 920)), ((1360, 890), (1330, 920))]:
        d.line([a, b], fill='#0b1020', width=11)
        d.line([a, b], fill='#ef4444', width=7)
    text((1200, 1060), 'feature/boom：拒绝合并，删除分支', size=28, fill='#ef4444')

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
