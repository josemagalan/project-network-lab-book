#!/usr/bin/env node
/*
 * Figuras del capítulo 8: Mecánicas del Sureste con tres tiempos en el apartado «El TCL y sus trampas» (M6) del portal,
 * como tabla propia: el caso «El proyecto entero» con el plazo de 16 días (normal del camino crítico frente a la
 * simulación de 10 000 réplicas con la semilla 2026).
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL, una copia local.
 * Uso, desde figuras/: node 08-capturas.cjs  →  08-proyecto-entero.png
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
// La misma tabla propia del capítulo 7 (07-capturas.cjs): Mecánicas con a, m y b, empaquetada con js/core/urlstate.js.
const UT = 'LYxFgiOByMpkEQsLZbERBhIiGMPGUPGcPixdhQiIUSikPHEWgYijEMIcPiMDicDHMgEUijJEh42j0mmUhkMjERFjsDGkPGsPIIsEEbm8ZI0cgcVlUPoktnBHk1IEVKjVCktFhhIqMDk8Qh5FoVHrAiJNbEUpEU1nNhoVQsZKqVUnsDstjJdmrtdIlCJFCuE3LpdgA';
const CAPTURAS = [
  ['08-proyecto-entero.png', `v=unc&um=m6&ue=own&ut=${UT}&ux=proj`, '.unc-simcard'],
];

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  const errores = [];
  pagina.on('pageerror', (e) => errores.push(e.message));
  for (const [archivo, estado, selector] of CAPTURAS) {
    await pagina.goto('about:blank');
    await pagina.goto(`${BASE}cpm.html?lang=es#${estado}`);
    await pagina.getByText('Simulación terminada', { exact: false }).first().waitFor({ timeout: 60000 });
    const zona = pagina.locator(selector).first();
    await zona.waitFor();
    await pagina.waitForTimeout(800);
    await zona.screenshot({ path: archivo });
    console.log(archivo);
  }
  await navegador.close();
  if (errores.length) { console.error(errores.join('\n')); process.exit(1); }
})();
