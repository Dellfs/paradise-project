# Installeert DM Serif Display, DM Sans en JetBrains Mono (OFL, Google Fonts / JetBrains) voor de huidige
# Windows-gebruiker: kopie naar %LOCALAPPDATA%\Microsoft\Windows\Fonts + registerwaarde onder HKCU. Geen adminrechten nodig.
import os
import shutil
import urllib.request
import winreg
from pathlib import Path

from PIL import ImageFont

BRON = {
    'DMSerifDisplay-Regular.ttf': 'https://github.com/google/fonts/raw/main/ofl/dmserifdisplay/DMSerifDisplay-Regular.ttf',
    'DMSerifDisplay-Italic.ttf': 'https://github.com/google/fonts/raw/main/ofl/dmserifdisplay/DMSerifDisplay-Italic.ttf',
    'JetBrainsMono-Regular.ttf': 'https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf',
    'JetBrainsMono-Bold.ttf': 'https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Bold.ttf',
}
for stijl in ('Regular', 'Medium', 'Bold', 'Italic', 'BoldItalic'):
    BRON[f'DMSans-{stijl}.ttf'] = f'https://github.com/googlefonts/dm-fonts/raw/main/Sans/fonts/ttf/DMSans-{stijl}.ttf'

HIER = Path(__file__).parent / 'fonts'
HIER.mkdir(exist_ok=True)
DOEL = Path(os.environ['LOCALAPPDATA']) / 'Microsoft' / 'Windows' / 'Fonts'
DOEL.mkdir(parents=True, exist_ok=True)
sleutel = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows NT\CurrentVersion\Fonts')
for naam, url in BRON.items():
    bestand = HIER / naam
    if not bestand.exists():
        urllib.request.urlretrieve(url, bestand)
    familie, stijl = ImageFont.truetype(str(bestand), 12).getname()
    shutil.copy2(bestand, DOEL / naam)
    winreg.SetValueEx(sleutel, f'{familie} {stijl} (TrueType)', 0, winreg.REG_SZ, str(DOEL / naam))
    print(f'{naam:28s} -> familie "{familie}", stijl "{stijl}"')
winreg.CloseKey(sleutel)
print('klaar; herstart PowerPoint als het openstond')
