#!/usr/bin/env node
/*
 * Figuras del capítulo 9: Mecánicas del Sureste con tres tiempos en el apartado «Montecarlo e índices» (M7) del portal,
 * como tabla propia, con la beta-PERT, 10 000 réplicas, la semilla 2026 y el plazo de 16 días:
 * - 09-duracion.png: vista «Duración del proyecto» (histograma, función de distribución y tabla de resultados);
 * - 09-indices.png: vista «Índices», solo el tornado en espejo y la red ROY coloreada por criticidad (las dos tablas se
 *   ocultan con CSS para que las dos tarjetas queden una al lado de la otra).
 * Usa Playwright (Chromium). Por defecto captura el portal publicado; con PNL_PORTAL_URL, una copia local.
 * Uso, desde figuras/: node 09-capturas.cjs  →  09-duracion.png y 09-indices.png
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.env.PNL_PORTAL_URL || 'https://josemagalan.github.io/project-network-lab/';
// La misma tabla propia de los capítulos 7 y 8 (07-capturas.cjs, 08-capturas.cjs).
const UT = 'LYxFgiOByMpkEQsLZbERBhIiGMPGUPGcPixdhQiIUSikPHEWgYijEMIcPiMDicDHMgEUijJEh42j0mmUhkMjERFjsDGkPGsPIIsEEbm8ZI0cgcVlUPoktnBHk1IEVKjVCktFhhIqMDk8Qh5FoVHrAiJNbEUpEU1nNhoVQsZKqVUnsDstjJdmrtdIlCJFCuE3LpdgA';
const CAPTURAS = [
  // [archivo, estado, texto que indica que ha terminado, CSS extra]
  ['09-duracion.png', `v=unc&um=m7&ue=own&ut=${UT}`, 'Resultados', ''],
  ['09-indices.png', `v=unc&um=m7&ue=own&ut=${UT}&uy=idx&ui=cr`, 'Caminos y su criticidad',
    '.m7-idx, .unc-pathscard { display: none !important; }'],
];

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2, colorScheme: 'light' });
  const errores = [];
  pagina.on('pageerror', (e) => errores.push(e.message));
  for (const [archivo, estado, listo, css] of CAPTURAS) {
    await pagina.goto('about:blank');
    await pagina.goto(`${BASE}cpm.html?lang=es#${estado}`);
    await pagina.getByText('10.000 réplicas simuladas', { exact: false }).first().waitFor({ timeout: 60000 });
    await pagina.getByText(listo, { exact: false }).first().waitFor({ timeout: 60000 });
    await pagina.waitForTimeout(1500);   // los índices se calculan a trozos después de la simulación
    if (css) await pagina.addStyleTag({ content: css });
    await pagina.waitForTimeout(500);
    const zona = pagina.locator('section.unc .unc-main').first();
    await zona.screenshot({ path: archivo });
    console.log(archivo);
  }
  await navegador.close();
  if (errores.length) { console.error(errores.join('\n')); process.exit(1); }
})();
