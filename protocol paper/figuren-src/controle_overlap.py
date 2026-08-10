# -*- coding: utf-8 -*-
"""Volledige overlapcontrole voor de figuren: tekst tegen lijnen, cirkels,
polylines, paths en andere tekst. Houdt rekening met tekenvolgorde, dekkende
achtergrondvlakken en rotatie."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from controle_overloop import breedte
from controle_kruising import tekst_bbox, snijdt
sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def getal(s, naam):
    m = re.search(r'\b%s="([-\d.]+)"' % naam, s)
    return float(m.group(1)) if m else None


def punten(d):
    return [(float(a), float(b)) for a, b in
            re.findall(r'(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)', d)]


def elementen(src):
    uit = []
    for m in re.finditer(r'<(line|rect|circle|polyline|polygon|path|text)\b[^>]*?(?:/>|>)', src):
        tag, s, pos = m.group(1), m.group(0), m.start()
        if tag == 'line':
            uit.append((tag, pos, (getal(s, 'x1'), getal(s, 'y1'),
                                   getal(s, 'x2'), getal(s, 'y2')), s))
        elif tag == 'rect':
            vul = re.search(r'fill="([^"]+)"', s)
            vul = vul.group(1) if vul else 'none'
            dekkend = vul not in ('none', 'transparent') and 'opacity' not in s
            uit.append((tag, pos, (getal(s, 'x') or 0, getal(s, 'y') or 0,
                                   getal(s, 'width'), getal(s, 'height')), dekkend))
        elif tag == 'circle':
            vul = re.search(r'fill="([^"]+)"', s)
            gevuld = bool(vul) and vul.group(1) not in ('none', 'transparent')
            sw = getal(s, 'stroke-width') or 1.0
            uit.append((tag, pos, (getal(s, 'cx'), getal(s, 'cy'), getal(s, 'r')),
                        (s, gevuld, sw)))
        elif tag in ('polyline', 'polygon'):
            p = re.search(r'points="([^"]+)"', s)
            uit.append((tag, pos, punten(p.group(1)) if p else [], s))
        elif tag == 'path':
            dd = re.search(r'\bd="([^"]+)"', s)
            uit.append((tag, pos, punten(dd.group(1)) if dd else [], s))
        elif tag == 'text':
            mm = re.search(r'<text\b[^>]*>(.*?)</text>', src[pos:pos + 4000], re.S)
            uit.append((tag, pos, (getal(s, 'x'), getal(s, 'y'), getal(s, 'font-size')),
                        (s, mm.group(1) if mm else '')))
    return uit


def dekt(rect, box):
    rx, ry, rw, rh = rect
    if rw is None or rh is None:
        return False
    return rx <= box[0] and ry <= box[1] and rx + rw >= box[2] and ry + rh >= box[3]


def cirkel_raakt(c, box, gevuld=True, sw=1.0):
    """Gevulde cirkel: schijf tegen kader. Ongevulde: enkel de streep telt."""
    cx, cy, r = c
    if None in c:
        return False
    hoeken = [(box[0], box[1]), (box[2], box[1]), (box[0], box[3]), (box[2], box[3])]
    afst = [((hx - cx) ** 2 + (hy - cy) ** 2) ** .5 for hx, hy in hoeken]
    nx = max(box[0], min(cx, box[2]))
    ny = max(box[1], min(cy, box[3]))
    dichtst = ((nx - cx) ** 2 + (ny - cy) ** 2) ** .5
    if gevuld:
        return dichtst <= r
    # streep raakt het kader alleen als r tussen dichtstbijzijnde en verste hoek ligt
    return dichtst - sw / 2 <= r <= max(afst) + sw / 2


def keten_raakt(pts, box):
    return any(snijdt((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]), box)
               for i in range(len(pts) - 1))


def overlapt(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def check(pad):
    src = open(pad, encoding='utf-8').read()
    els = elementen(src)
    teksten = []
    for i, (tag, pos, geo, extra) in enumerate(els):
        if tag != 'text' or None in geo:
            continue
        box, s = tekst_bbox(geo[0], geo[1], geo[2], extra[0], extra[1])
        if s.strip():
            teksten.append((i, box, s))

    meldingen = []
    for i, box, s in teksten:
        for j, (tag2, pos2, geo2, extra2) in enumerate(els[:i]):
            raak = False
            if tag2 == 'line':
                raak = snijdt(geo2, box)
            elif tag2 == 'circle':
                raak = cirkel_raakt(geo2, box, extra2[1], extra2[2])
            elif tag2 in ('polyline', 'polygon', 'path'):
                raak = keten_raakt(geo2, box)
            if not raak:
                continue
            verborgen = any(els[k][0] == 'rect' and els[k][3] and dekt(els[k][2], box)
                            for k in range(j + 1, i))
            if not verborgen:
                meldingen.append('%-9s over tekst %r' % (tag2, s[:50]))
        # cirkels en curves die NA de tekst komen, liggen er bovenop
        for j in range(i + 1, len(els)):
            tag2, pos2, geo2, extra2 = els[j]
            raak = False
            if tag2 == 'circle':
                raak = cirkel_raakt(geo2, box)
            elif tag2 in ('polyline', 'polygon', 'path'):
                raak = keten_raakt(geo2, box)
            elif tag2 == 'line':
                raak = snijdt(geo2, box)
            if raak:
                meldingen.append('%-9s BOVENOP tekst %r' % (tag2, s[:50]))

    for a in range(len(teksten)):
        for b in range(a + 1, len(teksten)):
            if overlapt(teksten[a][1], teksten[b][1]):
                meldingen.append('tekst     overlapt tekst: %r  <>  %r'
                                 % (teksten[a][2][:34], teksten[b][2][:34]))

    print('=== %s ===' % pad.split('\\')[-1])
    for m in dict.fromkeys(meldingen):
        print('  ' + m)
    if not meldingen:
        print('  schoon')
    print()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        check(p)
