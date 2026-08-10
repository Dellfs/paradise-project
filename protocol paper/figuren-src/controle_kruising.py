# -*- coding: utf-8 -*-
"""Zoekt lijnen die door tekst lopen, met z-volgorde: een lijn die eerder in het
document staat en daarna door een dekkende rect wordt afgedekt, telt niet mee."""
import os, re, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from controle_overloop import breedte
sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def elementen(src):
    """Alle line/rect/text in documentvolgorde, met hun index."""
    uit = []
    for m in re.finditer(r'<(line|rect|text|path)\b[^>]*?(?:/>|>)', src):
        tag, s = m.group(1), m.group(0)

        def f(naam):
            mm = re.search(r'\b%s="([-\d.]+)"' % naam, s)
            return float(mm.group(1)) if mm else None

        if tag == 'line':
            uit.append(('line', m.start(), (f('x1'), f('y1'), f('x2'), f('y2')), s))
        elif tag == 'rect':
            x, y, w, h = f('x'), f('y'), f('width'), f('height')
            vul = re.search(r'fill="([^"]+)"', s)
            vul = vul.group(1) if vul else 'none'
            dekkend = vul not in ('none', 'transparent') and 'opacity' not in s
            uit.append(('rect', m.start(), (x or 0, y or 0, w, h), dekkend))
        elif tag == 'text':
            mm = re.search(r'<text\b[^>]*>(.*?)</text>',
                           src[m.start():m.start() + 3000], re.S)
            body = mm.group(1) if mm else ''
            uit.append(('text', m.start(), (f('x'), f('y'), f('font-size')), (s, body)))
    return uit


def tekst_bbox(x, y, fs, attrs, body):
    s = re.sub(r'<[^>]+>', '', body)
    s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    bold = 'font-weight="bold"' in attrs
    ls = re.search(r'letter-spacing="([\d.]+)"', attrs)
    w = breedte(s, fs, bold, float(ls.group(1)) if ls else 0.0)
    if 'text-anchor="middle"' in attrs:
        x0 = x - w / 2
    elif 'text-anchor="end"' in attrs:
        x0 = x - w
    else:
        x0 = x
    box = (x0, y - fs * 0.76, x0 + w, y + fs * 0.24)

    rot = re.search(r'transform="rotate\(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)"', attrs)
    if rot:
        from math import radians, cos, sin
        a = radians(float(rot.group(1)))
        cxr, cyr = float(rot.group(2)), float(rot.group(3))
        hoeken = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
        gedraaid = []
        for px, py in hoeken:
            dx, dy = px - cxr, py - cyr
            gedraaid.append((cxr + dx * cos(a) - dy * sin(a),
                             cyr + dx * sin(a) + dy * cos(a)))
        xs = [p[0] for p in gedraaid]
        ys = [p[1] for p in gedraaid]
        box = (min(xs), min(ys), max(xs), max(ys))
    return box, s


def snijdt(lijn, box):
    """Liang-Barsky: snijdt het lijnsegment de rechthoek echt?"""
    x1, y1, x2, y2 = lijn
    if None in lijn:
        return False
    bx0, by0, bx1, by1 = box
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if abs(p) < 1e-9:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return False
                t0 = max(t0, r)
            else:
                if r < t0:
                    return False
                t1 = min(t1, r)
    return t0 <= t1


def dekt(rect, box):
    rx, ry, rw, rh = rect
    if rw is None or rh is None:
        return False
    return rx <= box[0] and ry <= box[1] and rx + rw >= box[2] and ry + rh >= box[3]


def check(pad):
    src = open(pad, encoding='utf-8').read()
    els = elementen(src)
    naam = pad.split('\\')[-1]
    meldingen = []
    for i, (tag, pos, geo, extra) in enumerate(els):
        if tag != 'text':
            continue
        x, y, fs = geo
        if None in (x, y, fs):
            continue
        box, s = tekst_bbox(x, y, fs, extra[0], extra[1])
        if not s.strip():
            continue
        for j, (tag2, pos2, geo2, extra2) in enumerate(els[:i]):
            if tag2 != 'line' or not snijdt(geo2, box):
                continue
            # afgedekt door een latere dekkende rect?
            verborgen = any(
                els[k][0] == 'rect' and els[k][3] and dekt(els[k][2], box)
                for k in range(j + 1, i))
            if not verborgen:
                meldingen.append('  lijn %s  kruist  %r' %
                                 (tuple(int(v) for v in geo2), s[:52]))
    print('=== %s ===' % naam)
    for m in dict.fromkeys(meldingen):
        print(m)
    if not meldingen:
        print('  geen kruisingen')
    print()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        check(p)
