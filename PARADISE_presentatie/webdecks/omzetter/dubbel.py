# Telt per dia de tekstvakken met dezelfde tekst op dezelfde plaats (dubbels) en meldt tekst die op een andere dia hoort.
import collections
import hashlib
import sys

from pptx import Presentation

p = Presentation(sys.argv[1])
print(sys.argv[1].split('\\')[-1], len(p.slides), 'dia\'s', hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest()[:8])
fout = 0
for i, s in enumerate(p.slides, 1):
    c = collections.Counter((sh.left, sh.top, sh.text_frame.text) for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip())
    for (l, t, tekst), n in c.items():
        if n > 1:
            fout += 1
            print(f'  dia {i}: {n}x "{tekst[:50]}"')
print('dubbels:', fout)
