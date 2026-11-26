#!/usr/bin/env node
/*
 * Figura del capítulo 3: la red ROY de la mudanza depurada (capítulo 2), tal como la dibuja el taller del portal.
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL, una copia local.
 * Uso, desde figuras/: node 03-capturas.cjs  →  03-roy-mudanza.png
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
const T = 'A%2C3%2C%2CInventario%3BB%2C2%2CA%2CEmbalar%2520el%2520vidrio%3BC%2C2%2CA%2CEmbalar%2520equipos%3BD%2C5%2C%2CPreparar%2520el%2520laboratorio%3BE%2C1%2CB%252C%2520C%252C%2520D%2CTransporte%3BF%2C3%2CE%252C%2520H%2CInstalar%2520equipos%3BG%2C1%2CE%2CDesembalar%2520el%2520vidrio%3BH%2C1%2CD%2CRevisar%2520la%2520seguridad';
const CAPTURAS = [['03-roy-mudanza.png', `v=work&t=${T}&step=1`]];

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
