# -*- coding: utf-8 -*-
"""Bouwt de animatiefilm over PARADISE als PowerPoint, klaar om te renderen.

Waarom zo. De AI-videodiensten vielen af, maar er stond al een werkende
animatie in het deck: de drukmat die van rood naar blauw morpht. Dat is echte
animatie, getekend uit PowerPoint-vormen, en PowerPoint exporteert het
rechtstreeks naar MP4. Geen account, geen tegoed, geen dienst — en achteraf
gewoon aanpasbaar.

Hoe het beweegt. Elke dia draagt een morph-overgang en een eigen tijd. Vormen
die tussen twee dia's dezelfde `!!`-naam hebben, koppelt PowerPoint één op één;
alles wat aan zo'n vorm verschilt — plaats, hoek, kleur, grootte — wordt vloeiend
doorlopen in plaats van hard verwisseld. Een dia is dus geen beeld maar een
sleutelmoment, zoals bij klassieke animatie.

Renderen:

    python maak_film.py            # bouwt PARADISE_animatie.pptx
    python maak_film.py --video    # en laat PowerPoint er een mp4 van maken
"""
import os, sys, math, copy
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

from inhoud import K, FONT, FONT_M
import beeld

HIER = os.path.dirname(os.path.abspath(__file__))
DOEL = os.path.join(HIER, 'PARADISE_animatie.pptx')
B, H = 1920, 1080
SCH = 13.333 / B


def px(v):
    return Inches(v * SCH)


def rgb(n):
    return RGBColor.from_string(K[n] if n in K else n)


def hex_(n):
    return K[n] if n in K else n


def meng_kl(n, f, naar=(0, 0, 0)):
    """Kleur richting zwart (f < 1) of richting een andere kleur toe schuiven.

    Elke vorm krijgt hiermee een omlijning en een schaduwzijde in zijn eigen
    kleur. Dat is het verschil tussen een plat blokje en iets dat getekend lijkt.
    """
    h = hex_(n)
    d = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return '%02X%02X%02X' % tuple(
        max(0, min(255, int(c * f + n2 * (1 - f)))) for c, n2 in zip(d, naar))


def lichter(n, f=0.35):
    return meng_kl(n, 1 - f, (255, 255, 255))


prs = Presentation()
prs.slide_width, prs.slide_height = px(B), px(H)
LEEG = prs.slide_layouts[6]
TIJDEN = []


def verloop(vorm_, van, naar, hoek=5400000):
    """Kleurverloop in plaats van een vlakke kleur. Op een groot scherm is een
    egaal vlak het eerste wat goedkoop oogt."""
    vorm_.fill.solid()
    oud = vorm_.fill._xPr.find(qn('a:solidFill'))
    # ter plaatse vervangen, niet vooraan invoegen: in spPr moet de vulling ná
    # a:xfrm en a:prstGeom komen, anders negeert PowerPoint hem en wordt de
    # vorm wit
    oud.getparent().replace(oud, etree.fromstring(
        '<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/'
        '2006/main" rotWithShape="1"><a:gsLst>'
        '<a:gs pos="0"><a:srgbClr val="%s"/></a:gs>'
        '<a:gs pos="100000"><a:srgbClr val="%s"/></a:gs>'
        '</a:gsLst><a:lin ang="%d" scaled="0"/></a:gradFill>'
        % (hex_(van), hex_(naar), hoek)))


def dia(stand, morph_ms=900, eerste=False):
    """Nieuwe dia met grond, morph-overgang en een eigen standtijd.

    `stand` is hoe lang het beeld blijft staan nádat de overgang klaar is.
    Zet hem op nul en geef de overgang de hele beat: dan loopt de beweging
    door in plaats van te verspringen. Dat is het verschil tussen een
    diavoorstelling en een film.
    """
    s = prs.slides.add_slide(LEEG)
    g = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, px(B), px(H))
    g.line.fill.background(); g.shadow.inherit = False
    g.name = '!!grond'
    # donker bovenaan, iets lichter naar de horizon toe: andersom oogt het als
    # een vignet in plaats van als lucht
    # klein bereik: een breed verloop toont zichtbare banden op een groot scherm
    verloop(g, meng_kl('bg', 0.80), lichter('bg', .05), 5400000)
    ms = max(10, int(stand * 1000))
    duur = 250 if eerste else morph_ms
    s._element.append(etree.fromstring(
        '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/'
        'markup-compatibility/2006" xmlns:p="http://schemas.openxmlformats.org/'
        'presentationml/2006/main">'
        '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/'
        '2015/09/main" Requires="p159">'
        '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/'
        '2010/main" spd="slow" p14:dur="%d" advClick="0" advTm="%d">'
        '<p159:morph option="byObject"/></p:transition></mc:Choice>'
        '<mc:Fallback><p:transition xmlns:p14="http://schemas.microsoft.com/'
        'office/powerpoint/2010/main" spd="slow" p14:dur="%d" advClick="0" '
        'advTm="%d"><p:fade/></p:transition></mc:Fallback>'
        '</mc:AlternateContent>' % (duur, ms, duur, ms)))
    TIJDEN.append(stand + duur / 1000.0)
    return s


def vorm(s, soort, x, y, w, h, vul=None, lijn=None, dik=2.5, rot=0,
         naam=None, alpha=None, rond=None, omlijn=0):
    if omlijn and vul and not lijn:
        lijn, dik = meng_kl(vul, 0.52), omlijn
    o = s.shapes.add_shape(soort, px(x), px(y), px(w), px(h))
    if vul:
        o.fill.solid(); o.fill.fore_color.rgb = rgb(vul)
        if alpha is not None:
            sf = o.fill.fore_color._xFill.find(
                '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
            etree.SubElement(sf, '{http://schemas.openxmlformats.org/drawingml/'
                             '2006/main}alpha').set('val', str(int(alpha * 1000)))
    else:
        o.fill.background()
    if lijn:
        o.line.color.rgb = rgb(lijn); o.line.width = Pt(dik)
    else:
        o.line.fill.background()
    o.shadow.inherit = False
    if rot:
        o.rotation = rot
    if rond is not None:
        try:
            o.adjustments[0] = rond
        except Exception:
            pass
    if naam:
        o.name = naam
    return o


def txt(s, x, y, w, h, tekst, gr=30, kl='ink', vet=False, font=FONT,
        uit=PP_ALIGN.LEFT, ra=1.2, naam=None, anker=MSO_ANCHOR.TOP, sp=0):
    tb = s.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anker
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, r in enumerate(tekst.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = uit
        p.line_spacing = ra
        run = p.add_run(); run.text = r
        f = run.font
        f.name = font; f.size = Pt(gr); f.bold = vet
        f.color.rgb = rgb(kl)
        if sp:
            run.font._rPr.set('spc', str(int(sp * 100)))
    if naam:
        tb.name = naam
    return tb


# --------------------------------------------------------------- personages
# Opa Frans en Lotte, getekend uit vormen in een raster van 100 bij 130.
# Elk onderdeel houdt over alle dia's dezelfde !!-naam, zodat morph de figuur
# laat lopen in plaats van hem te verversen.

FRANS = dict(haar='C9D6E0', huid='F0C9A6', romp='mid', broek='navy',
             schoen='gedempt', bril=True, snor=True, vlecht=False,
             kraag=True, zak=False)
LOTTE = dict(haar='8A5A3B', huid='F7D6B4', romp='groen', broek='navy',
             schoen='oranje', bril=False, snor=False, vlecht=True,
             kraag=False, zak=True)


def _eind(cx, cy, dy, hoek):
    """Waar het uiteinde van een gedraaide ledemaat terechtkomt.

    Zonder deze berekening blijft de hand of de schoen staan waar hij stond en
    valt hij los van de arm of het been zodra die draait — precies wat de
    eerste versie zo houterig maakte.
    """
    a = math.radians(hoek)
    return cx - dy * math.sin(a), cy + dy * math.cos(a)


def figuur(s, wie, sl, x, y, sc=1.0, been=(0, 0), arm=(0, 0), mond='lach'):
    """Tekent een personage; `been` en `arm` zijn hoeken in graden.

    Opgebouwd van achter naar voor, zoals je het zou tekenen: eerst het haar
    achter het hoofd, dan de ledematen, dan de romp, dan pas het gezicht.
    """
    lw = max(1.25, 0.62 * sc)          # omlijning schaalt mee met de figuur

    def v(soort, ax, ay, aw, ah, deel, **kw):
        return vorm(s, soort, x + ax * sc, y + ay * sc, aw * sc, ah * sc,
                    naam='!!%s_%s' % (sl, deel), **kw)

    huid_d = meng_kl(wie['huid'], 0.72)
    romp_d = meng_kl(wie['romp'], 0.74)

    # ---- schaduw op de grond, zodat de figuur niet zweeft
    v(MSO_SHAPE.OVAL, 22, 122, 56, 13, 'schaduw', vul=meng_kl('grond2', 0.7),
      alpha=55)

    # ---- haar achter het hoofd
    if wie['vlecht']:
        v(MSO_SHAPE.OVAL, 22, 2, 56, 48, 'haarmassa', vul=wie['haar'], omlijn=lw)
        for kant, ax in (('L', 15), ('R', 70)):
            v(MSO_SHAPE.OVAL, ax, 14, 16, 32, 'vlecht' + kant, vul=wie['haar'],
              omlijn=lw)
            v(MSO_SHAPE.OVAL, ax + 2, 42, 12, 7, 'strik' + kant, vul='oranje',
              omlijn=lw)
    else:
        v(MSO_SHAPE.OVAL, 26, 2, 48, 42, 'haarmassa', vul=wie['haar'], omlijn=lw)

    # ---- armen, met een hand aan het uiteinde dat meedraait
    for kant, ax, hoek in (('L', 19, arm[0]), ('R', 72, arm[1])):
        v(MSO_SHAPE.ROUNDED_RECTANGLE, ax, 48, 9, 33, 'arm' + kant,
          vul=wie['romp'], rot=hoek, rond=0.5, omlijn=lw)
        hx, hy = _eind(ax + 4.5, 64.5, 16.5, hoek)
        v(MSO_SHAPE.OVAL, hx - 5.5, hy - 5.5, 11, 11, 'hand' + kant,
          vul=wie['huid'], omlijn=lw)

    # ---- benen, met de schoen aan het uiteinde
    for kant, ax, hoek in (('L', 34, been[0]), ('R', 54, been[1])):
        v(MSO_SHAPE.ROUNDED_RECTANGLE, ax, 82, 12, 34, 'been' + kant,
          vul=wie['broek'], rot=hoek, rond=0.4, omlijn=lw)
        sx, sy = _eind(ax + 6, 99, 17, hoek)
        # smaller dan de eerste versie: op 24 breed liepen de twee schoenen
        # in elkaar over tot één blok
        v(MSO_SHAPE.ROUNDED_RECTANGLE, sx - 9.5, sy - 4, 19, 13,
          'schoen' + kant, vul=wie['schoen'], rot=hoek, rond=0.45, omlijn=lw)
        v(MSO_SHAPE.ROUNDED_RECTANGLE, sx - 9.5, sy + 4, 19, 6,
          'zool' + kant, vul=meng_kl(wie['schoen'], 0.66), rot=hoek, rond=0.5)

    # ---- romp, met kraag of zak
    v(MSO_SHAPE.ROUNDED_RECTANGLE, 27, 44, 46, 44, 'romp', vul=wie['romp'],
      rond=0.28, omlijn=lw)
    if wie['kraag']:
        v(MSO_SHAPE.TRAPEZOID, 41, 43, 18, 9, 'kraag', vul=lichter(wie['romp'], .5))
        v(MSO_SHAPE.RECTANGLE, 49, 50, 2, 34, 'rand', vul=romp_d)
    if wie['zak']:
        v(MSO_SHAPE.ROUNDED_RECTANGLE, 36, 66, 28, 15, 'zak', vul=romp_d,
          rond=0.4)
        v(MSO_SHAPE.ROUNDED_RECTANGLE, 44, 44, 12, 10, 'koord', vul=romp_d,
          rond=0.5)
    v(MSO_SHAPE.RECTANGLE, 43, 38, 14, 10, 'nek', vul=huid_d)

    # ---- hoofd en gezicht
    v(MSO_SHAPE.OVAL, 27, 4, 46, 44, 'hoofd', vul=wie['huid'], omlijn=lw)
    for kant, ax in (('L', 23), ('R', 71)):
        v(MSO_SHAPE.OVAL, ax, 22, 8, 11, 'oor' + kant, vul=wie['huid'],
          omlijn=lw)
    # het haar valt over het voorhoofd
    v(MSO_SHAPE.ARC if False else MSO_SHAPE.ROUND_2_SAME_RECTANGLE,
      28, 2, 44, 17, 'pony', vul=wie['haar'], omlijn=lw, rond=0.45)
    # kleinere ogen dan de eerste versie: op elf bij twaalf puilden ze uit
    for kant, ax in (('L', 36), ('R', 55)):
        v(MSO_SHAPE.OVAL, ax, 23, 9, 10, 'oogwit' + kant, vul='FFFFFF',
          omlijn=lw * 0.7)
        v(MSO_SHAPE.OVAL, ax + 2.4, 25.6, 4.6, 4.8, 'pupil' + kant, vul='1A2430')
        v(MSO_SHAPE.OVAL, ax + 3.6, 26.3, 1.6, 1.6, 'glans' + kant, vul='FFFFFF')
        v(MSO_SHAPE.ROUNDED_RECTANGLE, ax - 0.5, 18.5, 11, 3, 'wenk' + kant,
          vul=meng_kl(wie['haar'], 0.78), rond=0.5)
    v(MSO_SHAPE.OVAL, 46.5, 30, 7, 6.5, 'neus', vul=huid_d)
    for kant, ax in (('L', 29), ('R', 63)):
        v(MSO_SHAPE.OVAL, ax, 31, 9, 6, 'blos' + kant, vul='E8735E', alpha=45)
    if wie['bril']:
        for kant, ax in (('L', 33), ('R', 52)):
            v(MSO_SHAPE.OVAL, ax, 21, 15, 14, 'bril' + kant, lijn='394A5A',
              dik=lw * 1.3)
        v(MSO_SHAPE.RECTANGLE, 48, 27, 4, 2.2, 'brug', vul='394A5A')
    # mond hoger: op negenendertig zat hij op de kin in plaats van in het gezicht
    my = 35 if wie['snor'] else 36
    if wie['snor']:
        v(MSO_SHAPE.ROUNDED_RECTANGLE, 41, my, 18, 5, 'snor', vul=wie['haar'],
          rond=0.5, omlijn=lw * 0.6)
        my += 6
    # Eén vaste mond maakt van elke scène dezelfde blik. Een lach is dezelfde
    # ovaal met de bovenhelft weggedekt in huidskleur; dat leest als een
    # glimlach en houdt de vormen aan elkaar gelijk voor de morph.
    v(MSO_SHAPE.OVAL, 44.5, my, 11, 8.5, 'mond', vul='7A2E2E', omlijn=lw * 0.6)
    v(MSO_SHAPE.OVAL, 46.5, my + 0.8, 7, 3, 'tand', vul='FFFFFF')
    v(MSO_SHAPE.RECTANGLE, 43.5, my - 1, 13,
      5.2 if mond == 'lach' else 0.1, 'monddek', vul=wie['huid'])


# De voet komt uit hetzelfde profiel als de drukmat: honderdtwintig smalle
# banden tussen de mediale en de laterale rand. Een stapel losse ovalen — hiel,
# middenvoet, voorvoet, tenen — blijft een stapel ovalen; dit is een voet.
def zoolvorm(s, x, y, w, h, kl, sleutel, banden=110, marge=12):
    for r in range(banden):
        t = (r + 0.5) / banden
        li, la = beeld._rand(t)
        vorm(s, MSO_SHAPE.ROUNDED_RECTANGLE, x + li * w - marge,
             y + h - (r + 1) * h / banden, (la - li) * w + 2 * marge,
             h / banden + 2, vul=kl, naam='!!%s%03d' % (sleutel, r), rond=0.5)


def blokje(s, x, y, w, sleutel):
    """Legoblokje met noppen. Een oranje rechthoekje van vijftig eenheden zag
    niemand liggen; dit is groot, herkenbaar en het ligt in de weg."""
    h = w * 0.62
    vorm(s, MSO_SHAPE.BEVEL, x, y + h * 0.34, w, h * 0.66, vul='oranje',
         naam='!!%s_body' % sleutel, omlijn=2.2)
    for i in range(4):
        vorm(s, MSO_SHAPE.CAN, x + w * (0.05 + i * 0.235), y,
             w * 0.185, h * 0.46, vul=lichter('oranje', .12),
             naam='!!%s_nop%d' % (sleutel, i), omlijn=2)


def flits(s, cx, cy, r, sleutel):
    """Pijnster. Zonder dit gebeurt er zichtbaar niets op het moment zelf."""
    vorm(s, MSO_SHAPE.EXPLOSION1, cx - r, cy - r, 2 * r, 2 * r, vul='oranje',
         naam='!!%s_a' % sleutel)
    vorm(s, MSO_SHAPE.EXPLOSION1, cx - r * .62, cy - r * .62, r * 1.24,
         r * 1.24, vul='FFD24A', naam='!!%s_b' % sleutel)


def voetafdruk(s, x, y, w, h, sleutel, heet=True):
    """Een achtergelaten stap, in de vorm van een voet met zijn drukpunt."""
    zoolvorm(s, x, y, w, h, 'licht', sleutel, banden=26, marge=3)
    if heet:
        vorm(s, MSO_SHAPE.OVAL, x + 0.44 * w - w * .17, y + h - 0.66 * h - w * .17,
             w * .34, w * .34, vul='oranje', naam='!!%s_haard' % sleutel)


def grote_voet(s, x, y, w, h, kl='rand'):
    """Voetzool in het groot. Meer banden dan de zool: op deze schaal wordt
    de rand anders schilferig. Zonder lichtere voetboog — die werd een streep
    dwars over de voet in plaats van een welving."""
    zoolvorm(s, x, y, w, h, kl, 'voet', banden=200, marge=10)


def grondlijn(s, hoogte=880):
    """Grasveld met een lichtere rand aan de horizon en wat plukjes."""
    vorm(s, MSO_SHAPE.RECTANGLE, 0, hoogte, B, H - hoogte, vul='grond2',
         naam='!!gras')
    vorm(s, MSO_SHAPE.RECTANGLE, 0, hoogte, B, 5, vul=lichter('grond2', .3),
         naam='!!horizon')
    # onregelmatig verdeeld: een strakke rij plukjes leest als een patroon,
    # niet als gras. De verschuiving is vast, dus de morph laat ze staan.
    for i in range(13):
        px_ = 60 + i * 150 + (i * 53 % 61)
        hh = 24 + (i * 37 % 13)
        vorm(s, MSO_SHAPE.ISOSCELES_TRIANGLE, px_, hoogte + 42 - hh, 18, hh,
             vul=lichter('grond2', .3), naam='!!pluk%d' % i)
        vorm(s, MSO_SHAPE.ISOSCELES_TRIANGLE, px_ + 14, hoogte + 44 - hh * .74,
             14, hh * .74, vul=lichter('grond2', .2), naam='!!pluk%db' % i)


BOMEN = ((180, 1.0), (1620, 1.25), (1180, 0.75))


def boom(s, i, bx, bs, hoogte):
    """Stam met drie overlappende kruinen: een bol op een stok is geen boom."""
    vorm(s, MSO_SHAPE.TRAPEZOID, bx - 12 * bs, hoogte - 175 * bs, 50 * bs,
         175 * bs, vul='rand', naam='!!stam%d' % i, omlijn=1.5)
    for k, (dx, dy, dd, kl) in enumerate((
            (-86, -286, 150, meng_kl('tegel2', 0.82)),
            (-16, -320, 132, 'tegel2'),
            (-52, -240, 128, lichter('tegel2', .12)))):
        vorm(s, MSO_SHAPE.OVAL, bx + dx * bs, hoogte + dy * bs, dd * bs,
             dd * bs, vul=kl, naam='!!kruin%d_%d' % (i, k), omlijn=1.5)


def wolk(s, i, x, y, sc):
    for k, (dx, dy, dd) in enumerate(((0, 10, 46), (30, 0, 62), (74, 14, 42))):
        vorm(s, MSO_SHAPE.OVAL, x + dx * sc, y + dy * sc, dd * sc, dd * sc,
             vul=lichter('bg', .16), naam='!!wolk%d_%d' % (i, k))


def park(s, hoogte=880, bomen=BOMEN, wolken=((240, 150, 1.5), (1420, 210, 1.1))):
    """Rustige achtergrond: lucht met wolken, een horizon en een paar bomen."""
    for i, (wx, wy, ws) in enumerate(wolken):
        wolk(s, i, wx, wy, ws)
    grondlijn(s, hoogte)
    for i, (bx, bs) in enumerate(bomen):
        boom(s, i, bx, bs, hoogte)


def onderschrift(s, tekst, kl='ink'):
    # Een balk onder de tekst: op een projector of een scherm in een hal valt
    # witte tekst anders weg tegen een licht stuk beeld.
    b = vorm(s, MSO_SHAPE.RECTANGLE, 0, 930, B, 150, vul=meng_kl('bg', 0.55),
             naam='!!balk')
    verloop(b, meng_kl('bg', 0.55), meng_kl('bg', 0.35), 5400000)
    # 30 punt vet past op één regel over de volle breedte; op 40 sloeg het om
    # en viel de tweede regel van de dia
    txt(s, 120, 962, 1680, 84, tekst, gr=30, kl=kl, vet=True,
        uit=PP_ALIGN.CENTER, naam='!!onderschrift')


def soepel(t):
    """Versnellen en weer afremmen. Lineair bewegen ziet er mechanisch uit;
    alles wat leeft komt op gang en loopt uit."""
    return t * t * (3 - 2 * t)


def reeks(n):
    """n tussenstanden van 0 tot 1, met een zachte in- en uitloop."""
    return [soepel(i / float(n - 1)) for i in range(n)] if n > 1 else [1.0]


def meng(a, b, f):
    """Tussenstand tussen twee reeksen drukhaarden."""
    uit = []
    for ha, hb in zip(a, b):
        uit.append(tuple(x + (y - x) * f for x, y in zip(ha, hb)))
    return uit


GROND = 880
SC_F, SC_L = 3.3, 2.6
Y_F, Y_L = GROND - 124 * SC_F, GROND - 124 * SC_L

# ============================================================ 1 — in het park
# Acht beelden in plaats van twee, elk met een korte overgang en geen
# stilstand: dan lopen ze echt in plaats van twee keer te verspringen.
PARK_N = 8
for j, t in enumerate(reeks(PARK_N)):
    laatste = (j == PARK_N - 1)
    s = dia(1.8 if laatste else 0, 420 if j else 250, eerste=(j == 0))
    park(s)
    # de passen wisselen af, de figuren schuiven naar rechts
    hoek = 15 * math.sin(j * math.pi / 2.0)
    figuur(s, FRANS, 'f', 240 + t * 210, Y_F, SC_F, been=(-hoek, hoek),
           arm=(hoek * .6, -hoek * .6))
    figuur(s, LOTTE, 'l', 640 + t * 230, Y_L, SC_L, been=(hoek, -hoek),
           arm=(-hoek * .6, hoek * .6))
    # 72 punt, niet 82: op 82 sloeg de tweede regel om en kwam de derde
    # regel op het hoofd van Frans terecht
    txt(s, 120, 96, 1100, 400, 'Opa Frans\nen Lotte', gr=72, kl='ink',
        vet=True, ra=1.05, naam='!!kop')
    onderschrift(s, 'Elke zondag samen op stap. Tienduizend stappen.')

# ======================================================= 2 — het legoblokje
# Drie momenten in plaats van twee. In de vorige versie stond het onderschrift
# 'Lotte voelt het meteen' terwijl er nog niets gebeurd was, en het blokje was
# een oranje veegje onder haar voeten. Nu zie je eerst dat er iets ligt, dan
# dat zij erop stapt, en pas daarna dat opa er niets van merkt.
BLOK_B = 104                      # breedte van een blokje
BLOK_H = BLOK_B * 0.62            # en dus zijn hoogte
BLOK_L, BLOK_F = 560, 1352      # zijn blokje ligt náást zijn voeten, niet
FRANS_X = (1180, 1180, 1236)    # erachter, en hij stapt er pas op het eind op
# Elk moment krijgt een aanloop: Lotte loopt naar het blokje toe, springt op,
# komt neer. Drie harde standen lieten de kijker de beweging zelf invullen.
LEGO = []
for t in reeks(4):                                   # naar het blokje toe
    LEGO.append((0, 320 + t * 128, 0, 0, FRANS_X[0], 0))
for t in reeks(4):                                   # opspringen
    LEGO.append((1, 448, t * 78, t * 40, FRANS_X[0], 0))
LEGO.append((1, 448, 78, 40, FRANS_X[0], 0))         # even in de lucht blijven
for t in reeks(4):                                   # opa stapt op het zijne
    LEGO.append((2, 448 - t * 148, (1 - t) * 40, 0,
                 FRANS_X[0] + t * (FRANS_X[2] - FRANS_X[0]), t * BLOK_H))

for j, (fase, lx, hop, beenhoek, fx, frans_op) in enumerate(LEGO):
    # alleen op de laatste van elk blok even stil, zodat het onderschrift leest
    vast = j in (3, 8, len(LEGO) - 1)
    s = dia(1.9 if vast else 0, 340)
    grondlijn(s)
    # de blokjes liggen óp de grond, niet erin, zodat iemand er bovenop kan
    for i, bx in ((0, BLOK_L), (1, BLOK_F)):
        blokje(s, bx, GROND - BLOK_H, BLOK_B, 'blok%d' % i)
    figuur(s, LOTTE, 'l', lx, Y_L - hop, SC_L, been=(0, -beenhoek),
           arm=(-beenhoek * .65, beenhoek * .65),
           mond='open' if beenhoek > 8 else 'lach')
    figuur(s, FRANS, 'f', fx, Y_F - frans_op, SC_F, been=(0, 0), arm=(0, 0))
    if fase == 1 and beenhoek > 8:
        # naast haar voet, niet erover: anders verdwijnt het blokje eronder
        flits(s, BLOK_L - 46, GROND - 96, 26 + beenhoek * 1.7, 'pijn')
        txt(s, 300, 214, 340, 140, 'AU!', gr=60 + beenhoek * 0.8, kl='oranje',
            vet=True, uit=PP_ALIGN.CENTER, naam='!!au')
    if fase == 2 and frans_op > BLOK_H * 0.5:
        vorm(s, MSO_SHAPE.OVAL, BLOK_F - 40, GROND - BLOK_H - 62, 184, 184,
             lijn='groen2', dik=4, naam='!!kring')
    onderschrift(s, ('Er ligt een legoblokje op de grond.',
                     'Lotte stapt erop — en voelt het meteen.',
                     'Opa Frans staat op net zo’n blokje. Hij merkt niets.')[fase])

# ===================================================== 3 — de hete plek
# Hier zat het gat in het verhaal: de film liet zien dat opa niets voelt, maar
# nergens waaróm dat gevaarlijk is. Dat staat er nu bij.
# De haard gebruikt de kleurenband van de drukmat: geel, oranje, rood.
# Doorschijnend oranje over het blauw van de voet gaf een modderig bruin.
VX, VY, VW, VH = 1080, 150, 380, 720
# de haard klopt: drie keer aanzwellen en teruglopen, doorlopend
HAARD = []
for k, regel in enumerate((
        'Op één plekje. Als een steentje dat er altijd zit.',
        'Dat voelt hij niet.',
        'En net daar kan een wonde ontstaan.')):
    for t in reeks(5):
        HAARD.append((0.45 + 0.55 * math.sin(t * math.pi), regel, False))
    HAARD.append((0.45, regel, True))

for j, (groei, regel, vast) in enumerate(HAARD):
    s = dia(1.5 if vast else 0, 300)
    txt(s, 120, 200, 800, 320, 'Toch duwt\nzijn voet\nte hard', gr=72,
        kl='ink', vet=True, ra=1.12, naam='!!kop')
    grote_voet(s, VX, VY, VW, VH)
    # precies waar de drukmat zijn piek heeft: onder de bal van de voet
    hx, hy = VX + 0.44 * VW, VY + VH - 0.66 * VH
    for i, (kl, deel) in enumerate((('FFD24A', 1.0), ('FF7A00', 0.62),
                                    ('E8331E', 0.30))):
        r = (56 + 26 * groei) * deel
        vorm(s, MSO_SHAPE.OVAL, hx - r, hy - r, 2 * r, 2 * r, vul=kl,
             naam='!!haard%d' % i)
    onderschrift(s, regel)

# ======================================================= 4 — de meetzool
# De zool krijgt de vorm van een voet, opgebouwd uit dunne banden volgens
# hetzelfde profiel als de drukmat. Een afgeronde rechthoek leest niet als een
# zool; dit wel, en de negenennegentig sensoren staan erin waar ze horen.
ZX, ZY, ZW, ZH = 400, 216, 330, 620
CELLEN = []
for r in range(17):
    t = (r + 0.5) / 17
    li, la = beeld._rand(t)
    for c in range(9):
        fx = (c + 0.5) / 9
        if li <= fx <= la:
            CELLEN.append((ZX + fx * ZW, ZY + ZH - t * ZH))
CELLEN = CELLEN[:99]

ZOOL_N = 7
for j, t in enumerate(reeks(ZOOL_N)):
    vast = j in (0, ZOOL_N - 1)
    s = dia(2.2 if vast else 0, 340)
    # 'meetzool', niet zomaar 'zool': verderop komt de zool op maat, en dat
    # zijn twee verschillende dingen. De ene meet, de andere haalt druk weg.
    txt(s, 1060, 250, 780, 420, 'Een meetzool\nmet 99\nsensoren', gr=54,
        kl='ink', vet=True, ra=1.14, naam='!!kop')
    # De schoen van bovenaf, in dezelfde voetvorm, met een donkere holte erin.
    # Zonder schoen bleef het een zwevend plaatje en klopte 'ze gaat in zijn
    # eigen schoen' nergens mee.
    zoolvorm(s, ZX - 44, ZY - 40, ZW + 88, ZH + 80, 'tegel2', 'schoen',
             banden=130, marge=16)
    zoolvorm(s, ZX - 20, ZY - 18, ZW + 40, ZH + 36, 'bg', 'holte',
             banden=130, marge=12)
    # De meetzool zweeft er eerst boven en zakt er dan in. Naast de schoen
    # schuiven werkte niet: dan liep ze dwars over de titel.
    dy = -196 * (1 - t)
    zoolvorm(s, ZX, ZY + dy, ZW, ZH, 'rand', 'band', banden=130, marge=12)
    for i, (cx, cy) in enumerate(CELLEN):
        vorm(s, MSO_SHAPE.OVAL, cx - 10, cy + dy - 10, 20, 20,
             vul=meng_kl('licht', 0.55 + 0.45 * t), naam='!!cel%02d' % i)
    onderschrift(s, 'Flinterdun, en ze gaat in zijn eigen schoen.' if t < 0.9
                 else 'Zo meten we hoe hard zijn voet duwt.')

# ==================================================== 5 — tien meter wandelen
WANDEL_N = 11
for j, t in enumerate(reeks(WANDEL_N)):
    vast = j == WANDEL_N - 1
    s = dia(1.8 if vast else 0, 320)
    # een gemarkeerd looppad met begin en eind: anders is '10 meter' een getal
    # zonder beeld, en waren de stappen naamloze ovaaltjes
    vorm(s, MSO_SHAPE.RECTANGLE, 120, GROND, 1680, 14, vul='rand', naam='!!pad')
    for i, (mx, lbl) in enumerate(((120, '0 m'), (1800, '10 m'))):
        vorm(s, MSO_SHAPE.RECTANGLE, mx - 4, GROND - 34, 8, 48, vul='licht',
             naam='!!merk%d' % i)
        txt(s, mx - 70, GROND - 98, 140, 44, lbl, gr=24, kl='licht', vet=True,
            font=FONT_M, uit=PP_ALIGN.CENTER, naam='!!merklabel%d' % i)
    fx = 200 + t * 1120
    hoek = 16 * math.sin(j * math.pi / 2.0)
    figuur(s, FRANS, 'f', fx, Y_F, SC_F, been=(-hoek, hoek),
           arm=(hoek * .75, -hoek * .75))
    # het kastje aan zijn riem, met de kabel naar de zool in zijn schoen
    vorm(s, MSO_SHAPE.RECTANGLE, fx + 72 * SC_F, Y_F + 92 * SC_F, 3,
         30 * SC_F, vul='gedempt', naam='!!kabel')
    vorm(s, MSO_SHAPE.ROUNDED_RECTANGLE, fx + 62 * SC_F, Y_F + 74 * SC_F,
         26 * SC_F, 20 * SC_F, vul='tegel2', naam='!!kastje', omlijn=2,
         rond=0.3)
    vorm(s, MSO_SHAPE.OVAL, fx + 71 * SC_F, Y_F + 80 * SC_F, 8 * SC_F,
         8 * SC_F, vul='groen2', naam='!!lampje')
    # de stappen die al gezet zijn blijven staan, elk met zijn eigen drukpunt
    for i in range(6):
        if 250 + i * 240 < fx + 40:
            voetafdruk(s, 250 + i * 240, 898, 40, 58, 'stap%d' % i)
    # hoger en kleiner dan de andere koppen: Frans loopt er anders doorheen
    txt(s, 120, 84, 900, 380, '10 meter\nwandelen', gr=66, kl='ink', vet=True,
        ra=1.1, naam='!!kop')
    onderschrift(s, 'Honderd metingen per seconde, bij elke stap.')

# ================================================= 6 — de eerste meting
def matdia(f, waarde, kop, regel, stand, morph=900):
    s = dia(stand, morph)
    beeld.drukmat(s, 210, 130, 420, 800, meng(beeld.VOOR, beeld.NA, f),
                  sleutel='m', piek=float(waarde))
    txt(s, 760, 168, 700, 420, str(waarde), gr=190,
        kl='oranje' if f < 0.6 else 'licht', vet=True, ra=0.9, naam='!!getal')
    txt(s, 1420, 250, 300, 120, 'kPa', gr=60, kl='gedempt', naam='!!eenheid')
    # 56 punt op 560: op 64 liep de tweede regel achter de onderschriftbalk
    txt(s, 760, 560, 960, 300, kop, gr=56, kl='ink', vet=True, ra=1.1,
        naam='!!kop')
    onderschrift(s, regel)


matdia(0.0, 312, 'Rood is waar\nhet duwt', 'Alles boven 200 is te veel.', 2.8)
matdia(0.0, 312, 'Rood is waar\nhet duwt',
       'Precies het plekje dat opa niet voelt.', 2.4)

# ============================================== 7 — de zool op maat
# De ontbrekende schakel. Zonder deze scène daalt de druk in de film zomaar,
# van driehonderdtwaalf naar honderdzesentachtig, zonder dat iemand iets doet.
LAGEN = (('mid', 'kurk'), ('licht', 'schuim'), ('gedempt', 'deklaag'))
LX, LY, LW, LH = 250, 250, 340, 500
LAAG_N = 7
for j, t in enumerate(reeks(LAAG_N)):
    vast = j in (0, LAAG_N - 1)
    s = dia(2.4 if vast else 0, 360)
    txt(s, 1120, 250, 720, 400, 'Een zool\nop maat', gr=76, kl='ink',
        vet=True, ra=1.1, naam='!!kop')
    for i, (kl, naam_) in enumerate(LAGEN):
        # De lagen schuiven van uit elkaar naar op elkaar, maar nooit precies:
        # precies op elkaar zag je alleen de bovenste laag en was van
        # 'opgebouwd uit lagen' niets meer te merken.
        lx = LX + (i - 1) * (72 - t * 56) + t * i * 16
        ly = LY + (i - 1) * (132 - t * 98) + t * i * 34
        zoolvorm(s, lx, ly, LW, LH, kl, 'laag%d_' % i, banden=80, marge=9)
        # Gestapeld vielen de labels over elkaar. Ze schuiven mee naar een
        # eigen kolom, met een kleurstaal zodat je ziet wat bij wat hoort.
        ex = (lx + LW + 30) * (1 - t) + (LX + LW + 150) * t
        ey = (ly + 22) * (1 - t) + (LY + 40 + i * 88) * t
        vorm(s, MSO_SHAPE.ROUNDED_RECTANGLE, ex, ey + 8, 34, 34, vul=kl,
             naam='!!laagstaal%d' % i, rond=0.3, omlijn=2)
        txt(s, ex + 50, ey + 8, 300, 60, naam_, gr=26, kl='gedempt',
            naam='!!laagnaam%d' % i)
    # het kussentje dat de druk van de bal van de voet weghaalt
    tl = 2  # het ligt op de bovenste laag
    px_ = LX + (tl - 1) * (72 - t * 56) + t * tl * 16 + 0.28 * LW
    py = LY + (tl - 1) * (132 - t * 98) + t * tl * 34 + LH - 0.68 * LH
    vorm(s, MSO_SHAPE.OVAL, px_, py, 78 + t * 32, 52 + t * 22,
         vul='oranje', naam='!!pad', omlijn=2.4)
    onderschrift(s, 'De schoenmaker bouwt hem op uit lagen.' if t < 0.9
                 else 'Het kussentje haalt de druk weg van dat ene plekje.')

# ============================================ 8 — meten met de nieuwe zool
# Twaalf tussenstanden in plaats van vier: de plek koelt nu echt af en het
# cijfer telt zichtbaar terug, in plaats van in sprongen te verspringen.
matdia(0.0, 312, 'Zelfde voet,\nnieuwe zool', 'We meten opnieuw.', 1.8)
KOEL_N = 12
for j, t in enumerate(reeks(KOEL_N)):
    laatste = j == KOEL_N - 1
    matdia(t, int(round(312 - t * 126)),
           'En kijk:\nhet rood koelt af' if not laatste
           else 'En kijk:\nhet rood is weg',
           'De druk verdeelt zich over de hele voet.', 3.6 if laatste else 0,
           300)

# ============================================================== 7 — het slot
s = dia(5.5, 700)
# de boom links weggelaten: daar staat nu de tekst
park(s, bomen=((1620, 1.25), (1120, 0.75)))
figuur(s, FRANS, 'f', 1180, Y_F, SC_F, been=(-10, 10), arm=(8, -8))
figuur(s, LOTTE, 'l', 1560, Y_L, SC_L, been=(10, -10), arm=(-8, 8))
# Gemeten aan de afdruk: op dertig punt passen er maar drie-en-dertig tekens
# in negenhonderd eenheden. Vandaar korte regels en een kleiner korps — anders
# slaat elke regel om en schuift alles over elkaar.
# 'Werkt dat echt?' klonk alsof we net niet hadden laten zien dat het werkt.
# Wat we tonen is dat de druk daalt; of dat ook wonden voorkomt, is de vraag
# die de studie moet beantwoorden. Dat verschil staat er nu.
# twee regels van vijftig punt in plaats van drie van tweeënzestig: die derde
# regel viel over de tekst eronder
txt(s, 120, 130, 1060, 320, 'Maar voorkomt dat\nook echt een wonde?', gr=50,
    kl='ink', vet=True, ra=1.1, naam='!!kop')
txt(s, 124, 470, 980, 270,
    'Zes Belgische ziekenhuizen\nzoeken het nu samen uit,\nook AZ Groeninge in Kortrijk.',
    gr=26, kl='gedempt', ra=1.35)
for i in range(6):
    vorm(s, MSO_SHAPE.OVAL, 128 + i * 62, 762, 42, 42, vul='groen2',
         naam='!!ziek%d' % i)
txt(s, 124, 832, 900, 50, 'PARADISE  ·  KU Leuven Campus Brugge', gr=19,
    kl='licht', font=FONT_M, sp=1.4)
onderschrift(s, 'Dat is wat PARADISE de komende jaren uitzoekt.')

prs.save(DOEL)
# TIJDEN telt per dia de overgang én de standtijd, dus de som is de speelduur
print('%d dia\'s · %d:%02d · %.0f KB · %s'
      % (len(TIJDEN), int(sum(TIJDEN)) // 60, int(sum(TIJDEN)) % 60,
         os.path.getsize(DOEL) / 1024, os.path.basename(DOEL)))

# ------------------------------------------------------------------- renderen
# Via PowerShell in plaats van pywin32: dat laatste staat hier niet, en
# PowerShell praat even goed met PowerPoint zonder dat er iets bij moet.
if '--video' in sys.argv:
    import subprocess
    mp4 = DOEL.replace('.pptx', '.mp4')
    if os.path.exists(mp4):
        os.remove(mp4)
    print('renderen — dit duurt enkele minuten')
    ps = (
        "$pp = New-Object -ComObject PowerPoint.Application; "
        "$pr = $pp.Presentations.Open('%s', $true, $false, $false); "
        # bestand, tijden gebruiken, standaardduur, 1080 lijnen, 60 b/s, kwaliteit
        "$pr.CreateVideo('%s', $true, 3, 1080, 60, 100); "
        # 1 = bezig, 2 = in de wachtrij, 3 = klaar, 4 = mislukt. Alleen op 1
        # wachten stopt te vroeg: de taak staat eerst even in de wachtrij.
        "$n = 0; "
        "while (($pr.CreateVideoStatus -eq 1 -or $pr.CreateVideoStatus -eq 2) "
        "-and $n -lt 400) { Start-Sleep -Seconds 3; $n++ }; "
        "$st = $pr.CreateVideoStatus; "
        "try { $pr.Close() } catch {}; try { $pp.Quit() } catch {}; "
        "if ($st -ne 3) { Write-Output ('renderen mislukt, status ' + $st) }"
        % (DOEL.replace("'", "''"), mp4.replace("'", "''")))
    subprocess.run(['powershell', '-NoProfile', '-Command', ps])
    if os.path.exists(mp4):
        print('%s · %.1f MB' % (os.path.basename(mp4),
                                os.path.getsize(mp4) / 1024 / 1024))
    else:
        print('Geen mp4 gemaakt. Staat het deck nog open in PowerPoint?')
