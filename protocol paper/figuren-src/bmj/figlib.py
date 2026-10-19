"""Small SVG toolkit for the PARADISE manuscript figures: one typographic and colour system for all figures.

Units are SVG pixels at a 1000 px canvas width (about 17 cm in print). Text is wrapped with Arial advance widths.
"""
from xml.sax.saxutils import escape

INK = '#1D2B36'      # primary text
MUTED = '#5E6B75'    # secondary text, measurement labels
RULE = '#8C98A1'     # neutral strokes
LINE = '#3A4A56'     # arrows
SHARED_FILL = '#F2F4F6'
TEAL = '#0B7A84'     # PARADISE-only elements
TEAL_FILL = '#E6F2F3'
NAVY = '#1B3A5C'     # primary outcome
BAND = '#F8F9FA'
FONT = 'Arial, Helvetica, sans-serif'

# Arial advance widths per 1000 em (regular); bold is about 6% wider
_W = {' ': 278, '!': 278, '"': 355, '%': 889, '&': 667, "'": 191, '(': 333, ')': 333, '*': 389, '+': 584, ',': 278,
      '-': 333, '.': 278, '/': 278, ':': 278, ';': 278, '<': 584, '=': 584, '>': 584, '?': 556, '[': 278, ']': 278,
      '–': 556, '—': 1000, '·': 278, '•': 350, '≥': 549, '≤': 549, '×': 584, '→': 1000, '↑': 500, '↓': 500,
      'f': 278, 'i': 222, 'j': 222, 'l': 222, 'r': 333, 't': 278, 'm': 833, 'w': 722, 'I': 278, 'J': 500,
      'M': 833, 'W': 944, 'm': 833}
for c in '0123456789':
    _W[c] = 556
for c in 'abcdeghknopqsuvxyz':
    _W.setdefault(c, 556 if c not in 'ckvxyz' else 500)
for c in 'ABCDEFGHKLNOPQRSTUVXYZ':
    _W.setdefault(c, 667 if c not in 'CDGHNOQU' else 722)


def tw(s, size, bold=False):
    return sum(_W.get(ch, 556) for ch in s) * size / 1000 * (1.06 if bold else 1)


def wrap(s, width, size, bold=False):
    lines, cur = [], ''
    for word in s.split(' '):
        trial = (cur + ' ' + word).strip()
        if tw(trial, size, bold) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Fig:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.el = []

    # ------------------------------------------------------------ primitives
    def rect(self, x, y, w, h, fill='none', stroke=RULE, sw=1.2, rx=3, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" '
                       'stroke-width="%s"%s/>' % (x, y, w, h, rx, fill, stroke, sw, d))

    def text(self, x, y, s, size=11.5, fill=INK, bold=False, italic=False, anchor='start', spacing=None):
        a = ' font-weight="bold"' if bold else ''
        a += ' font-style="italic"' if italic else ''
        a += ' letter-spacing="%s"' % spacing if spacing else ''
        self.el.append('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s"%s>%s</text>'
                       % (x, y, size, fill, anchor, a, escape(s)))

    def para(self, x, y, s, width, size=11.5, fill=INK, bold=False, italic=False, lead=None, anchor='start'):
        """Wrapped text; returns the y of the next line."""
        lead = lead or size * 1.32
        for line in wrap(s, width, size, bold):
            self.text(x, y, line, size, fill, bold, italic, anchor)
            y += lead
        return y

    def line(self, pts, color=LINE, sw=1.4, arrow=True, dash=None):
        d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
        m = ' marker-end="url(#ah)"' if arrow else ''
        da = ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>' % (d, color, sw, m, da))

    def diamond(self, cx, cy, w, h, fill='#FFFFFF', stroke=LINE, sw=1.3):
        pts = '%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f' % (cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2, cx - w / 2, cy)
        self.el.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (pts, fill, stroke, sw))

    def circle(self, cx, cy, r, fill=LINE, stroke='none'):
        self.el.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s"/>' % (cx, cy, r, fill, stroke))

    # ------------------------------------------------------------ composite: a box with a title, body and measure
    def box(self, x, y, w, h, title=None, body=None, measure=None, kind='shared', tag=None, pad=10, size=11.5,
            tsize=12.5, centre=False):
        fill, stroke, tcol, bcol, sw = {
            'shared': (SHARED_FILL, RULE, INK, INK, 1.2),
            'white': ('#FFFFFF', RULE, INK, INK, 1.2),
            'paradise': (TEAL_FILL, TEAL, INK, INK, 1.4),
            'mediator': ('#FFFFFF', TEAL, INK, INK, 2.4),
            'primary': (NAVY, NAVY, '#FFFFFF', '#E8EEF4', 1.4),
            'muted': ('#FFFFFF', RULE, MUTED, MUTED, 1.0),
        }[kind]
        self.rect(x, y, w, h, fill, stroke, sw)
        cx = x + w / 2
        ty = y + pad + tsize * 0.8
        if tag:
            tagcol = TEAL if kind in ('paradise', 'mediator') else ('#BFD3E6' if kind == 'primary' else MUTED)
            self.text(cx if centre else x + pad, ty, tag.upper(), 9, tagcol, True, anchor='middle' if centre else 'start',
                      spacing='0.6')
            ty += 14
        anchor = 'middle' if centre else 'start'
        tx = cx if centre else x + pad
        if title:
            ty = self.para(tx, ty, title, w - 2 * pad, tsize, tcol, True, anchor=anchor) + 1
        if body:
            for b in ([body] if isinstance(body, str) else body):
                ty = self.para(tx, ty, b, w - 2 * pad, size, bcol, anchor=anchor)
        if measure:
            ty = self.para(tx, ty + 1, measure, w - 2 * pad, size - 1.5, '#C9D6E2' if kind == 'primary' else MUTED,
                           italic=True, anchor=anchor)
        return ty

    def svg(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="%s">'
                '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" '
                'markerUnits="userSpaceOnUse"><path d="M0,0.8 L7,4 L0,7.2 z" fill="%s"/></marker></defs>'
                '<rect width="100%%" height="100%%" fill="#FFFFFF"/>' % (self.w, self.h, self.w, self.h, FONT, LINE))
        return head + '\n'.join(self.el) + '</svg>'
