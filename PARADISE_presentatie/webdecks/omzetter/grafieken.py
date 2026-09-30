"""Echte PowerPoint-grafieken voor de canvasgrafieken die een gewone staaf- of lijngrafiek zijn.

Elke functie leest de cijfers uit de broncode van de canvas (embeds/<dia>_<k>.html), zodat PowerPoint dezelfde
getallen toont als het webdeck. REGISTER koppelt '<dia>_<k>' aan een functie; wat er niet in staat, wordt een GIF.
Elke functie geeft (vorm, richting) terug; richting is de wipe van de animatie ('onder' of 'links').
"""
import json
import math
import re

from pptx.chart.data import CategoryChartData, XyChartData
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.chart import (XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE, XL_TICK_LABEL_POSITION,
                             XL_TICK_MARK)
from pptx.oxml.ns import qn
from pptx.util import Pt, Emu

EMU = 6350          # per css-pixel op een dia van 1920 breed
LIJN, AS, LEGENDE, WIT = '15395A', '8FB0CA', 'C5D8E8', 'F2F8FC'


def js_waarde(bron, naam):
    """Leest `const NAAM=[...]` of `NAAM=[...]` uit JavaScript als Python-waarde."""
    m = re.search(r'(?<![\w.])' + naam + r'\s*=\s*\[', bron)
    begin = m.end() - 1
    diepte, i, in_tekst = 0, begin, None
    while True:
        ch = bron[i]
        if in_tekst:
            if ch == in_tekst:
                in_tekst = None
        elif ch in '\'"':
            in_tekst = ch
        elif ch == '[':
            diepte += 1
        elif ch == ']':
            diepte -= 1
            if diepte == 0:
                break
        i += 1
    tekst = bron[begin:i + 1].replace("'", '"')
    tekst = re.sub(r'([{,])\s*([A-Za-z_]\w*)\s*:', r'\1"\2":', tekst)       # {t:'..'} -> {"t":".."}
    return json.loads(tekst)


def rgb(h):
    return RGBColor.from_string(h.lstrip('#').upper())


def tekst_opmaak(font, grootte_px, kleur, vet=False):
    font.size = Pt(grootte_px / 2)
    font.name = 'Segoe UI'
    font.bold = vet
    font.color.rgb = rgb(kleur)


def basis(grafiek, ymax, ystap, legende=True, legende_px=24):
    grafiek.font.name = 'Segoe UI'
    grafiek.font.size = Pt(12)
    grafiek.font.color.rgb = rgb(AS)
    va = grafiek.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = 0, ymax, ystap
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = rgb(LIJN)
    va.major_gridlines.format.line.width = Pt(0.75)
    va.format.line.fill.background()
    va.major_tick_mark = XL_TICK_MARK.NONE
    tekst_opmaak(va.tick_labels.font, 24, AS)
    ca = grafiek.category_axis
    ca.format.line.color.rgb = rgb(LIJN)
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    tekst_opmaak(ca.tick_labels.font, 24, AS)
    # elk categorielabel tonen (lege labels blijven leeg): anders slaat PowerPoint er zelf over (alleen op een categorie-as)
    el = ca._element
    if el.tag == qn('c:catAx') and el.find(qn('c:tickLblSkip')) is None:
        skip = el.makeelement(qn('c:tickLblSkip'), {'val': '1'})
        nm = el.find(qn('c:noMultiLvlLbl'))
        nm.addprevious(skip) if nm is not None else el.append(skip)
    grafiek.has_legend = legende
    if legende:
        grafiek.legend.position = XL_LEGEND_POSITION.BOTTOM
        grafiek.legend.include_in_layout = False
        tekst_opmaak(grafiek.legend.font, legende_px, LEGENDE)
    # grafiek- en tekengebied doorzichtig: de dia-achtergrond blijft zichtbaar
    cs = grafiek._chartSpace
    doorzichtig(cs, cs.find(qn('c:chart')))
    pa = cs.find(qn('c:chart')).find(qn('c:plotArea'))
    laatste = [c for c in pa if c.tag in (qn('c:catAx'), qn('c:valAx'), qn('c:dateAx'), qn('c:serAx'), qn('c:dTable'))][-1]
    doorzichtig(pa, laatste)


def doorzichtig(ouder, na):
    """Voegt <c:spPr> zonder vulling en zonder rand toe, direct na `na` (volgorde volgens het schema)."""
    sp = ouder.find(qn('c:spPr'))
    if sp is None:
        sp = ouder.makeelement(qn('c:spPr'), {})
        na.addnext(sp)
    for kind in list(sp):
        sp.remove(kind)
    sp.append(sp.makeelement(qn('a:noFill'), {}))
    ln = sp.makeelement(qn('a:ln'), {})
    ln.append(ln.makeelement(qn('a:noFill'), {}))
    sp.append(ln)


def reeks_kleur(reeks, kleur):
    reeks.format.fill.solid()
    reeks.format.fill.fore_color.rgb = rgb(kleur)
    reeks.format.line.fill.background()


def kader(slide, it, marge=(0, 0, 0, 0)):
    """Plaatst de grafiek in het vak van de canvas, met marges in css-pixels (boven, rechts, onder, links)."""
    b, r, o, l = marge
    return (Emu(round((it['x'] + l) * EMU)), Emu(round((it['y'] + b) * EMU)),
            Emu(round((it['w'] - l - r) * EMU)), Emu(round((it['h'] - b - o) * EMU)))


def label(slide, it, x, y, w, tekst, kleur=AS, grootte=24, rechts=False, midden=False):
    from pptx.enum.text import PP_ALIGN
    tb = slide.shapes.add_textbox(Emu(round((it['x'] + x) * EMU)), Emu(round((it['y'] + y) * EMU)), Emu(round(w * EMU)), Emu(round(grootte * 1.4 * EMU)))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER if midden else PP_ALIGN.RIGHT if rechts else PP_ALIGN.LEFT
    run = p.add_run()
    run.text = tekst
    tekst_opmaak(run.font, grootte, kleur)
    return tb


# ------------------------------------------------------------------ DFC-deck
def dfc_scenario(slide, it, bron):
    K = js_waarde(bron, 'K')                     # [[naam, kleur], ...]
    G = js_waarde(bron, 'G')                     # [[groep, [waarden]], ...]
    data = CategoryChartData()
    data.categories = [g for g, _ in G]
    for k, (naam, _) in enumerate(K):
        data.add_series(naam, [vs[k] for _, vs in G])
    x, y, w, h = kader(slide, it, (60, 0, 0, 0))
    vorm = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, w, h, data)
    gr = vorm.chart
    basis(gr, 100, 25)
    gr.value_axis.tick_labels.number_format = '0"%"'
    gr.value_axis.tick_labels.number_format_is_linked = False
    plot = gr.plots[0]
    plot.gap_width, plot.overlap = 60, -10
    for k, reeks in enumerate(plot.series):
        reeks_kleur(reeks, K[k][1])
        for j, (_, vs) in enumerate(G):
            v = vs[k]
            dl = reeks.points[j].data_label
            dl.position = XL_LABEL_POSITION.OUTSIDE_END
            dl.text_frame.text = '> 99%' if v > 99.5 else f'{round(v)}%'
            tekst_opmaak(dl.text_frame.paragraphs[0].runs[0].font, 26, WIT, vet=True)
    label(slide, it, 80, 12, 800, 'kans dat alle 144 er zijn vóór eind maart 2028')
    return vorm, 'onder'


def dfc_belasting(slide, it, bron):
    if 'const KOP=' in bron:
        return dfc_belasting_per_visite(slide, it, bron)
    KL, NM, V = js_waarde(bron, 'KL'), js_waarde(bron, 'NM'), js_waarde(bron, 'V')
    n = len(V[0])
    data = CategoryChartData()
    data.categories = [str(m) if m in (1, 6, 12, 18, 24, 30) else ' ' for m in range(1, n + 1)]
    for naam, reeks in zip(NM, V):
        data.add_series(naam, reeks)
    x, y, w, h = kader(slide, it, (40, 0, 0, 0))
    vorm = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, x, y, w, h, data)
    gr = vorm.chart
    basis(gr, 25, 5)
    plot = gr.plots[0]
    plot.gap_width, plot.overlap = 25, 100
    for reeks, kleur in zip(plot.series, KL):
        reeks_kleur(reeks, kleur)
    label(slide, it, 0, 0, 400, 'uur per maand')
    label(slide, it, it['w'] - 400, it['h'] - 76, 400, 'maand na de start', rechts=True)
    return vorm, 'onder'


def dfc_belasting_per_visite(slide, it, bron):
    """Drie panelen (3, 2 en 1,5 per maand), elk een gestapelde grafiek met een kleur per visite; één legende eronder."""
    from pptx.enum.shapes import MSO_SHAPE
    D, K, NM, KOP = js_waarde(bron, 'D'), js_waarde(bron, 'K'), js_waarde(bron, 'NM'), js_waarde(bron, 'KOP')
    PW, G, IN = 520, 52, 44
    from PIL import ImageFont
    try:
        vet = ImageFont.truetype('segoeuib.ttf', 30)
    except OSError:
        vet = None
    vormen = []
    for j, panel in enumerate(D):
        x0 = j * (PW + G) + (0 if j == 0 else IN - 30)
        titel = label(slide, it, x0 + 30, 4, 300, KOP[j][0], kleur=WIT, grootte=30)
        titel.text_frame.paragraphs[0].runs[0].font.bold = True
        breed = vet.getlength(KOP[j][0]) if vet else len(KOP[j][0]) * 16
        label(slide, it, x0 + 30 + breed + 16, 10, 320, KOP[j][1], kleur=AS)
        label(slide, it, x0 + 30, 50, 520, KOP[j][2], kleur=LEGENDE)
        label(slide, it, x0 + 30, 82, 520, KOP[j][3], kleur=LEGENDE)
        data = CategoryChartData()
        n = len(panel[0])
        data.categories = [str(m) if m in (1, 12, 24, 36) else ' ' for m in range(1, n + 1)]
        for naam, reeks in zip(NM, panel):
            data.add_series(naam, reeks)
        vorm = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Emu(round((it['x'] + x0) * EMU)), Emu(round((it['y'] + 112) * EMU)),
                                      Emu(round((PW + (IN if j == 0 else 30)) * EMU)), Emu(round(380 * EMU)), data)
        gr = vorm.chart
        basis(gr, 20, 5, legende=False)
        if j:
            gr.value_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
        plot = gr.plots[0]
        plot.gap_width, plot.overlap = 20, 100
        for reeks, kleur in zip(plot.series, K):
            reeks_kleur(reeks, kleur)
        vormen.append(vorm)
    # één legende voor de drie panelen, zoals in het webdeck
    lx = IN
    from PIL import ImageFont
    try:
        maat = ImageFont.truetype('segoeui.ttf', 24)
    except OSError:
        maat = None
    for naam, kleur in zip(NM, K):
        blok = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(round((it['x'] + lx) * EMU)), Emu(round((it['y'] + it['h'] - 34) * EMU)),
                                      Emu(22 * EMU), Emu(22 * EMU))
        blok.fill.solid()
        blok.fill.fore_color.rgb = rgb(kleur)
        blok.line.fill.background()
        label(slide, it, lx + 30, it['h'] - 40, 200, naam, kleur=LEGENDE)
        lx += 30 + (maat.getlength(naam) if maat else len(naam) * 12) + 34
    label(slide, it, it['w'] - 400, it['h'] - 40, 400, 'maand na de start', rechts=True)
    return [(v, 'onder') for v in vormen]


# ------------------------------------------------------------------ XY-grafieken (kanscurves)
def js_getal(bron, naam):
    return float(re.search(r'(?<![\w.])' + naam + r'\s*=\s*([\d.]+)', bron).group(1))


def js_kleur(bron, naam):
    return re.search(r'(?<![\w.])' + naam + r"\s*=\s*'#([0-9A-Fa-f]{6})'", bron).group(1)


def poisson_minstens(mu, n=24):
    """Kans op minstens n gebeurtenissen bij een Poisson-verdeling met gemiddelde mu, zoals de canvas rekent."""
    if mu <= 0:
        return 0.0
    return 1 - sum(math.exp(-mu + k * math.log(mu) - math.lgamma(k + 1)) for k in range(n))


def xy_basis(grafiek, xas, yas, kader_px, legende=False):
    """Assen zoals in de canvas, en het binnenste tekengebied vast op (L, T, R, B) van de canvas, zodat de lijnen samenvallen."""
    (xmin, xmax, xstap, xfmt), (ymax, ystap) = xas, yas
    basis(grafiek, ymax, ystap, legende=legende)
    grafiek.value_axis.tick_labels.number_format = '0"%"'
    grafiek.value_axis.tick_labels.number_format_is_linked = False
    xa = grafiek.category_axis                   # bij een XY-grafiek is dit de x-waardeas
    xa.minimum_scale, xa.maximum_scale, xa.major_unit = xmin, xmax, xstap
    xa.has_major_gridlines = False
    xa.tick_labels.number_format = xfmt
    xa.tick_labels.number_format_is_linked = False
    W, H, L, T, R, B = kader_px
    pa = grafiek._chartSpace.find(qn('c:chart')).find(qn('c:plotArea'))
    lay = pa.find(qn('c:layout'))
    if lay is None:
        lay = pa.makeelement(qn('c:layout'), {})
        pa.insert(0, lay)
    for kind in list(lay):
        lay.remove(kind)
    ml = lay.makeelement(qn('c:manualLayout'), {})
    for tag, val in (('layoutTarget', 'inner'), ('xMode', 'edge'), ('yMode', 'edge'),
                     ('x', L / W), ('y', T / H), ('w', (R - L) / W), ('h', (B - T) / H)):
        ml.append(ml.makeelement(qn('c:' + tag), {'val': f'{val:.4f}' if isinstance(val, float) else val}))
    lay.append(ml)


def xy_lijn(reeks, kleur, breedte_px, streep=False):
    reeks.smooth = False
    reeks.marker.style = XL_MARKER_STYLE.NONE
    reeks.format.line.color.rgb = rgb(kleur)
    reeks.format.line.width = Emu(round(breedte_px * EMU))
    if streep:
        reeks.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH


def xy_punt(reeks, kleur, diameter_px=18):
    reeks.format.line.fill.background()
    reeks.marker.style = XL_MARKER_STYLE.CIRCLE
    reeks.marker.size = round(diameter_px / 2)       # 1 css-pixel = 0,5 pt op een dia van 1920 breed
    reeks.marker.format.fill.solid()
    reeks.marker.format.fill.fore_color.rgb = rgb(kleur)
    reeks.marker.format.line.color.rgb = rgb('0A2540')
    reeks.marker.format.line.width = Pt(1.5)


def punt_label(reeks, idx, tekst, positie, grootte=28, vet=True, kleur=WIT, dy=0.0):
    dl = reeks.points[idx].data_label
    dl.text_frame.text = tekst
    dl.text_frame.word_wrap = False                  # één regel, zoals in de canvas
    tekst_opmaak(dl.text_frame.paragraphs[0].runs[0].font, grootte, kleur, vet=vet)
    dl.position = positie
    if dy:                                           # verschuiving als fractie van de grafiekhoogte
        el = dl._dLbl
        lay = el.makeelement(qn('c:layout'), {})
        ml = lay.makeelement(qn('c:manualLayout'), {})
        ml.append(ml.makeelement(qn('c:x'), {'val': '0'}))
        ml.append(ml.makeelement(qn('c:y'), {'val': f'{dy:.4f}'}))
        lay.append(ml)
        el.find(qn('c:idx')).addnext(lay)


def dfc_tempo(slide, it, bron):
    """Kans dat één centrum zijn 24 haalt binnen 12 maanden, per gemiddeld tempo; punten op 2 en 3 per maand."""
    W, H = js_getal(bron, 'W'), js_getal(bron, 'H')
    L, R, T, B, A, Z = (js_getal(bron, n) for n in ('L', 'R', 'T', 'B', 'A', 'Z'))
    BL, OR = js_kleur(bron, 'BL'), js_kleur(bron, 'OR')
    kans = lambda l: poisson_minstens(12 * l) * 100
    PUNTEN = [(2.0, OR), (3.0, BL)]
    data = XyChartData()
    curve = data.add_series('kans')
    stappen = round((Z - A) / 0.01)
    for i in range(stappen + 1):
        l = A + i * 0.01
        curve.add_data_point(round(l, 2), kans(l))
    for l, _ in PUNTEN:
        s = data.add_series(f'lood {l}')
        s.add_data_point(l, 0)
        s.add_data_point(l, kans(l))
    for l, _ in PUNTEN:
        data.add_series(f'punt {l}').add_data_point(l, kans(l))
    x, y, w, h = kader(slide, it)
    vorm = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS, x, y, w, h, data)
    gr = vorm.chart
    xy_basis(gr, (A, Z, 0.5, '0.0'), (100, 20), (W, H, L, T, R, B))
    reeksen = list(gr.plots[0].series)
    xy_lijn(reeksen[0], 'C5D8E8', 3)
    labels = []
    for k, (l, kleur) in enumerate(PUNTEN):
        xy_lijn(reeksen[1 + k], kleur, 2, streep=True)
        xy_punt(reeksen[3 + k], kleur)
        # tekstvak op dezelfde plek als in de canvas: rechts van het punt, basislijn Y+10 of Y+46
        X, Y = L + (l - A) / (Z - A) * (R - L), B - kans(l) / 100 * (B - T)
        tb = label(slide, it, X + 22, Y + (10 if l < 2.5 else 46) - 30, 360, f'{l:.0f} per maand → {round(kans(l))}%',
                   kleur=WIT, grootte=28)
        tb.text_frame.paragraphs[0].runs[0].font.bold = True
        labels.append((tb, 'vervaag'))
    label(slide, it, L, T - 38, 760, 'kans dat een centrum 24 haalt binnen 12 maanden')
    label(slide, it, L, B + 50, R - L, 'gemiddeld aantal inclusies per maand, per centrum', midden=True)
    return [(vorm, 'links')] + labels


def dfc_tweepermaand(slide, it, bron):
    """Kans dat de inclusie rond is, maand na maand: één centrum en alle zes, aan 3 en aan 2 per maand; grens op 13 maanden."""
    W, H = js_getal(bron, 'W'), js_getal(bron, 'H')
    L, R, T, B, XM, GRENS = (js_getal(bron, n) for n in ('L', 'R', 'T', 'B', 'XM', 'GRENS'))
    BL, OR = js_kleur(bron, 'BL'), js_kleur(bron, 'OR')
    REEKS = [(3, 1, BL, '3 per maand, één centrum'), (3, 6, BL, '3 per maand, alle zes'),
             (2, 1, OR, '2 per maand, één centrum'), (2, 6, OR, '2 per maand, alle zes')]
    v = lambda l, n, m: poisson_minstens(l * m) ** n * 100
    data = XyChartData()
    for l, n, _, naam in REEKS:
        s = data.add_series(naam)
        for i in range(round(XM / 0.05) + 1):
            m = i * 0.05
            s.add_data_point(round(m, 2), v(l, n, m))
    g = data.add_series('grens')
    for yy in (0, 5, 100):
        g.add_data_point(GRENS, yy)
    ALLE6 = [r for r in REEKS if r[1] > 1]
    for l, n, _, _ in ALLE6:
        data.add_series(f'punt {l}').add_data_point(GRENS, v(l, n, GRENS))
    x, y, w, h = kader(slide, it)
    vorm = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS, x, y, w, h, data)
    gr = vorm.chart
    xy_basis(gr, (0, XM, 6, '0'), (100, 25), (W, H, L, T, R, B))
    reeksen = list(gr.plots[0].series)
    for reeks, (l, n, kleur, _) in zip(reeksen, REEKS):
        xy_lijn(reeks, kleur, 3 if n > 1 else 2, streep=n > 1)
    xy_lijn(reeksen[4], WIT, 1.5, streep=True)
    XG = L + GRENS / XM * (R - L)
    labels = [(label(slide, it, XG + 10, B - 14 - 27, 300, '13: uiterste grens', kleur=WIT), 'vervaag')]
    for k, (l, n, kleur, _) in enumerate(ALLE6):
        xy_punt(reeksen[5 + k], kleur, 16)
        Y = B - v(l, n, GRENS) / 100 * (B - T)
        tekst = f'{round(v(l, n, GRENS))}%'
        if l == 2:                                   # links van het punt, zoals in de canvas
            tb = label(slide, it, XG - 16 - 160, Y + 9 - 28, 160, tekst, kleur=WIT, grootte=26, rechts=True)
        else:                                        # gecentreerd boven het punt
            tb = label(slide, it, XG - 80, Y - 18 - 28, 160, tekst, kleur=WIT, grootte=26, midden=True)
        tb.text_frame.paragraphs[0].runs[0].font.bold = True
        labels.append((tb, 'vervaag'))
    label(slide, it, L, B + 44, R - L, 'maanden na de start van de inclusie', midden=True)
    # legende zoals in de canvas: kleur = tempo, lijnstijl = één centrum of alle zes
    from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
    from PIL import ImageFont
    try:
        maat = ImageFont.truetype('segoeui.ttf', 24)
    except OSError:
        maat = None
    breedte = lambda t: maat.getlength(t) if maat else len(t) * 12
    px = lambda v: Emu(round(v * EMU))
    lx = L
    for t, k in (('3 per maand', BL), ('2 per maand', OR)):
        blok = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(it['x'] + lx), px(it['y'] + H - 36), px(22), px(22))
        blok.fill.solid()
        blok.fill.fore_color.rgb = rgb(k)
        blok.line.fill.background()
        label(slide, it, lx + 32, H - 40, breedte(t) + 20, t, kleur=LEGENDE)
        lx += 32 + breedte(t) + 40
    for t, streep in (('één centrum', False), ('alle zes', True)):
        ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, px(it['x'] + lx), px(it['y'] + H - 25), px(it['x'] + lx + 40), px(it['y'] + H - 25))
        ln.line.color.rgb = rgb(LEGENDE)
        ln.line.width = px(3)
        if streep:
            ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        label(slide, it, lx + 50, H - 40, breedte(t) + 20, t, kleur=LEGENDE)
        lx += 50 + breedte(t) + 40
    return [(vorm, 'links')] + labels


# ------------------------------------------------------------------ rekruteringsdeck
def rek_movemonitor(slide, it, bron):
    D = js_waarde(bron, 'D')                      # [[tempo, dag7, dag14, gem. dagen], ...]
    data = CategoryChartData()
    data.categories = [d[0] for d in D]
    data.add_series('terug op dag 7', [d[1] * 100 for d in D])
    data.add_series('terug na 14 dagen (werkhypothese)', [d[2] * 100 for d in D])
    x, y, w, h = kader(slide, it, (0, 0, 60, 0))
    vorm = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, w, h, data)
    gr = vorm.chart
    basis(gr, 20, 5)
    gr.value_axis.tick_labels.number_format = '0"%"'
    gr.value_axis.tick_labels.number_format_is_linked = False
    plot = gr.plots[0]
    plot.gap_width, plot.overlap = 90, -8
    for reeks, kleur, k in zip(plot.series, ('8FB0CA', '52BDEC'), (1, 2)):
        reeks_kleur(reeks, kleur)
        for j, d in enumerate(D):
            dl = reeks.points[j].data_label
            dl.position = XL_LABEL_POSITION.OUTSIDE_END
            dl.text_frame.text = f'{d[k] * 100:.1f}'.replace('.', ',') + '%'
            tekst_opmaak(dl.text_frame.paragraphs[0].runs[0].font, 24, WIT, vet=True)
    label(slide, it, 0, it['h'] - 44, it['w'],
          'Gemiddelde wachttijd bij 14 dagen: ' + ' · '.join(f'{d[3]:.1f}'.replace('.', ',') for d in D) + ' dagen')
    return vorm, 'onder'


def lijnen(slide, it, bron, ymax, ystap, titel, etiketten):
    S = js_waarde(bron, 'S')                      # [{t, k, v}, ...]
    n = len(S[0]['v'])
    data = CategoryChartData()
    data.categories = [str(m) if m in etiketten else ' ' for m in range(1, n + 1)]
    for s in S:
        data.add_series(s['t'], s['v'])
    x, y, w, h = kader(slide, it, (40, 0, 0, 0))
    vorm = slide.shapes.add_chart(XL_CHART_TYPE.LINE, x, y, w, h, data)
    gr = vorm.chart
    basis(gr, ymax, ystap)
    for reeks, s in zip(gr.plots[0].series, S):
        reeks.format.line.color.rgb = rgb(s['k'])
        reeks.format.line.width = Pt(2)
        reeks.smooth = False
        reeks.marker.style = XL_MARKER_STYLE.NONE
    label(slide, it, 0, 0, 700, titel)
    label(slide, it, it['w'] - 400, it['h'] - 76, 400, 'maand na de start', rechts=True)
    return vorm, 'links'


def rek_drievier(slide, it, bron):
    return lijnen(slide, it, bron, 25, 5, 'uren per maand, per centrum', (1, 6, 12, 18, 24))


def rek_totaal(slide, it, bron):
    return lijnen(slide, it, bron, 350, 50, 'opgetelde betaalde uren per centrum', (1, 6, 12, 18, 24, 30))


REGISTER = {
    ('dfc', 'tempo_0'): dfc_tempo,
    ('dfc', 'tweepermaand_0'): dfc_tweepermaand,
    ('dfc', 'scenario_0'): dfc_scenario,
    ('dfc', 'belasting_0'): dfc_belasting,
    ('rekrutering', 'movemonitor_0'): rek_movemonitor,
    ('rekrutering', 'drievier_0'): rek_drievier,
    ('rekrutering', 'totaal_0'): rek_totaal,
}
