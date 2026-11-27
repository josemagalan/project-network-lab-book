#!/usr/bin/env node
/*
 * Figuras del capítulo 10: Electrona en el portal.
 * - 10-roy.png y 10-pert.png: el taller con la tabla de Electrona (enunciado ej5 de «Del enunciado a la tabla»), paso 2
 *   (red ROY) y paso 6 de la red PERT (sucesos numerados, aún sin tiempos);
 * - 10-duracion.png y 10-indices.png: Electrona con tres tiempos como tabla propia del apartado «Montecarlo e índices»
 *   (M7), beta-PERT, 10 000 réplicas, semilla 2026, plazo de 19 días y percentil 90; en la vista «Índices», solo el
 *   tornado y la red ROY coloreada por criticidad (las dos tablas se ocultan con CSS, como en 09-capturas.cjs).
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL, una copia local.
 * Uso, desde figuras/: node 10-capturas.cjs  →  10-roy.png, 10-pert.png, 10-duracion.png y 10-indices.png
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
const T = 'A%2C3%2C%2CMateriales%2520de%2520X%2520e%2520Y%3BB%2C1%2C%2CPuesta%2520a%2520punto%3BC%2C2%2C%2CMateriales%2520de%2520Z%3BD%2C7%2CA%252C%2520B%2CFabricar%2520Y%3BE%2C5%2CB%252C%2520C%2CFabricar%2520Z%3BF%2C6%2CA%252C%2520B%2CFabricar%2520X%3BG%2C1%2CF%2CTransportar%2520X%3BH%2C2%2CD%252C%2520E%2CEnsamblar%2520YZ%3BI%2C1%2CH%2CTransportar%2520YZ%3BJ%2C3%2CG%252C%2520I%2CEnsamblar%2520XYZ%3BK%2C1%2CJ%2CEnvasar';
const UT = 'LYxFgiOByMpkEQsLZbERBhIiGUPGcPG0Ph5NMJ0MpyNJhNhlOYgMhlEBYEEkLIiLsKERCh4xl8Si0DKB1kB0MIgnJwOpuOhvlUsIcxgcRgY1mYijEajkekEikhaoMMIkUh43h45h5BFggl0DIxhMUcMZhOQglMrhhFh40h9IgY4h5CrtDsFislmEFStQiI1vq0DGNygdcr0PsNjNNls5YqYiI9EEUwwWIh5UORhNxzOBvOU4xuPJEPo0QmUDIldtkDIubMJtMRsvRZvksJOSymTh-jgeYzWcz2gtG1hhK0mnEVwyFd2-s12w2WN2mPJe4yXG5x2MJzs0qLpdgA';
const REDES = [['10-roy.png', `v=work&t=${T}&step=1`], ['10-pert.png', `v=work&t=${T}&graph=aoa&step=5`]];
const M7 = [
  ['10-duracion.png', `v=unc&um=m7&ue=own&ut=${UT}&ud=19&uv=90`, 'Resultados', ''],
  ['10-indices.png', `v=unc&um=m7&ue=own&ut=${UT}&ud=19&uy=idx&ui=cr`, 'Caminos y su criticidad',
    '.m7-idx, .unc-pathscard { display: none !important; }'],
];

(async () => {
  const navegador = await chromium.launch();
  const errores = [];
  let pagina = await navegador.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  pagina.on('pageerror', (e) => errores.push(e.message));
  for (const [archivo, estado] of REDES) {
    await pagina.goto('about:blank');
    await pagina.goto(`${BASE}cpm.html?lang=es#${estado}`);
    const red = pagina.locator('#netView svg.net');
    await red.waitFor();
    await pagina.waitForTimeout(500);
    await red.screenshot({ path: archivo });
    console.log(archivo);
  }
  await pagina.close();
  pagina = await navegador.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  pagina.on('pageerror', (e) => errores.push(e.message));
  for (const [archivo, estado, listo, css] of M7) {
    await pagina.goto('about:blank');
    await pagina.goto(`${BASE}cpm.html?lang=es#${estado}`);
    await pagina.getByText('10.000 réplicas simuladas', { exact: false }).first().waitFor({ timeout: 60000 });
    await pagina.getByText(listo, { exact: false }).first().waitFor({ timeout: 60000 });
    await pagina.waitForTimeout(1500);
    if (css) await pagina.addStyleTag({ content: css });
    await pagina.waitForTimeout(500);
    await pagina.locator('section.unc .unc-main').first().screenshot({ path: archivo });
    console.log(archivo);
  }
  await navegador.close();
  if (errores.length) { console.error(errores.join('\n')); process.exit(1); }
})();
