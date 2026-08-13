# -*- coding: utf-8 -*-
"""Bouwt de PARADISE-presentatie: dark mode, bento-grid, morph-overgangen.

Alle tekst staat in echte tekstvakken, dus alles blijft bewerkbaar in
PowerPoint. Sprekersnotities bevatten per dia de presentatietip en het
interactiemoment. Inhoud staat in inhoud.py.
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image

from inhoud import SLIDES, K, FONT, FONT_L, FONT_M, kol, PUNTEN
import beeld

HIER = os.path.dirname(os.path.abspath(__file__))
BEELD = os.path.join(HIER, 'beeld')
DOEL = os.path.join(HIER, 'PARADISE_informatiesessie_voetklinieken.pptx')

B, H = 1920, 1080
SCH = 13.333 / B


def px(v):
    return Inches(v * SCH)


def rgb(n):
    return RGBColor.from_string(K[n])


def tegel(s, x, y, w, h, vul='tegel', rand='rand', alpha=None, rond=True, naam=None):
    """Bento-tegel; alpha geeft het glaseffect."""
    vorm = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rond else MSO_SHAPE.RECTANGLE,
        px(x), px(y), px(w), px(h))
    if naam:
        vorm.name = naam
    vorm.fill.solid()
    vorm.fill.fore_color.rgb = rgb(vul)
    if alpha is not None:
        sf = vorm.fill.fore_color._xFill.find(qn('a:srgbClr'))
        el = etree.SubElement(sf, qn('a:alpha'))
        el.set('val', str(int(alpha * 1000)))
    if rand:
        vorm.line.color.rgb = rgb(rand)
        vorm.line.width = Pt(0.75)
    else:
        vorm.line.fill.background()
    if rond:
        vorm.adjustments[0] = 0.045
    vorm.shadow.inherit = False
    return vorm


def txt(s, x, y, w, h, regels, gr=16, kl='ink', vet=False, font=FONT,
        uit=PP_ALIGN.LEFT, ra=1.25, sp=0, anker=MSO_ANCHOR.TOP, caps=False, naam=None,
        omslag=True):
    tb = s.shapes.add_textbox(px(x), px(y), px(w), px(h))
    if naam:
        tb.name = naam
    tf = tb.text_frame
    tf.word_wrap = omslag
    tf.vertical_anchor = anker
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if isinstance(regels, str):
        regels = regels.split('\n')
    for i, r in enumerate(regels):
        ex = {}
        if isinstance(r, tuple):
            r, ex = r
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ex.get('uit', uit)
        p.line_spacing = ex.get('ra', ra)
        if i:
            p.space_before = Pt(ex.get('voor', 5))
        run = p.add_run()
        run.text = r.upper() if ex.get('caps', caps) else r
        f = run.font
        f.name = ex.get('font', font)
        f.size = Pt(ex.get('gr', gr))
        f.bold = ex.get('vet', vet)
        f.color.rgb = rgb(ex.get('kl', kl))
        s2 = ex.get('sp', sp)
        if s2:
            run.font._rPr.set('spc', str(int(s2 * 100)))
    return tb


def punt(s, x, y, d, kl):
    """Losse stip voor de puntenmatrix."""
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, px(x), px(y), px(d), px(d))
    o.fill.solid(); o.fill.fore_color.rgb = rgb(kl)
    o.line.fill.background(); o.shadow.inherit = False
    return o


def matrix(s, x, y, n, per_rij, d, spatie, kleuren):
    """Puntenmatrix: n stippen, kleur per index via de lijst kleuren."""
    for i in range(n):
        r, k = divmod(i, per_rij)
        punt(s, x + k * (d + spatie), y + r * (d + spatie), d, kleuren[i])


def staaf(s, x, y, w, h, deel, kl, achter='tegel2'):
    """Horizontale staaf met gevuld aandeel (deel = 0..1)."""
    b = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(x), px(y), px(w), px(h))
    b.fill.solid(); b.fill.fore_color.rgb = rgb(achter)
    b.line.fill.background(); b.shadow.inherit = False
    b.adjustments[0] = 0.5
    if deel > 0:
        f = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px(x), px(y), px(w * deel), px(h))
        f.fill.solid(); f.fill.fore_color.rgb = rgb(kl)
        f.line.fill.background(); f.shadow.inherit = False
        f.adjustments[0] = 0.5
    return b


def merkstreep(s, x, y, h, kl='ink'):
    """Verticale streefwaardestreep over een staaf."""
    m = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(x), px(y), px(3), px(h))
    m.fill.solid(); m.fill.fore_color.rgb = rgb(kl)
    m.line.fill.background(); m.shadow.inherit = False
    return m


def gloed(s, x, y, d, kl, alpha=7):
    """Grote, bijna doorzichtige cirkel: geeft diepte achter een heldia."""
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, px(x), px(y), px(d), px(d))
    o.fill.solid(); o.fill.fore_color.rgb = rgb(kl)
    sf = o.fill.fore_color._xFill.find(qn('a:srgbClr'))
    etree.SubElement(sf, qn('a:alpha')).set('val', str(int(alpha * 1000)))
    o.line.fill.background(); o.shadow.inherit = False
    return o


def liniaal(s, x, y, w, kl='rand', dik=1.5):
    """Haarlijn als scheiding — vervangt een kader waar een kader te veel is."""
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(x), px(y), px(w), px(dik))
    r.fill.solid(); r.fill.fore_color.rgb = rgb(kl)
    r.line.fill.background(); r.shadow.inherit = False
    return r


def foto(s, bestand, x, y, w, h, naam=None):
    """Past een foto passend in het vak x,y,w,h en centreert hem daarin."""
    pad = os.path.join(BEELD, bestand)
    with Image.open(pad) as im:
        bw, bh = im.size
    f = min(w / bw, h / bh)
    fw, fh = bw * f, bh * f
    p = s.shapes.add_picture(pad, px(x + (w - fw) / 2), px(y + (h - fh) / 2),
                             px(fw), px(fh))
    if naam:
        p.name = naam
    return p


def kicker(s, t, kl='teal', y=90):
    txt(s, 100, y, 1500, 34, t, gr=12.5, kl=kl, vet=True, font=FONT_M, sp=2.4, caps=True)


def kop(s, t, y=132, gr=40, kl='ink', w=1560, naam=None):
    txt(s, 100, y, w, 200, t, gr=gr, kl=kl, vet=True, ra=1.1, naam=naam)


def notitie(s, d):
    tf = s.notes_slide.notes_text_frame
    tf.text = ('PRESENTATIETIP\n' + d.get('tip', '') +
               '\n\nINTERACTIE\n' + d.get('interactie', ''))


def morph(s, soort='morph'):
    """PowerPoint-morphovergang, met fade als terugval op oudere versies."""
    if soort == 'fade':
        xml = ('<p:transition xmlns:p="http://schemas.openxmlformats.org/'
               'presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/'
               'office/powerpoint/2010/main" spd="slow" p14:dur="900"><p:fade/></p:transition>')
    else:
        xml = (
          '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/'
          'markup-compatibility/2006" xmlns:p="http://schemas.openxmlformats.org/'
          'presentationml/2006/main">'
          '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" '
          'Requires="p159">'
          '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
          'spd="slow" p14:dur="1200"><p159:morph option="byObject"/></p:transition></mc:Choice>'
          '<mc:Fallback>'
          '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
          'spd="slow" p14:dur="900"><p:fade/></p:transition></mc:Fallback>'
          '</mc:AlternateContent>')
    s._element.append(etree.fromstring(xml))


prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
leeg = prs.slide_layouts[6]
TOT = len(SLIDES)


def nieuw():
    s = prs.slides.add_slide(leeg)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, px(B), px(H))
    bg.fill.solid(); bg.fill.fore_color.rgb = rgb('bg')
    bg.line.fill.background(); bg.shadow.inherit = False
    return s


def paginering(s, i):
    txt(s, 1660, 1006, 160, 28, '%02d / %02d' % (i, TOT), gr=10.5, kl='gedempt',
        font=FONT_M, uit=PP_ALIGN.RIGHT)


for i, d in enumerate(SLIDES, 1):
    t, s = d['t'], nieuw()

    if t == 'hero_titel':
        tegel(s, 100, 150, 1720, 470, 'tegel', 'rand', alpha=60)
        txt(s, 150, 206, 1400, 270, d['boven'], gr=110, kl='ink', vet=True,
            ra=0.92, naam='hero')
        txt(s, 156, 442, 1200, 90, d['onder'], gr=36, kl='teal', vet=True)
        txt(s, 156, 552, 1300, 70, d['staart'], gr=18, kl='gedempt', font=FONT_L)
        for j, (g, l) in enumerate(d['tegels']):
            x, w = kol(j * 4, 4)
            tegel(s, x, 664, w, 210, 'tegel2', 'rand')
            txt(s, x + 34, 698, w - 60, 120, g, gr=56, kl='teal', vet=True, ra=1.0)
            txt(s, x + 36, 810, w - 60, 40, l, gr=14, kl='gedempt', font=FONT_M,
                caps=True, sp=1.4)
        txt(s, 100, 1006, 1500, 30, d['voet'], gr=11.5, kl='gedempt', font=FONT_M)

    elif t == 'sectie':
        txt(s, 100, 292, 700, 320, d['nr'], gr=150, kl='teal', vet=True, ra=0.9, naam='hero')
        txt(s, 100, 626, 1400, 140, d['titel'], gr=56, kl='ink', vet=True, naam='sectietitel')
        txt(s, 104, 786, 1300, 80, d['regel'], gr=21, kl='gedempt', font=FONT_L)
        paginering(s, i)

    elif t == 'keuze':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (nr, naam, sub) in enumerate(d['tegels']):
            x, w = kol(j * 3, 3)
            tegel(s, x, 340, w, 480, 'tegel', 'rand')
            txt(s, x + 30, 380, w - 60, 66, nr, gr=28, kl='teal', vet=True, font=FONT_M)
            txt(s, x + 30, 466, w - 60, 120, naam, gr=23, kl='ink', vet=True, ra=1.15)
            txt(s, x + 30, 606, w - 60, 180, sub, gr=15, kl='gedempt', ra=1.35)
        paginering(s, i)

    elif t == 'hero_cijfer':
        acc = d.get('accent', 'teal')
        gloed(s, -160, 40, 820, acc, 6)
        # het cijfer loopt bewust buiten het kader: schaal als beeldmiddel
        txt(s, 60, 120, 1200, 520, d['cijfer'], gr=250, kl=acc, vet=True, ra=0.82,
            naam='hero')
        txt(s, 700, 208, 240, 160, d['suffix'], gr=76, kl=acc, vet=True, font=FONT_L)
        txt(s, 104, 626, 860, 200, d['kop'], gr=32, kl='ink', vet=True, ra=1.2)
        if d.get('meter'):
            # meter met streefwaarde: laat zien hoe ver het van de norm ligt
            m = d['meter']
            txt(s, 1000, 300, 800, 36, m['label'], gr=13, kl='gedempt', font=FONT_M,
                caps=True, sp=1.4)
            yy = 350
            for lbl, waarde in m['staven']:
                txt(s, 1000, yy, 260, 36, lbl, gr=15, kl='gedempt')
                staaf(s, 1000, yy + 42, 700, 40, waarde / 100.0, acc)
                txt(s, 1720, yy + 38, 110, 44, '%d%%' % waarde, gr=22, kl='ink', vet=True)
                yy += 118
            merkstreep(s, 1000 + 700 * 0.80, 344, 348)
            txt(s, 1000 + 700 * 0.80 - 100, 704, 200, 36, 'norm 80%', gr=13, kl='ink',
                vet=True, font=FONT_M, uit=PP_ALIGN.CENTER)
        else:
            for j, (g, l) in enumerate(d['tegels']):
                x, w = kol(8, 4)
                y = 180 + j * 216
                tegel(s, x, y, w, 190, 'tegel', 'rand')
                txt(s, x + 32, y + 28, w - 60, 96, g, gr=42, kl='ink', vet=True, ra=1.0)
                txt(s, x + 34, y + 124, w - 60, 40, l, gr=13.5, kl='gedempt',
                    font=FONT_M, caps=True, sp=1.3)
        txt(s, 100, 1006, 1400, 30, d['voet'], gr=11.5, kl='gedempt', font=FONT_M)
        paginering(s, i)

    elif t == 'splitsing':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        # proportionele staven: lengte draagt de vergelijking, niet het cijfer
        y = 288
        for kant in (d['links'], d['rechts']):
            liniaal(s, 100, y, 1720)
            txt(s, 100, y + 26, 600, 50, kant['titel'], gr=22, kl='ink', vet=True)
            txt(s, 102, y + 82, 600, 34, kant['sub'], gr=13, kl='gedempt', font=FONT_M)
            for lbl, waarde, kl in ((kant['ref_lbl'], kant['ref'], 'gedempt'),
                                    (kant['int_lbl'], float(kant['groot'].replace(',', '.')),
                                     kant['kleur'])):
                yy = y + (140 if kl == 'gedempt' else 206)
                txt(s, 100, yy + 8, 320, 34, lbl, gr=14, kl='gedempt', font=FONT_M)
                staaf(s, 440, yy, 1080, 46, waarde / 50.0, kl)
                txt(s, 1560, yy - 4, 220, 54,
                    ('%.1f' % waarde).replace('.', ',') + '%', gr=27, kl=kl, vet=True)
            txt(s, 100, y + 274, 900, 44, kant['slot'], gr=18, kl=kant['kleur'], vet=True)
            y += 356
        txt(s, 900, 934, 920, 60, d['punchline'], gr=24, kl='ink', vet=True,
            uit=PP_ALIGN.RIGHT)
        txt(s, 100, 1006, 1400, 30, d['voet'], gr=11.5, kl='gedempt', font=FONT_M)
        paginering(s, i)

    elif t == 'formule':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (naam, sub, kl, tag) in enumerate(d['delen']):
            x, w = kol(j * 4, 4)
            tegel(s, x, 400, w - 40, 310, 'tegel', 'rand')
            txt(s, x + 30, 436, w - 100, 66, naam, gr=25, kl='ink', vet=True)
            txt(s, x + 30, 504, w - 100, 56, sub, gr=15, kl='gedempt')
            tegel(s, x + 30, 598, 160, 44, kl if kl != 'gedempt' else 'glas', None)
            txt(s, x + 30, 610, 160, 32, tag, gr=11,
                kl='bg' if kl != 'gedempt' else 'gedempt', vet=True, font=FONT_M,
                uit=PP_ALIGN.CENTER, caps=True, sp=1.2)
            if j < 2:
                txt(s, x + w - 48, 512, 64, 90, '×', gr=34, kl='gedempt',
                    uit=PP_ALIGN.CENTER, font=FONT_L)
        txt(s, 100, 770, 1720, 90, d['slot'], gr=20, kl='gedempt', ra=1.4)
        paginering(s, i)

    elif t == 'duo':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, c in enumerate((d['een'], d['twee'])):
            x, w = kol(j * 6, 6)
            tegel(s, x, 320, w, 570, 'tegel', 'rand')
            txt(s, x + 40, 354, 200, 60, c['nr'], gr=26, kl='teal', vet=True, font=FONT_M)
            txt(s, x + 40, 418, w - 80, 110, c['naam'], gr=24, kl='ink', vet=True, ra=1.15)
            tegel(s, x + 40, 548, w - 80, 84, 'glas', None)
            txt(s, x + 40, 572, w - 80, 48, c['kern'], gr=18, kl='teal', vet=True,
                uit=PP_ALIGN.CENTER, font=FONT_M)
            txt(s, x + 40, 668, w - 80, 200,
                [(r, {'voor': 13}) for r in c['regels']], gr=15, kl='gedempt', ra=1.35)
        paginering(s, i)

    elif t == 'statraster':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        # 144 deelnemers als puntenmatrix, 72 per arm
        kleuren = ['teal'] * 72 + ['koraal'] * 72
        matrix(s, 100, 300, 144, 24, 26, 12, kleuren)
        txt(s, 100, 520, 400, 40, '72 PARADISE', gr=13, kl='teal', vet=True,
            font=FONT_M, sp=1.4)
        txt(s, 380, 520, 400, 40, '72 GEBRUIKELIJKE ZORG', gr=13, kl='koraal',
            vet=True, font=FONT_M, sp=1.4)
        txt(s, 1080, 286, 740, 250,
            'Elke stip is een patiënt die u zelf includeert.\n24 per kliniek.',
            gr=30, kl='ink', vet=True, ra=1.3)
        for j, (k2, v) in enumerate(d['klein']):
            x, w = kol((j % 2) * 6, 6)
            y = 606 + (j // 2) * 132
            tegel(s, x, y, w, 114, 'tegel', 'rand')
            txt(s, x + 30, y + 20, w - 60, 34, k2, gr=12, kl='teal', vet=True,
                font=FONT_M, caps=True, sp=1.4)
            txt(s, x + 30, y + 58, w - 60, 46, v, gr=15.5, kl='ink')
        paginering(s, i)

    elif t == 'steun':
        # asymmetrisch: lijst links, één groot geruststellend cijfer rechts
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (k2, v) in enumerate(d['rijen']):
            y = 314 + j * 152
            liniaal(s, 100, y, 980)
            txt(s, 100, y + 26, 980, 50, k2, gr=21, kl='ink', vet=True)
            txt(s, 102, y + 76, 960, 60, v, gr=15.5, kl='gedempt', ra=1.3)
        tegel(s, 1180, 300, 640, 622, 'tegel2', 'amber')
        gloed(s, 1260, 322, 480, 'amber', 5)
        txt(s, 1224, 340, 560, 300, d['cijfer'], gr=150, kl='amber', vet=True, ra=0.9,
            uit=PP_ALIGN.CENTER, naam='hero')
        txt(s, 1224, 640, 560, 62, d['cijfer_label'], gr=30, kl='ink', vet=True,
            uit=PP_ALIGN.CENTER)
        txt(s, 1230, 722, 540, 160, d['cijfer_regel'], gr=16, kl='gedempt', ra=1.4,
            uit=PP_ALIGN.CENTER)
        paginering(s, i)

    elif t == 'dubbelkolom':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, kant in enumerate((d['links'], d['rechts'])):
            x, w = kol(j * 6, 6)
            tegel(s, x, 314, w, 606, 'tegel', 'rand')
            tegel(s, x + 40, 348, 120, 46, kant['kleur'], None)
            txt(s, x + 40, 360, 120, 34, kant['titel'], gr=13.5, kl='bg', vet=True,
                uit=PP_ALIGN.CENTER, font=FONT_M, caps=True, sp=1.3)
            txt(s, x + 40, 432, w - 80, 470,
                [(it, {'voor': 15}) for it in kant['items']], gr=15.5, kl='gedempt',
                ra=1.3)
        paginering(s, i)

    elif t in ('traject', 'zoom'):
        # Doorlopend canvas: elke dia toont hetzelfde traject onder een andere
        # camera-instelling. Morph koppelt de vormen via hun !!-naam en maakt
        # er een vloeiende in- of uitzoom van in plaats van een dia-wissel.
        kicker(s, d['kicker'], y=56)
        kop(s, d['kop'], y=96, naam='!!sectietitel')
        band = tegel(s, 0, 190, 1920, 520, 'tegel', None, rond=False)
        band.name = '!!band'
        if t == 'traject':
            beeld.canvas(s, PUNTEN, txt, liniaal, 1.0, 960, 454, 960, 480)
            txt(s, 100, 764, 320, 230, d['groot'], gr=96, kl='amber', vet=True,
                ra=1.0, omslag=False, naam='!!camera')
            txt(s, 460, 782, 1340, 66, d['punt'], gr=30, kl='ink', vet=True)
            txt(s, 462, 858, 1340, 120, d['slot'], gr=18, kl='gedempt', ra=1.4)
        else:
            beeld.canvas(s, PUNTEN, txt, liniaal, d['schaal'], d['mid'], 454,
                         d.get('ox', 560), 500)
            p = d['paneel']
            liniaal(s, 100, 748, 1720)
            txt(s, 100, 772, 420, 60, p['titel'], gr=24, kl='amber', vet=True,
                naam='!!camera')
            for j, r in enumerate(p['regels']):
                txt(s, 560 + j * 660, 770, 600, 200, r, gr=16.5, kl='gedempt', ra=1.35)
        paginering(s, i)

    elif t == 'drukmeting':
        # De sensormatrix is geen illustratie maar de meting zelf: dezelfde
        # cellen op beide dia's, alleen de kleur verandert. Morph laat de
        # drukpiek daardoor letterlijk afkoelen.
        kicker(s, d['kicker'])
        kop(s, d['kop'], naam='!!sectietitel')
        beeld.drukmat(s, 70, 216, 450, 690,
                      beeld.NA if d['fase'] == 'na' else beeld.VOOR, sleutel='p',
                      piek=float(d['waarde']))
        beeld.schaalbalk(s, 145, 930, 300, 16, txt)
        acc = 'teal' if d['fase'] == 'na' else 'koraal'
        txt(s, 560, 250, 700, 300, d['waarde'], gr=150, kl=acc, vet=True, ra=0.9,
            omslag=False, naam='!!piek')
        txt(s, 1080, 300, 200, 80, 'kPa', gr=44, kl=acc, vet=True, font=FONT_L,
            naam='!!eenheid')
        txt(s, 564, 528, 1200, 60, d['plek'], gr=22, kl='ink', vet=True,
            naam='!!plek')
        tegel(s, 560, 618, 1260, 96, 'glas', None, naam='!!norm')
        txt(s, 560, 646, 1260, 46, d['norm'], gr=22, kl='amber', vet=True,
            uit=PP_ALIGN.CENTER, font=FONT_M, naam='!!normtekst')
        txt(s, 560, 760, 1260, 200,
            [(r, {'voor': 12}) for r in d['regels']], gr=17, kl='gedempt', ra=1.35)
        txt(s, 100, 1006, 1400, 30, d['voet'], gr=11.5, kl='gedempt', font=FONT_M)
        paginering(s, i)

    elif t == 'vijfluik':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (nr, wanneer, wat) in enumerate(d['stappen']):
            x = 100 + j * 348
            tegel(s, x, 330, 324, 540, 'tegel', 'rand')
            txt(s, x + 28, 364, 260, 60, nr, gr=27, kl='teal', vet=True, font=FONT_M)
            txt(s, x + 28, 440, 268, 66, wanneer, gr=20, kl='ink', vet=True)
            txt(s, x + 28, 524, 268, 320, wat, gr=15, kl='gedempt', ra=1.38)
        paginering(s, i)

    elif t == 'drieluik':
        # echte bento: één groot vlak links, twee gestapelde rechts
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        g, rest = d['kaarten'][0], d['kaarten'][1:]
        gx, gw = kol(0, 6)
        tegel(s, gx, 310, gw, 630, 'tegel', 'rand')
        foto(s, g['foto'], gx + 40, 344, gw - 80, 262)
        txt(s, gx + 44, 626, 380, 70, g['naam'], gr=32, kl='ink', vet=True)
        txt(s, gx + 46, 700, 380, 36, g['sub'], gr=12.5, kl='teal', vet=True,
            font=FONT_M, caps=True, sp=1.6)
        txt(s, gx + 44, 734, 380, 60, g['groot'] + '  ' + g['onder'], gr=24,
            kl='teal', vet=True, ra=1.0)
        txt(s, gx + 44, 800, 380, 40, g['wie'], gr=13, kl='amber', vet=True,
            font=FONT_M, caps=True, sp=1.3)
        txt(s, gx + 448, 626, gw - 492, 280,
            [(r, {'voor': 10}) for r in g['regels']], gr=14.5, kl='gedempt', ra=1.3)
        for j, c in enumerate(rest):
            x, w = kol(6, 6)
            y = 310 + j * 328
            tegel(s, x, y, w, 302, 'tegel', 'rand')
            tegel(s, x + 24, y + 24, 340, 254, c.get('vlak', 'tegel2'), None)
            foto(s, c['foto'], x + 36, y + 36, 316, 230)
            tx = x + 400
            txt(s, tx, y + 30, 420, 54, c['naam'], gr=25, kl='ink', vet=True)
            txt(s, tx + 2, y + 88, 420, 34, c['sub'], gr=12, kl='teal', vet=True,
                font=FONT_M, caps=True, sp=1.5)
            txt(s, tx, y + 120, 420, 56, c['groot'] + '  ' + c['onder'], gr=22,
                kl='teal', vet=True, ra=1.0)
            txt(s, tx, y + 174, w - 440, 90,
                [(r, {'voor': 6}) for r in c['regels']], gr=14, kl='gedempt', ra=1.28)
            txt(s, tx, y + 264, 420, 36, c['wie'], gr=12.5, kl='amber', vet=True,
                font=FONT_M, caps=True, sp=1.3)
        paginering(s, i)

    elif t == 'vierluik':
        # rijen in plaats van kolommen: leest sneller en breekt het kaartenritme
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (rol, punten) in enumerate(d['kolommen']):
            y = 304 + j * 164
            liniaal(s, 100, y, 1720)
            txt(s, 100, y + 34, 420, 60, rol, gr=27, kl='ink', vet=True)
            for k, p in enumerate(punten):
                px_ = 560 + k * 428
                punt(s, px_, y + 48, 11, 'teal')
                txt(s, px_ + 26, y + 36, 372, 90, p, gr=15.5, kl='gedempt', ra=1.3)
        liniaal(s, 100, 960, 1720)
        paginering(s, i)

    elif t == 'statement':
        kicker(s, d['kicker'], kl='koraal')
        txt(s, 100, 168, 1080, 400, d['kop'], gr=54, kl='ink', vet=True, ra=1.08, naam='hero')
        tegel(s, 100, 646, 1080, 244, 'tegel', 'rand')
        txt(s, 144, 690, 1000, 190, d['body'], gr=17.5, kl='gedempt', ra=1.45)
        tegel(s, 1240, 320, 580, 554, 'tegel2', 'koraal')
        txt(s, 1288, 366, 490, 38, 'Uitzondering', gr=12.5, kl='koraal', vet=True,
            font=FONT_M, caps=True, sp=1.6)
        txt(s, 1288, 430, 490, 400, d['uitzondering'], gr=18, kl='ink', ra=1.45)
        paginering(s, i)

    elif t == 'eerlijk':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        txt(s, 100, 264, 1400, 44, d['intro'], gr=16.5, kl='gedempt')
        for j, (k2, v) in enumerate(d['rijen']):
            x, w = kol((j % 2) * 6, 6)
            y = 336 + (j // 2) * 142
            tegel(s, x, y, w, 122, 'tegel', 'rand')
            txt(s, x + 32, y + 22, w - 64, 36, k2, gr=12.5, kl='teal', vet=True,
                font=FONT_M, caps=True, sp=1.4)
            txt(s, x + 32, y + 64, w - 64, 46, v, gr=17, kl='ink')
        tegel(s, 100, 646, 1720, 150, 'tegel2', 'teal')
        txt(s, 150, 692, 1620, 110, d['slot'], gr=19, kl='ink', ra=1.4)
        paginering(s, i)

    elif t == 'pauze':
        kicker(s, d['kicker'], kl='amber')
        txt(s, 100, 372, 1720, 280, d['kop'], gr=120, kl='ink', vet=True,
            uit=PP_ALIGN.CENTER, ra=1.0, naam='hero')
        txt(s, 100, 700, 1720, 70, d['regel'], gr=23, kl='gedempt',
            uit=PP_ALIGN.CENTER, font=FONT_L)
        paginering(s, i)

    elif t == 'vraagraster':
        # geen kaders: enkel haarlijnen, vraag in wit, antwoord ingesprongen
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (v, a) in enumerate(d['paren']):
            x, w = kol((j % 2) * 6, 6)
            y = 300 + (j // 2) * 226
            liniaal(s, x, y, w)
            txt(s, x, y + 26, w, 60, v, gr=19, kl='ink', vet=True, ra=1.2)
            txt(s, x, y + 96, 30, 40, '—', gr=15, kl='teal', vet=True)
            txt(s, x + 40, y + 94, w - 40, 100, a, gr=15.5, kl='gedempt', ra=1.35)
        paginering(s, i)

    elif t == 'afspraak':
        # één blad in plaats van vier tegels: dit leest als een overeenkomst
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        tegel(s, 100, 300, 1720, 622, 'tegel', 'rand')
        for j, (g, m, sub) in enumerate(d['tegels']):
            y = 344 + j * 146
            if j:
                liniaal(s, 168, y - 26, 1584)
            txt(s, 118, y, 300, 120, g, gr=54, kl='teal', vet=True, ra=1.0,
                uit=PP_ALIGN.RIGHT, omslag=False)
            txt(s, 470, y + 8, 900, 60, m, gr=26, kl='ink', vet=True)
            txt(s, 472, y + 62, 1250, 50, sub, gr=16, kl='gedempt')
        paginering(s, i)

    elif t == 'slot':
        txt(s, 100, 296, 1200, 230, d['kop'], gr=96, kl='ink', vet=True, ra=1.0, naam='hero')
        txt(s, 104, 548, 1300, 80, d['regel'], gr=23, kl='teal', font=FONT_L)
        tegel(s, 100, 664, 1000, 226, 'tegel', 'rand')
        txt(s, 148, 708, 920, 170,
            [(r, {'voor': 8}) for r in d['contact']], gr=16.5, kl='gedempt', ra=1.45)
        txt(s, 100, 1006, 1500, 30, d['voet'], gr=11.5, kl='gedempt', font=FONT_M)

    else:
        raise SystemExit('onbekend type: %s' % t)

    notitie(s, d)
    morph(s, d.get('morph', 'morph'))

prs.save(DOEL)
print("%d dia's · %.0f KB · %s" % (TOT, os.path.getsize(DOEL) / 1024, os.path.basename(DOEL)))
