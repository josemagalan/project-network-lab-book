#!/usr/bin/env node
/*
 * Figura del capítulo 4: el caso tipo (una precedencia implícita) en el comparador de métodos del portal, con la red de
 * las reglas de los conjuntos y la red mínima lado a lado.
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL, una copia local.
 * Uso, desde figuras/: node 04-capturas.cjs  →  04-tipo-comparador.png
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
const CAPTURAS = [['04-tipo-comparador.png', 'v=route&ex=tipo&graph=aoa&view=cmp&pair=rules,min', '.cmp-grid.pair']];

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
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
