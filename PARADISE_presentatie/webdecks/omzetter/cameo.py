"""Zet op elke dia een live camera (cameo), zodat de spreker zichtbaar blijft bij een online presentatie.

    python cameo.py <in.pptx> <uit.pptx> [dianummer=x,y,d ...]

Het object is wat PowerPoint zelf maakt met Invoegen > Cameo: een p:pic met alf:liveFeedProps en een svg als
plaatshouder (cameo_plaatshouder.svg, overgenomen uit een opname van 12 oktober 2026). De plaats is in px op
1920 x 1080: standaard PLEK, per dia af te wijken met dianummer=x,y,d. De overgangen vallen weg: een fade dimt
ook het gezicht van de spreker, en een harde wissel blijft scherper in de videostroom van Teams.
"""
import sys
import uuid
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn

EMU = 6350
PLEK = (1656, 24, 240)
SVG = Path(__file__).parent / 'cameo_plaatshouder.svg'
NS = ('xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


def camera(vorm_id, r_id, x, y, d):
    return etree.fromstring(
        f'<p:pic {NS}><p:nvPicPr><p:cNvPr id="{vorm_id}" name="Camera {vorm_id - 1}"><a:extLst>'
        '<a:ext uri="{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}"><a16:creationId '
        f'xmlns:a16="http://schemas.microsoft.com/office/drawing/2014/main" id="{{{str(uuid.uuid4()).upper()}}}"/></a:ext>'
        '</a:extLst></p:cNvPr><p:cNvPicPr><a:picLocks noChangeAspect="1"/><a:extLst>'
        '<a:ext uri="{51228E76-BA90-4043-B771-695A4F85340A}"><alf:liveFeedProps '
        'xmlns:alf="http://schemas.microsoft.com/office/drawing/2021/livefeed"/></a:ext></a:extLst></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
        '<p:blipFill><a:blip><a:extLst><a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}"><asvg:svgBlip '
        f'xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="{r_id}"/></a:ext></a:extLst></a:blip>'
        '<a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm>'
        f'<a:off x="{x * EMU}" y="{y * EMU}"/><a:ext cx="{d * EMU}" cy="{d * EMU}"/></a:xfrm>'
        '<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def main(bron, uit, afwijkend):
    prs = Presentation(bron)
    deel = Part(PackURI('/ppt/media/cameo.svg'), 'image/svg+xml', prs.part.package, SVG.read_bytes())
    for i, dia in enumerate(prs.slides, 1):
        x, y, d = afwijkend.get(i, PLEK)
        boom = dia.shapes._spTree
        boom.append(camera(max(int(e) for e in boom.xpath('.//p:cNvPr/@id')) + 1, dia.part.relate_to(deel, RT.IMAGE), x, y, d))
        for overgang in dia._element.findall(qn('p:transition')):
            dia._element.remove(overgang)
    prs.core_properties.author = prs.core_properties.last_modified_by = 'Janou De Buyser'
    prs.save(uit)
    print(f'{len(prs.slides)} dia\'s met cameo: {uit}')


if __name__ == '__main__':
    plekken = {int(k): tuple(int(v) for v in w.split(',')) for k, w in (a.split('=') for a in sys.argv[3:])}
    main(sys.argv[1], sys.argv[2], plekken)
