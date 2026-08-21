#!/usr/bin/env node
/**
 * Genereert de voorgerenderde Nederlandse inhoud van paradise-academy.html.
 *
 * Waarom dit bestaat. De MOOC draagt elke tekst twee keer: eenmaal in de
 * JS-data (ACADEMY, DATA, UI) en eenmaal als kant-en-klare HTML in <div
 * id="app">. Dat is met opzet — die tweede kopie maakt de pagina volledig
 * leesbaar zonder JavaScript, en pas wie op EN klikt laat de JS hertekenen.
 * De prijs is dat de twee stil uit elkaar kunnen lopen, en dat gebeurde ook:
 * een gewijzigd quizantwoord in de data bleef in de HTML op de oude tekst staan.
 *
 * Voortaan is de JS-data de enige bron en is de HTML een gegenereerd artefact.
 * Pas de data aan, draai dit script, commit het resultaat.
 *
 *   node maak_academy.js          schrijft de HTML bij
 *   node maak_academy.js --check  meldt alleen of ze gelijk staan (exit 1 bij drift)
 */
'use strict';
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const BESTAND = path.join(__dirname, 'paradise-academy.html');
const START = '<div id="app">';

function scriptBron(html) {
  const blok = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)]
    .filter(m => !/src=|ld\+json/.test(m[1] || ''));
  if (!blok.length) throw new Error('geen inline script gevonden');
  return blok[0][2];
}

/** Draait het paginascript in een lege omgeving en geeft buildBody() terug. */
function bouwer(html) {
  const bron = scriptBron(html).replace(
    '(function(global){',
    '(function(global){ global.__bouw=function(){return buildBody;};');
  const ctx = {
    console,
    localStorage: { getItem: () => null, setItem() {} },
    document: {
      documentElement: { classList: { add() {} } },
      body: { classList: { add() {} } },
      getElementById: () => null,
      querySelector: () => null,
      querySelectorAll: () => [],
      addEventListener() {}
    }
  };
  ctx.window = ctx; ctx.self = ctx; ctx.top = ctx;
  vm.createContext(ctx);
  vm.runInContext(bron, ctx);
  if (!ctx.__bouw) throw new Error('buildBody niet bereikbaar gemaakt');
  return ctx.__bouw();
}

/** De grenzen van de inhoud in <div id="app"> … </div>. */
function grenzen(html) {
  const i = html.indexOf(START);
  if (i < 0) throw new Error('<div id="app"> niet gevonden');
  const van = i + START.length;
  const tot = html.lastIndexOf('</div>', html.indexOf('<script', van));
  if (tot < van) throw new Error('einde van #app niet gevonden');
  return { van, tot };
}

const html = fs.readFileSync(BESTAND, 'utf8');
const nieuw = bouwer(html)();
const { van, tot } = grenzen(html);
const huidig = html.slice(van, tot);
const gelijk = huidig.replace(/\s+/g, ' ').trim() === nieuw.replace(/\s+/g, ' ').trim();

if (process.argv.includes('--check')) {
  if (gelijk) {
    console.log('paradise-academy.html: voorgerenderde HTML loopt gelijk met de data.');
  } else {
    const a = huidig.replace(/\s+/g, ' ').trim(), b = nieuw.replace(/\s+/g, ' ').trim();
    let k = 0; while (k < a.length && k < b.length && a[k] === b[k]) k++;
    console.log('DRIFT in paradise-academy.html — draai: node maak_academy.js');
    console.log('  in de HTML : …' + a.slice(Math.max(0, k - 60), k + 90));
    console.log('  in de data : …' + b.slice(Math.max(0, k - 60), k + 90));
    process.exitCode = 1;
  }
} else if (gelijk) {
  console.log('Al gelijk, niets te doen.');
} else {
  fs.writeFileSync(BESTAND, html.slice(0, van) + nieuw + html.slice(tot), 'utf8');
  console.log('paradise-academy.html bijgewerkt uit de data (%d tekens).', nieuw.length);
}
