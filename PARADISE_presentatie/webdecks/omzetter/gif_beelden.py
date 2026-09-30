# Zet enkele beelden van een GIF naast elkaar in één PNG, om de opname na te kijken: python gif_beelden.py <gif> <png>
import sys

from PIL import Image, ImageSequence

g = Image.open(sys.argv[1])
alle = [f.convert('RGB') for f in ImageSequence.Iterator(g)]
kies = [alle[0], alle[len(alle) // 4], alle[len(alle) // 2], alle[-1]]
w, h = kies[0].size
schaal = 480 / w
blad = Image.new('RGB', (int(w * schaal) * 4 + 30, int(h * schaal)), 'white')
for i, f in enumerate(kies):
    blad.paste(f.resize((int(w * schaal), int(h * schaal))), (i * (int(w * schaal) + 10), 0))
blad.save(sys.argv[2])
print(len(alle), 'beelden')
