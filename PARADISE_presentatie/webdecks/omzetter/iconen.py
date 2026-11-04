"""Zet op elke dia waar een toestel aan bod komt het icoontje van dat toestel, rechtsboven naast de cameo.

Welk toestel: gezocht in de zichtbare tekst (zonder voetregel en bron) en in de notities; `extra` vult per dia aan of
haalt weg, bv. {33: '+N', 42: '-N'}, met N = Novel pedar, M = MoveMonitor, O = Orthotimer. De beeldjes staan in iconen/.
"""
import re
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

EMU = 6350
MAP = Path(__file__).parent / 'iconen'
TOESTEL = {'N': ('Novel pedar', 'novel_pedar.png', r'pedar|novel|drukmeting|pressure monitoring tool|\bmeting [AB]\b'),
           'M': ('MoveMonitor', 'movemonitor.png', r'movemonitor|dynaport|mcroberts'),
           'O': ('Orthotimer', 'orthotimer.png', r'orthotimer|draagsensor|uw sensor|hours/day')}
B, H, TUSSEN, BOVEN, RECHTS = 124, 90, 12, 24, 1640


def tekst_van(dia):
    delen = []
    for vorm in dia.shapes:
        if vorm.has_text_frame:
            t = vorm.text_frame.text.strip()
            if not t.startswith(('Novel pedar · MoveMonitor', 'Bron ·')):
                delen.append(t)
        if vorm.has_table:
            delen += [c.text for r in vorm.table.rows for c in r.cells]
    if dia.has_notes_slide:
        delen.append(dia.notes_slide.notes_text_frame.text)
    return ' '.join(delen)


def icoon(dia, sleutel, x):
    naam, bestand, _ = TOESTEL[sleutel]
    pic = dia.shapes.add_picture(str(MAP / bestand), Emu(x * EMU), Emu(BOVEN * EMU), Emu(B * EMU), Emu(H * EMU))
    pic.name = f'Icoon {naam}'
    pic._element.nvPicPr.cNvPr.set('descr', naam)
    pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
    geom = pic._element.spPr.find(qn('a:prstGeom')).find(qn('a:avLst'))
    geom.append(geom.makeelement(qn('a:gd'), {'name': 'adj', 'fmla': 'val 11000'}))
    pic.line.color.rgb = RGBColor(0xD3, 0xDF, 0xE8)
    pic.line.width = Pt(0.75)


def zet(bron, uit, extra=None, rechts=None):
    """rechts: dianummers waar de rij elders eindigt omdat de cameo er niet rechtsboven staat, bv. {66: 1792}."""
    prs = Presentation(bron)
    for i, dia in enumerate(prs.slides, 1):
        tekst = tekst_van(dia)
        keuze = {k for k, (_, _, patroon) in TOESTEL.items() if re.search(patroon, tekst, flags=re.I)}
        for teken, letters in re.findall(r'([+-])([NMO]+)', (extra or {}).get(i, '')):
            keuze = keuze | set(letters) if teken == '+' else keuze - set(letters)
        x = (rechts or {}).get(i, RECHTS)
        for k in reversed([k for k in TOESTEL if k in keuze]):
            x -= B
            icoon(dia, k, x)
            x -= TUSSEN
    prs.save(uit)
