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

from inhoud import SLIDES, K, FONT, FONT_L, FONT_M, kol

HIER = os.path.dirname(os.path.abspath(__file__))
DOEL = os.path.join(HIER, 'PARADISE_informatiesessie_voetklinieken.pptx')

B, H = 1920, 1080
SCH = 13.333 / B


def px(v):
    return Inches(v * SCH)


def rgb(n):
    return RGBColor.from_string(K[n])


def tegel(s, x, y, w, h, vul='tegel', rand='rand', alpha=None, rond=True):
    """Bento-tegel; alpha geeft het glaseffect."""
    vorm = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rond else MSO_SHAPE.RECTANGLE,
        px(x), px(y), px(w), px(h))
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
        uit=PP_ALIGN.LEFT, ra=1.25, sp=0, anker=MSO_ANCHOR.TOP, caps=False, naam=None):
    tb = s.shapes.add_textbox(px(x), px(y), px(w), px(h))
    if naam:
        tb.name = naam
    tf = tb.text_frame
    tf.word_wrap = True
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
        txt(s, 96, 178, 1000, 400, d['cijfer'], gr=170, kl=acc, vet=True, ra=0.88, naam='hero')
        txt(s, 496, 232, 200, 130, d['suffix'], gr=58, kl=acc, vet=True, font=FONT_L)
        txt(s, 104, 588, 900, 200, d['kop'], gr=30, kl='ink', vet=True, ra=1.2)
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
        for j, kant in enumerate((d['links'], d['rechts'])):
            x, w = kol(j * 6, 6)
            tegel(s, x, 320, w, 440, 'tegel', 'rand')
            txt(s, x + 40, 354, w - 80, 48, kant['titel'], gr=21, kl='ink', vet=True)
            txt(s, x + 40, 404, w - 80, 34, kant['sub'], gr=12.5, kl='gedempt', font=FONT_M)
            txt(s, x + 40, 456, w - 80, 190, kant['groot'] + '%', gr=76, kl=kant['kleur'],
                vet=True, ra=0.95)
            txt(s, x + 44, 626, w - 80, 44, kant['klein'], gr=15.5, kl='gedempt')
            txt(s, x + 40, 690, w - 80, 48, kant['slot'], gr=18, kl=kant['kleur'], vet=True)
        txt(s, 100, 812, 1720, 70, d['punchline'], gr=25, kl='ink', vet=True,
            uit=PP_ALIGN.CENTER)
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
        for j, (g, l) in enumerate(d['groot']):
            x, w = kol(j * 3, 3)
            tegel(s, x, 320, w, 230, 'tegel', 'rand')
            txt(s, x + 30, 352, w - 60, 116, g, gr=50, kl='teal', vet=True, ra=1.0)
            txt(s, x + 32, 474, w - 60, 40, l, gr=13, kl='gedempt', font=FONT_M,
                caps=True, sp=1.3)
        for j, (k2, v) in enumerate(d['klein']):
            x, w = kol((j % 2) * 6, 6)
            y = 586 + (j // 2) * 132
            tegel(s, x, y, w, 114, 'tegel2', 'rand')
            txt(s, x + 30, y + 20, w - 60, 34, k2, gr=12, kl='teal', vet=True,
                font=FONT_M, caps=True, sp=1.4)
            txt(s, x + 30, y + 58, w - 60, 46, v, gr=15.5, kl='ink')
        paginering(s, i)

    elif t == 'dubbelkolom':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, kant in enumerate((d['links'], d['rechts'])):
            x, w = kol(j * 6, 6)
            tegel(s, x, 320, w, 560, 'tegel', 'rand')
            tegel(s, x + 40, 354, 120, 46, kant['kleur'], None)
            txt(s, x + 40, 366, 120, 34, kant['titel'], gr=13.5, kl='bg', vet=True,
                uit=PP_ALIGN.CENTER, font=FONT_M, caps=True, sp=1.3)
            txt(s, x + 40, 438, w - 80, 420,
                [(it, {'voor': 17}) for it in kant['items']], gr=16, kl='gedempt', ra=1.3)
        paginering(s, i)

    elif t == 'tijdlijn':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        n = len(d['punten'])
        bx, bw = 100, 1720
        stap = bw / n
        tegel(s, bx, 430, bw, 3, 'rand', None, rond=False)
        for j, (wanneer, wat) in enumerate(d['punten']):
            cx = bx + stap * j + stap / 2
            c = s.shapes.add_shape(MSO_SHAPE.OVAL, px(cx - 13), px(419), px(26), px(26))
            c.fill.solid(); c.fill.fore_color.rgb = rgb('teal' if wat else 'rand')
            c.line.color.rgb = rgb('bg'); c.line.width = Pt(2.5); c.shadow.inherit = False
            txt(s, cx - stap / 2, 356, stap, 44, wanneer, gr=16, kl='ink', vet=True,
                uit=PP_ALIGN.CENTER, font=FONT_M)
            if wat:
                txt(s, cx - stap / 2, 478, stap, 70, wat, gr=13, kl='teal',
                    uit=PP_ALIGN.CENTER, font=FONT_M)
        tegel(s, 100, 640, 1720, 220, 'tegel', 'rand')
        txt(s, 150, 698, 1620, 130, d['slot'], gr=22, kl='ink', ra=1.45)
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
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, c in enumerate(d['kaarten']):
            x, w = kol(j * 4, 4)
            tegel(s, x, 320, w, 570, 'tegel', 'rand')
            txt(s, x + 32, 354, w - 64, 54, c['naam'], gr=23, kl='ink', vet=True)
            txt(s, x + 32, 408, w - 64, 36, c['sub'], gr=12, kl='teal', vet=True,
                font=FONT_M, caps=True, sp=1.4)
            txt(s, x + 32, 462, w - 64, 124, c['groot'], gr=58, kl='teal', vet=True, ra=1.0)
            txt(s, x + 34, 582, w - 64, 40, c['onder'], gr=13.5, kl='gedempt', font=FONT_M)
            txt(s, x + 32, 652, w - 64, 150,
                [(r, {'voor': 12}) for r in c['regels']], gr=14, kl='gedempt', ra=1.32)
            tegel(s, x + 32, 808, w - 64, 52, 'glas', None)
            txt(s, x + 32, 822, w - 64, 36, c['wie'], gr=13.5, kl='teal', vet=True,
                uit=PP_ALIGN.CENTER)
        paginering(s, i)

    elif t == 'vierluik':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (rol, punten) in enumerate(d['kolommen']):
            x, w = kol(j * 3, 3)
            tegel(s, x, 320, w, 520, 'tegel', 'rand')
            tegel(s, x, 320, w, 78, 'tegel2', None)
            txt(s, x + 28, 342, w - 56, 46, rol, gr=20, kl='teal', vet=True)
            txt(s, x + 28, 432, w - 56, 380,
                [(p, {'voor': 17}) for p in punten], gr=15, kl='gedempt', ra=1.32)
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
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (v, a) in enumerate(d['paren']):
            x, w = kol((j % 2) * 6, 6)
            y = 306 + (j // 2) * 238
            tegel(s, x, y, w, 208, 'tegel', 'rand')
            txt(s, x + 32, y + 26, w - 64, 66, v, gr=17.5, kl='ink', vet=True, ra=1.2)
            txt(s, x + 32, y + 102, w - 64, 92, a, gr=15, kl='gedempt', ra=1.35)
        paginering(s, i)

    elif t == 'afspraak':
        kicker(s, d['kicker']); kop(s, d['kop'], naam='sectietitel')
        for j, (g, m, sub) in enumerate(d['tegels']):
            x, w = kol(j * 3, 3)
            tegel(s, x, 330, w, 470, 'tegel', 'rand')
            txt(s, x + 30, 370, w - 60, 136, g, gr=58, kl='teal', vet=True, ra=1.0)
            txt(s, x + 30, 514, w - 60, 54, m, gr=20, kl='ink', vet=True)
            txt(s, x + 30, 582, w - 60, 190, sub, gr=14.5, kl='gedempt', ra=1.35)
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
