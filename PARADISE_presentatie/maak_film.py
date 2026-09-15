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


prs = Presentation()
prs.slide_width, prs.slide_height = px(B), px(H)
LEEG = prs.slide_layouts[6]
TIJDEN = []


def dia(seconden, eerste=False):
    """Nieuwe dia met grond, morph-overgang en een eigen standtijd."""
    s = prs.slides.add_slide(LEEG)
    g = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, px(B), px(H))
    g.fill.solid(); g.fill.fore_color.rgb = rgb('bg')
    g.line.fill.background(); g.shadow.inherit = False
    g.name = '!!grond'
    ms = int(seconden * 1000)
    duur = 250 if eerste else 900
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
    TIJDEN.append(seconden)
    return s


def vorm(s, soort, x, y, w, h, vul=None, lijn=None, dik=2.5, rot=0,
         naam=None, alpha=None, rond=None):
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
             schoen='gedempt', bril=True, snor=True, vlecht=False)
LOTTE = dict(haar='8A5A3B', huid='F7D6B4', romp='groen', broek='navy',
             schoen='oranje', bril=False, snor=False, vlecht=True)


def figuur(s, wie, sl, x, y, sc=1.0, been=(0, 0), arm=(0, 0), spiegel=False):
    """Tekent een personage; `been` en `arm` zijn hoeken in graden."""
    def v(soort, ax, ay, aw, ah, deel, **kw):
        bx = (100 - ax - aw) if spiegel else ax
        return vorm(s, soort, x + bx * sc, y + ay * sc, aw * sc, ah * sc,
                    naam='!!%s_%s' % (sl, deel), **kw)

    if wie['vlecht']:
        v(MSO_SHAPE.OVAL, 16, 14, 15, 36, 'vlechtL', vul=wie['haar'])
        v(MSO_SHAPE.OVAL, 69, 14, 15, 36, 'vlechtR', vul=wie['haar'])
    v(MSO_SHAPE.ROUNDED_RECTANGLE, 20, 46, 9, 34, 'armL', vul=wie['romp'],
      rot=arm[0], rond=0.5)
    v(MSO_SHAPE.ROUNDED_RECTANGLE, 71, 46, 9, 34, 'armR', vul=wie['romp'],
      rot=arm[1], rond=0.5)
    v(MSO_SHAPE.ROUNDED_RECTANGLE, 34, 84, 12, 32, 'beenL', vul=wie['broek'],
      rot=been[0], rond=0.45)
    v(MSO_SHAPE.ROUNDED_RECTANGLE, 54, 84, 12, 32, 'beenR', vul=wie['broek'],
      rot=been[1], rond=0.45)
    v(MSO_SHAPE.OVAL, 28, 112, 22, 12, 'schoenL', vul=wie['schoen'])
    v(MSO_SHAPE.OVAL, 50, 112, 22, 12, 'schoenR', vul=wie['schoen'])
    v(MSO_SHAPE.ROUNDED_RECTANGLE, 28, 44, 44, 42, 'romp', vul=wie['romp'],
      rond=0.25)
    v(MSO_SHAPE.OVAL, 30, 4, 40, 40, 'hoofd', vul=wie['huid'])
    v(MSO_SHAPE.OVAL, 27, 0, 46, 22, 'haar', vul=wie['haar'])
    if wie['bril']:
        v(MSO_SHAPE.OVAL, 33, 16, 13, 13, 'brilL', lijn='bg', dik=2)
        v(MSO_SHAPE.OVAL, 54, 16, 13, 13, 'brilR', lijn='bg', dik=2)
    else:
        v(MSO_SHAPE.OVAL, 37, 18, 8, 8, 'oogL', vul='bg')
        v(MSO_SHAPE.OVAL, 55, 18, 8, 8, 'oogR', vul='bg')
    if wie['snor']:
        v(MSO_SHAPE.ROUNDED_RECTANGLE, 41, 31, 18, 5, 'snor', vul=wie['haar'],
          rond=0.5)
    else:
        v(MSO_SHAPE.OVAL, 43, 31, 14, 9, 'mond', vul='bg')


# De voet in het groot, met dezelfde vormen als het icoon in het deck: hiel,
# middenvoet, voorvoet en vijf tenen in één kleur, zodat ze samensmelten tot
# één silhouet. Drie losse ovalen doen dat niet en zien er niet uit als een voet.
VOETDELEN = ((30, 54, 42, 42), (32, 34, 38, 32), (20, 18, 62, 36))
TENEN = ((21, 2, 18), (42, 0, 14), (56, 2, 12.5), (68, 6, 11.5), (79, 11, 10.5))


def grote_voet(s, x, y, sc, kl='rand'):
    for i, (ax, ay, aw, ah) in enumerate(VOETDELEN):
        vorm(s, MSO_SHAPE.OVAL, x + ax * sc, y + ay * sc, aw * sc, ah * sc,
             vul=kl, naam='!!voetdeel%d' % i)
    for i, (ax, ay, ad) in enumerate(TENEN):
        vorm(s, MSO_SHAPE.OVAL, x + ax * sc, y + ay * sc, ad * sc, ad * sc,
             vul=kl, naam='!!teen%d' % i)


def grondlijn(s, hoogte=880):
    vorm(s, MSO_SHAPE.RECTANGLE, 0, hoogte, B, H - hoogte, vul='grond2',
         naam='!!gras')


BOMEN = ((180, 1.0), (1620, 1.25), (1180, 0.75))


def park(s, hoogte=880, bomen=BOMEN):
    """Rustige achtergrond: een horizon en een paar bomen."""
    grondlijn(s, hoogte)
    for i, (bx, bs) in enumerate(bomen):
        vorm(s, MSO_SHAPE.RECTANGLE, bx, hoogte - 150 * bs, 22 * bs, 150 * bs,
             vul='rand', naam='!!stam%d' % i)
        vorm(s, MSO_SHAPE.OVAL, bx - 74 * bs, hoogte - 300 * bs, 170 * bs,
             170 * bs, vul='tegel2', naam='!!kruin%d' % i)


def onderschrift(s, tekst, kl='ink'):
    # 30 punt vet past op één regel over de volle breedte; op 40 sloeg het om
    # en viel de tweede regel van de dia
    txt(s, 120, 962, 1680, 84, tekst, gr=30, kl=kl, vet=True,
        uit=PP_ALIGN.CENTER, naam='!!onderschrift')


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
for j, (fx, lx, been) in enumerate(
        ((240, 640, (-14, 14)), (400, 840, (13, -13)))):
    s = dia(3.4, eerste=(j == 0))
    park(s)
    figuur(s, FRANS, 'f', fx, Y_F, SC_F, been=been,
           arm=(been[1] // 2, been[0] // 2))
    figuur(s, LOTTE, 'l', lx, Y_L, SC_L, been=(been[1], been[0]),
           arm=(-been[0], -been[1]))
    txt(s, 120, 96, 1100, 230,
        'Opa Frans\nen Lotte' if j == 0 else 'Elke zondag\nsamen op stap',
        gr=82, kl='ink', vet=True, ra=1.05, naam='!!kop')
    onderschrift(s, 'Tienduizend stappen, zonder erbij na te denken.')

# ======================================================= 2 — het legoblokje
for j in range(2):
    s = dia(3.6)
    grondlijn(s)
    figuur(s, FRANS, 'f', 1180, Y_F, SC_F, been=(0, 0), arm=(0, 0))
    figuur(s, LOTTE, 'l', 460, Y_L - j * 90, SC_L,
           been=(0, -38 * j), arm=(-22 * j, 22 * j))
    # twee identieke blokjes op de grond, elk onder een voet
    for i, bx in enumerate((556, 1310)):
        vorm(s, MSO_SHAPE.ROUNDED_RECTANGLE, bx, 866, 52, 30, vul='oranje',
             naam='!!blok%d' % i, rond=0.2)
    if j:
        txt(s, 360, 226, 320, 130, 'AU!', gr=84, kl='oranje', vet=True,
            uit=PP_ALIGN.CENTER, naam='!!au')
    onderschrift(s, 'Lotte voelt het meteen.' if j == 0
                 else 'Opa Frans voelt niets.')

# ===================================================== 3 — de hete plek
# De haard is opgebouwd uit dezelfde kleurenband als de drukmat: geel, oranje,
# rood. Doorschijnend oranje over het blauw van de voet gaf een modderig bruin.
for j, groei in enumerate((0.55, 1.0, 0.75)):
    s = dia(2.4)
    txt(s, 120, 200, 760, 300, 'Toch duwt\nzijn voet\nte hard', gr=72,
        kl='ink', vet=True, ra=1.12, naam='!!kop')
    grote_voet(s, 1020, 150, 6.2)
    hx, hy = 1020 + 45 * 6.2, 150 + 30 * 6.2
    for i, (kl, deel) in enumerate((('FFD24A', 1.0), ('FF7A00', 0.62),
                                    ('E8331E', 0.30))):
        r = (52 + 26 * groei) * deel
        vorm(s, MSO_SHAPE.OVAL, hx - r, hy - r, 2 * r, 2 * r, vul=kl,
             naam='!!haard%d' % i)
    onderschrift(s, 'Op één plekje. Als een steentje dat er altijd zit.')

# ======================================================= 4 — de meetzool
# De zool krijgt de vorm van een voet, opgebouwd uit dunne banden volgens
# hetzelfde profiel als de drukmat. Een afgeronde rechthoek leest niet als een
# zool; dit wel, en de negenennegentig voelertjes staan erin waar ze horen.
ZX, ZY, ZW, ZH = 250, 140, 440, 800
CELLEN = []
for r in range(17):
    t = (r + 0.5) / 17
    li, la = beeld._rand(t)
    for c in range(9):
        fx = (c + 0.5) / 9
        if li <= fx <= la:
            CELLEN.append((ZX + fx * ZW, ZY + ZH - t * ZH))
CELLEN = CELLEN[:99]

for j in range(2):
    s = dia(3.4)
    txt(s, 1060, 236, 760, 400, 'Een zool\nmet 99\nvoelertjes', gr=68,
        kl='ink', vet=True, ra=1.12, naam='!!kop')
    for r in range(120):
        t = (r + 0.5) / 120
        li, la = beeld._rand(t)
        vorm(s, MSO_SHAPE.ROUNDED_RECTANGLE, ZX + li * ZW - 14,
             ZY + ZH - (r + 1) * ZH / 120, (la - li) * ZW + 28, ZH / 120 + 2,
             vul='tegel2', naam='!!band%03d' % r, rond=0.5)
    for i, (cx, cy) in enumerate(CELLEN):
        vorm(s, MSO_SHAPE.OVAL, cx - 13, cy - 13, 26, 26,
             vul='licht' if j else 'rand', naam='!!cel%02d' % i)
    onderschrift(s, 'Ze past gewoon in je eigen schoen.')

# ==================================================== 5 — tien meter wandelen
for j in range(3):
    s = dia(2.6)
    vorm(s, MSO_SHAPE.RECTANGLE, 0, GROND, B, 14, vul='rand', naam='!!pad')
    figuur(s, FRANS, 'f', 200 + j * 560, Y_F, SC_F,
           been=(-16, 16) if j % 2 == 0 else (15, -15),
           arm=(12, -12) if j % 2 == 0 else (-12, 12))
    # de stappen die al gezet zijn blijven staan
    for i in range(j * 2 + 1):
        vorm(s, MSO_SHAPE.OVAL, 262 + i * 280, 906, 70, 42,
             vul='oranje' if i % 2 else 'licht', naam='!!stap%d' % i)
    # hoger en kleiner dan de andere koppen: Frans loopt er anders doorheen
    txt(s, 120, 84, 900, 380, '10 meter\nwandelen', gr=66, kl='ink', vet=True,
        ra=1.1, naam='!!kop')
    onderschrift(s, 'Honderd metingen per seconde, bij elke stap.')

# ================================================= 6 — de drukmat koelt af
STAPPEN = [(0.0, 312), (0.0, 312), (0.45, 256), (0.8, 212), (1.0, 186), (1.0, 186)]
for j, (f, waarde) in enumerate(STAPPEN):
    s = dia(3.2 if j in (1, len(STAPPEN) - 1) else 2.0)
    beeld.drukmat(s, 210, 130, 420, 800, meng(beeld.VOOR, beeld.NA, f),
                  sleutel='m', piek=float(waarde))
    txt(s, 760, 168, 700, 420, str(waarde), gr=190, kl='oranje' if f < 0.6
        else 'licht', vet=True, ra=0.9, naam='!!getal')
    txt(s, 1420, 250, 300, 120, 'kPa', gr=60, kl='gedempt', naam='!!eenheid')
    txt(s, 760, 606, 960, 240,
        'Rood is waar\nhet duwt' if f < 0.6 else 'En kijk:\nhet rood is weg',
        gr=64, kl='ink', vet=True, ra=1.1, naam='!!kop')
    onderschrift(s, 'Alles boven 200 is te veel.' if f < 0.6
                 else 'De druk zit nu verdeeld over de hele voet.')

# ============================================================== 7 — het slot
s = dia(5.5)
# de boom links weggelaten: daar staat nu de tekst
park(s, bomen=((1620, 1.25), (1120, 0.75)))
figuur(s, FRANS, 'f', 1180, Y_F, SC_F, been=(-10, 10), arm=(8, -8))
figuur(s, LOTTE, 'l', 1560, Y_L, SC_L, been=(10, -10), arm=(-8, 8))
# Gemeten aan de afdruk: op dertig punt passen er maar drie-en-dertig tekens
# in negenhonderd eenheden. Vandaar korte regels en een kleiner korps — anders
# slaat elke regel om en schuift alles over elkaar.
txt(s, 120, 110, 1000, 400, 'Werkt dat\necht?', gr=76, kl='ink', vet=True,
    ra=1.05, naam='!!kop')
txt(s, 124, 524, 980, 270,
    'Zes Belgische ziekenhuizen\nzoeken het nu samen uit,\nook AZ Groeninge in Kortrijk.',
    gr=26, kl='gedempt', ra=1.35)
for i in range(6):
    vorm(s, MSO_SHAPE.OVAL, 128 + i * 62, 806, 42, 42, vul='groen2',
         naam='!!ziek%d' % i)
txt(s, 124, 872, 900, 50, 'PARADISE  ·  KU Leuven Campus Brugge', gr=19,
    kl='licht', font=FONT_M, sp=1.4)
onderschrift(s, 'Wat we tot nu toe schatten, gaan we eindelijk meten.')

prs.save(DOEL)
print('%d dia\'s · %.0f seconden · %s'
      % (len(TIJDEN), sum(TIJDEN) + 0.9 * (len(TIJDEN) - 1),
         os.path.basename(DOEL)))

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
        # bestand, tijden gebruiken, standaardduur, 1080 lijnen, 30 b/s, kwaliteit
        "$pr.CreateVideo('%s', $true, 3, 1080, 30, 100); "
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
