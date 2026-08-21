/**
 * De MOOC draagt elke tekst twee keer: in de JS-data en als voorgerenderde
 * HTML in <div id="app">. Die tweede kopie maakt de pagina leesbaar zonder
 * JavaScript en is dus geen fout — maar ze kan stil uit de pas lopen, en dat
 * is ook gebeurd: een gewijzigd quizantwoord bleef in de HTML op de oude tekst
 * staan, zodat een Nederlandstalige bezoeker het verkeerde antwoord las.
 *
 * Deze toets draait de generator in controlestand. Faalt hij, draai dan
 * `node maak_academy.js` en commit het resultaat.
 */
'use strict';
const { execFileSync } = require('child_process');
const path = require('path');

const WORTEL = path.join(__dirname, '..');
let fouten = 0;

function check(label, waar) {
  console.log((waar ? '  ok   - ' : '  FAIL - ') + label);
  if (!waar) fouten++;
}

let uit = '', code = 0;
try {
  uit = execFileSync(process.execPath, [path.join(WORTEL, 'maak_academy.js'), '--check'],
                     { cwd: WORTEL, encoding: 'utf8' });
} catch (e) {
  uit = (e.stdout || '') + (e.stderr || '');
  code = e.status || 1;
}

check('voorgerenderde HTML loopt gelijk met de JS-data', code === 0);
if (code !== 0) {
  console.log(uit.split('\n').map(r => '        ' + r).join('\n'));
}

console.log(fouten ? '\nEr faalden checks.' : '\nAlle checks geslaagd.');
process.exitCode = fouten ? 1 : 0;
