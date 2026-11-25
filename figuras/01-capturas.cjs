#!/usr/bin/env node
/*
 * Figuras del capítulo 1: capturas de la red ROY y de la red PERT de Mecánicas del Sureste en el portal.
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL se puede usar
 * una copia local servida en otra dirección (por ejemplo, http://127.0.0.1:8770/).
 *
 * Uso, desde figuras/: node 01-capturas.cjs  →  01-roy.png y 01-pert.png
 * Los estados son los de los botones del capítulo: ruta guiada, paso 2 (red ROY) y paso 6 de la red PERT
 * (sucesos numerados, aún sin tiempos).
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
const CAPTURAS = [
  ['01-roy.png', 'v=route&ex=ej6&step=1'],
  ['01-pert.png', 'v=route&ex=ej6&graph=aoa&step=5'],
];

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  const errores = [];
  pagina.on('pageerror', (e) => errores.push(e.message));
  for (const [archivo, estado] of CAPTURAS) {
    await pagina.goto('about:blank');
    await pagina.goto(`${BASE}cpm.html?lang=es#${estado}`);
    const red = pagina.locator('#netView svg.net');
    await red.waitFor();
    await pagina.waitForTimeout(500);
    await red.screenshot({ path: archivo });
    console.log(archivo);
  }
  await navegador.close();
  if (errores.length) { console.error(errores.join('\n')); process.exit(1); }
})();
