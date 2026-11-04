"""Generate source/image/git-minecraft/minecraft-git-graph.png.

Story:
- A and B branch from C2 and both modify the same left wall.
- A is merged first (M1).
- B is merged next; that creates a conflict, resolved in M2.
- The creeper branch is rejected and deleted, so it never reaches main.

The PNG has a transparent background and no embedded title/footnote.
Run:
    python source/scripts/git-minecraft/generate_graph.py
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import make_state, render_snapshot  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
FONT_PATH = ROOT / 'unifont-18.0.01.otf'
OUT_PATH = ROOT / 'source/image/git-minecraft/minecraft-git-graph.png'

W, H = 2200, 1500
SCALE = 4
NODE_W, NODE_H = 80 * SCALE, 60 * SCALE

# Main row: C2 [50..370], M1 [850..1170], M2 [1300..1620].
# Branch column: [450..770], between C2 and M1.
# C! sits at exactly the same y/height as G1 (feature/garden).
NODE_POS = {
    'C2': (50, 1200),
    'T1': (450, 900),
    'G1': (450, 550),
    'X1': (450, 200),
    'M1': (850, 1200),
    'C!': (1300, 550),
    'M2': (1300, 1200),
}


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

    def arrow(points, color='#64748b', width=8, head=22):
        # dark halo keeps lines visible on light backgrounds
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

    # ---- main line: C2 -> M1 -> M2 -> ... ----
    arrow([(370, 1320), (850, 1320)], color='#94a3b8')
    arrow([(1170, 1320), (1300, 1320)], color='#94a3b8')
    arrow([(1620, 1320), (1850, 1320)], color='#94a3b8')
    for dot_x in (1900, 1950, 2000):
        d.ellipse([dot_x - 13, 1307, dot_x + 13, 1333], fill='#0b1020')
        d.ellipse([dot_x - 8, 1312, dot_x + 8, 1328], fill='#e2e8f0')

    # ---- C2 -> branch nodes (top exits, left to right: boom, garden, tower) ----
    arrow([(110, 1200), (110, 320), (450, 320)], color='#ef4444')   # boom -> X1 left
    arrow([(210, 1200), (210, 670), (450, 670)], color='#eab308')  # garden -> G1 left
    arrow([(310, 1200), (310, 1020), (450, 1020)], color='#9acd32')  # tower -> T1 left

    # ---- A merges first: T1 right edge -> M1 top-center ----
    arrow([(770, 1020), (1010, 1020), (1010, 1200)], color='#9acd32')
    # ---- B merges next and conflicts: G1 right edge -> C! left edge ----
    arrow([(770, 670), (1300, 670)], color='#eab308')
    # ---- conflict resolved: C! bottom -> M2 top-center ----
    arrow([(1460, 790), (1460, 1200)], color='#ef4444')

    # ---- creeper branch is rejected, not merged ----
    for x1, x2 in [(785, 810), (820, 845), (855, 880)]:
        d.line([(x1, 320), (x2, 320)], fill='#0b1020', width=9)
        d.line([(x1, 320), (x2, 320)], fill='#ef4444', width=5)
    for a, b in [((885, 305), (915, 335)), ((915, 305), (885, 335))]:
        d.line([a, b], fill='#0b1020', width=11)
        d.line([a, b], fill='#ef4444', width=7)
    text((800, 355), '拒绝合并，删除 feature/boom', size=36, fill='#ef4444')

    # ---- labels ----
    text((450, 846), 'feature/tower / A：左墙加塔楼', size=36, fill='#65a30d')
    text((450, 496), 'feature/garden / B：同一面左墙开拱门', size=36, fill='#d97706')
    text((450, 146), 'feature/boom：苦力怕炸房子', size=36, fill='#ef4444')

    text((790, 1040), 'merge A', size=36, fill='#65a30d')
    text((880, 720), 'merge B：发生冲突', size=36, fill='#d97706')
    text((1490, 1010), '解决冲突后提交', size=36, fill='#ef4444')

    # ---- snapshots ----
    states = {
        'C2': make_state(foundation=True, walls=True),
        'T1': make_state(foundation=True, walls=True, tower=True, roof=True, banner=True),
        'G1': make_state(foundation=True, walls=True, garden=True, arch='left'),
        'X1': make_state(foundation=True, walls=True, boom=True),
        'M1': make_state(foundation=True, walls=True, tower=True, roof=True, banner=True),
        'C!': make_state(foundation=True, walls=True, tower=True, roof=True, banner=True),
        'M2': make_state(foundation=True, walls=True, tower=True, roof=True,
                         banner=True, garden=True, arch='right'),
    }

    for key, pos in NODE_POS.items():
        img.paste(render_snapshot(states[key], SCALE), pos)

    # conflict node styling
    cx, cy = NODE_POS['C!']
    d.rectangle([cx, cy, cx + NODE_W - 1, cy + NODE_H - 1], outline='#ef4444', width=8)
    d.rectangle([cx + 18, cy + 14, cx + 78, cy + 74], fill='#7f1d1d', outline='#fca5a5', width=3)
    text((cx + 48, cy + 44), '!', size=44, fill='#fee2e2', anchor='mm')
    d.rectangle([cx, cy + NODE_H - 38, cx + NODE_W, cy + NODE_H], fill='#450a0a')
    text((cx + NODE_W // 2, cy + NODE_H - 19), 'C! 冲突', size=32,
         fill='#fecaca', anchor='mm')

    # ---- node labels ----
    text((50, 1452), 'C2 你建好的房子', size=36, fill='#94a3b8')
    text((850, 1452), 'M1 合并 A', size=36, fill='#65a30d')
    text((1300, 1452), 'M2 合并 B 并解决冲突', size=36, fill='#ef4444')

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
