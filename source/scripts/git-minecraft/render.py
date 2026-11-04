"""Minecraft-style pixel-art snapshot renderer for the Git diagrams.

This module only draws a single commit snapshot. Layout and labels live in
generate_graph.py so that future diagrams can reuse the same renderer.
"""
from PIL import Image, ImageDraw


def make_state(**kwargs):
    base = dict(
        empty=False,
        foundation=False,
        walls=False,
        tower=False,
        roof=False,
        banner=False,
        garden=False,
        arch=None,
        boom=False,
        pond=False,
    )
    base.update(kwargs)
    return base


def render_snapshot(state, scale=4):
    """Return a 320x240 (at scale=4) pixel-art snapshot of the build state."""
    W, H = 80, 60
    img = Image.new('RGB', (W * scale, H * scale), '#7ec8e3')
    d = ImageDraw.Draw(img)

    def r(x, y, w, h, c):
        d.rectangle([x * scale, y * scale, (x + w) * scale - 1, (y + h) * scale - 1], fill=c)

    # sky bands
    for i, c in enumerate(['#5fb8ef', '#6ec3f3', '#7ec8e3', '#8fd4f0', '#a0def6']):
        r(0, i * 10, W, 10, c)

    # sun
    r(66, 5, 4, 1, '#ffe680')
    r(65, 6, 6, 4, '#ffe680')
    r(66, 10, 4, 1, '#ffe680')
    r(67, 6, 2, 2, '#fff3b0')

    # clouds
    for x, y, w, h in [(5, 9, 13, 3), (9, 12, 9, 2), (48, 16, 16, 3),
                       (53, 19, 9, 2), (30, 4, 9, 2)]:
        r(x, y, w, h, '#f8fafc')
        r(x + 1, y + h, w - 2, 1, '#dbeafe')

    # ground
    r(0, 46, W, 3, '#5aa02c')
    r(0, 47, W, 1, '#3d7a1f')
    r(0, 48, W, 12, '#7a4f2a')
    for x, y in [(3, 52), (11, 57), (20, 50), (31, 56),
                 (43, 53), (56, 58), (67, 51), (75, 56)]:
        r(x, y, 3, 2, '#63401f')
    for x in [2, 17, 34, 51, 68, 77]:
        r(x, 45, 1, 2, '#3d7a1f')

    if state.get('empty'):
        r(36, 38, 8, 7, '#8b5e34')
        r(37, 39, 6, 4, '#d7b377')
        r(38, 40, 4, 1, '#5c3d1f')
        r(40, 45, 1, 3, '#5c3d1f')
        for x in [20, 26, 54, 60]:
            r(x, 41, 1, 5, '#8b5e34')
        return _finish(img, scale)

    # foundation
    if state.get('foundation'):
        r(8, 40, 64, 6, '#8b5e34')
        r(8, 45, 64, 1, '#5c3d1f')
        for x in range(10, 70, 8):
            r(x, 42, 4, 1, '#6f4826')
            r(x + 4, 44, 3, 1, '#6f4826')

    # walls / main keep
    if state.get('walls'):
        r(18, 28, 44, 12, '#8d99ae')
        for y in [32, 36, 40]:
            r(18, y, 44, 1, '#5c677d')
        for i, y in enumerate([28, 33, 37, 41]):
            off = 0 if i % 2 == 0 else 4
            for x in range(20 + off, 60, 8):
                r(x, y, 1, 2, '#6c7a92')
        for x in range(18, 62, 6):
            r(x, 25, 4, 3, '#8d99ae')
            r(x, 25, 4, 1, '#aab4c8')
        # gate
        r(34, 32, 12, 8, '#4e342e')
        r(35, 30, 10, 2, '#4e342e')
        r(37, 29, 6, 1, '#4e342e')
        for x in [36, 40, 44]:
            r(x, 30, 1, 10, '#3e2723')
        r(44, 35, 1, 1, '#eab308')
        # windows
        for x, y in [(24, 31), (52, 31)]:
            r(x, y, 4, 5, '#2f4858')
            r(x + 1, y + 1, 2, 3, '#4fc3f7')

    # tower
    if state.get('tower'):
        r(8, 18, 20, 22, '#8d99ae')
        for x, y, w, h in [(9, 26, 3, 2), (18, 31, 3, 2),
                           (11, 35, 2, 2), (21, 21, 2, 2)]:
            r(x, y, w, h, '#6b8e23')
        for y in [22, 26, 30, 34, 38]:
            r(8, y, 20, 1, '#5c677d')
        for i, y in enumerate([18, 23, 27, 31, 35, 39]):
            off = 0 if i % 2 == 0 else 3
            for x in range(10 + off, 27, 6):
                r(x, y, 1, 2, '#6c7a92')
        if state.get('roof'):
            # Solid top course: the roof must sit on the tower, not float above it.
            r(8, 15, 20, 3, '#8d99ae')
            r(8, 15, 20, 1, '#aab4c8')
            for x in [11, 16, 21]:
                r(x, 16, 1, 2, '#6c7a92')
        else:
            for x in [8, 13, 18, 23]:
                r(x, 15, 3, 3, '#8d99ae')
                r(x, 15, 3, 1, '#aab4c8')
        for x, y in [(13, 23), (20, 23)]:
            r(x, y, 3, 5, '#2f4858')
            r(x + 1, y + 1, 1, 3, '#4fc3f7')
        r(15, 34, 6, 6, '#4e342e')
        r(16, 33, 4, 1, '#4e342e')

    # tower roof / banner
    if state.get('tower') and state.get('roof'):
        for x, y, w in [(18, 3, 4), (16, 5, 8), (14, 7, 12),
                        (12, 9, 16), (10, 11, 20), (8, 13, 24)]:
            r(x, y, w, 2, '#b33939')
            r(x, y, w, 1, '#d9534f')
            r(x, y + 1, w, 1, '#7f1d1d')
        if state.get('banner'):
            r(19, 0, 1, 4, '#e2e8f0')
            r(20, 0, 6, 3, '#eab308')
            r(20, 0, 6, 1, '#fde047')
            r(20, 1, 6, 1, '#a16207')

    # garden
    if state.get('garden'):
        r(34, 46, 12, 9, '#b9a17a')
        for y in [48, 51, 54]:
            r(35, y, 10, 1, '#8f7a58')
        r(12, 46, 16, 2, '#2f8f2f')
        r(52, 46, 16, 2, '#2f8f2f')
        flower_cols = ['#e84a5f', '#ffd166', '#f78c6b', '#c77dff', '#5dd39e']
        for i, x in enumerate([13, 17, 21, 25, 53, 57, 61, 65]):
            r(x, 43, 1, 4, '#3d7a1f')
            r(x - 1, 42, 3, 2, flower_cols[i % len(flower_cols)])
            r(x, 42, 1, 1, '#fff3b0')
        for x, y in [(7, 42), (69, 42)]:
            r(x, y, 4, 4, '#2f8f2f')
            r(x + 1, y - 1, 2, 1, '#4caf50')

    # archway (kept for future variants)
    arch = state.get('arch')
    if arch in ('left', 'right') and state.get('walls'):
        ax = 18 if arch == 'left' else 52
        r(ax, 29, 10, 3, '#6c7a92')
        r(ax, 32, 2, 8, '#6c7a92')
        r(ax + 8, 32, 2, 8, '#6c7a92')
        r(ax + 2, 31, 6, 9, '#2b2b36')
        r(ax + 3, 30, 4, 2, '#2b2b36')
        r(ax + 2, 33, 6, 1, '#5d4037')
        r(ax + 2, 38, 6, 2, '#5d4037')
        r(ax - 1, 31, 1, 5, '#3d7a1f')
        r(ax + 9, 31, 1, 5, '#3d7a1f')
        r(ax - 2, 35, 2, 2, '#e84a5f')
        r(ax + 10, 33, 2, 2, '#ffd166')

    # repaired crater -> pond
    if state.get('pond'):
        r(4, 48, 16, 9, '#1d4ed8')
        r(5, 49, 14, 7, '#3b82f6')
        r(6, 50, 12, 2, '#7dd3fc')
        r(4, 47, 16, 1, '#8d99ae')
        r(4, 57, 16, 1, '#8d99ae')
        for x, y in [(7, 51), (15, 53), (10, 55), (17, 50)]:
            r(x, y, 2, 1, '#bfdbfe')
        r(9, 53, 4, 2, '#22c55e')
        r(10, 53, 1, 1, '#166534')

    # creeper explosion
    if state.get('boom'):
        r(18, 28, 14, 12, '#17141c')
        r(16, 30, 18, 8, '#17141c')
        r(21, 26, 8, 2, '#17141c')
        r(20, 40, 10, 2, '#17141c')
        for x, y, w, h in [(16, 33, 2, 2), (30, 27, 2, 2), (31, 34, 2, 3),
                           (17, 39, 2, 2), (28, 39, 3, 2), (22, 25, 2, 2)]:
            r(x, y, w, h, '#5c677d')
        for x, y in [(8, 41), (28, 43), (34, 40), (5, 46), (24, 45)]:
            r(x, y, 2, 2, '#8d99ae')
        for x, y, w, h, c in [
            (15, 29, 3, 3, '#ff6b00'), (31, 31, 3, 3, '#ffb703'),
            (19, 24, 2, 2, '#ffd166'), (26, 26, 2, 2, '#ff6b00'),
            (13, 35, 2, 2, '#f97316'), (33, 37, 2, 2, '#ffd166'),
        ]:
            r(x, y, w, h, c)
        for x, y, w, h in [(22, 17, 4, 3), (27, 14, 3, 3), (18, 20, 3, 2),
                           (31, 20, 3, 2), (24, 11, 3, 3)]:
            r(x, y, w, h, '#94a3b8')
        r(7, 38, 8, 7, '#c0392b')
        r(7, 40, 8, 2, '#f8fafc')
        r(8, 39, 1, 1, '#2b2b36')
        r(13, 43, 1, 1, '#2b2b36')
        r(9, 44, 1, 1, '#2b2b36')

    return _finish(img, scale)


def _finish(img, scale):
    d = ImageDraw.Draw(img)
    w, h = img.size
    d.rectangle([0, 0, w - 1, h - 1], outline='#0b1020', width=max(2, scale))
    d.rectangle([scale, scale, w - scale - 1, h - scale - 1],
                outline='#dbeafe', width=max(1, scale // 2))
    return img


def render_player(kind='steve', scale=6):
    """Return a small pixel-art player/creeper sprite (transparent background)."""
    W, H = 16, 24
    img = Image.new('RGBA', (W * scale, H * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def r(x, y, w, h, c):
        d.rectangle([x * scale, y * scale, (x + w) * scale - 1,
                     (y + h) * scale - 1], fill=c)

    if kind == 'creeper':
        r(4, 0, 8, 8, '#4caf50')
        r(5, 0, 6, 1, '#6bcf70')
        r(5, 2, 2, 2, '#111827')
        r(9, 2, 2, 2, '#111827')
        r(7, 4, 2, 3, '#111827')
        r(5, 5, 2, 2, '#111827')
        r(9, 5, 2, 2, '#111827')
        r(4, 8, 8, 10, '#43a047')
        r(5, 9, 2, 6, '#66bb6a')
        r(4, 18, 3, 6, '#2e7d32')
        r(9, 18, 3, 6, '#2e7d32')
        return img

    if kind == 'alex':
        hair, shirt, pants, skin = '#c96a2a', '#3fa34d', '#6b4f3a', '#e0ac69'
    elif kind == 'builder':
        hair, shirt, pants, skin = '#4b2e1e', '#eab308', '#3b3b8f', '#c68642'
    else:
        hair, shirt, pants, skin = '#3b2a1a', '#2f6db5', '#3b3b8f', '#c68642'

    r(5, 1, 6, 6, skin)
    r(5, 0, 6, 2, hair)
    r(5, 1, 1, 3, hair)
    r(10, 1, 1, 3, hair)
    r(6, 4, 1, 1, '#1f2937')
    r(9, 4, 1, 1, '#1f2937')
    r(7, 6, 2, 1, '#8b5e34')
    r(5, 7, 6, 8, shirt)
    r(3, 7, 2, 7, skin if kind != 'builder' else shirt)
    r(11, 7, 2, 7, skin if kind != 'builder' else shirt)
    r(5, 8, 2, 6, shirt)
    r(5, 15, 2, 8, pants)
    r(9, 15, 2, 8, pants)
    r(5, 22, 3, 2, '#1f2937')
    r(9, 22, 3, 2, '#1f2937')
    return img
