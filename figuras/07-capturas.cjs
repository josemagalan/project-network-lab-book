#!/usr/bin/env node
/*
 * Figuras del capítulo 7: Mecánicas del Sureste con tres tiempos en la pestaña «Duraciones inciertas» (M5) del portal,
 * como tabla propia: la red con las medias, con F elegida.
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL, una copia local.
 * Uso, desde figuras/: node 07-capturas.cjs  →  07-red-medias.png
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
// Tabla propia de M5 (ut): Mecánicas con a, m y b (A 1 2 3, B 2 3 8, C 1 2 9, D 6 8 16, E 3 4 5, F 2 3 9, G 1 2 3,
// H 1 1 1, I 1 2 6, J 2 3 4, K 1 1 1), empaquetada con js/core/urlstate.js del portal.
const UT = 'LYxFgiOByMpkEQsLZbERBhIiGMPGUPGcPixdhQiIUSikPHEWgYijEMIcPiMDicDHMgEUijJEh42j0mmUhkMjERFjsDGkPGsPIIsEEbm8ZI0cgcVlUPoktnBHk1IEVKjVCktFhhIqMDk8Qh5FoVHrAiJNbEUpEU1nNhoVQsZKqVUnsDstjJdmrtdIlCJFCuE3LpdgA';
const CAPTURAS = [
  ['07-red-medias.png', `v=unc&ue=own&ut=${UT}&ua=F`, '.unc-netcard'],
];

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  const errores = [];
  pagina.on('pageerror', (e) => errores.push(e.message));
  for (const [archivo, estado, selector] of CAPTURAS) {
    await pagina.goto('about:blank');
    await pagina.goto(`${BASE}cpm.html?lang=es#${estado}`);
    const zona = pagina.locator(selector);
    await zona.waitFor();
    await pagina.waitForTimeout(800);
    await zona.screenshot({ path: archivo });
    console.log(archivo);
  }
  await navegador.close();
  if (errores.length) { console.error(errores.join('\n')); process.exit(1); }
})();
