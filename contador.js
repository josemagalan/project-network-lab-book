/*
 * Total de páginas vistas en el pie de página / Page-view total in the page footer.
 * El recuento lo hace GoatCounter (sin cookies), con el script que carga cada página desde _quarto.yml.
 * El sitio de GoatCounter es el mismo que el de «Evolución a la vista» y el del portal, así que todas las
 * páginas del libro cuentan en una sola ruta (RUTA, fijada en data-goatcounter-settings) para que su total
 * no se mezcle con el de los otros. Este archivo solo lee el total público de esa ruta y lo muestra.
 * Si la petición falla (sin conexión, bloqueador de contenido, contador no activado), no muestra nada.
 */
(function () {
  'use strict';
  var PANEL = 'https://josemagalan.goatcounter.com/';
  var RUTA = '/project-network-lab-book/';
  var es = (document.documentElement.lang || 'es').slice(0, 2) !== 'en';
  var pie = document.querySelector('.nav-footer-right');
  if (!pie || !window.fetch) return;
  fetch(PANEL + 'counter/' + encodeURIComponent(RUTA) + '.json')
    .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error(r.status)); })
    .then(function (d) {
      // El total llega como texto con separadores en inglés («1,234»): se lee como número y se escribe en el idioma del libro.
      var cifras = String(d && d.count != null ? d.count : '').replace(/[^\d]/g, '');
      if (!cifras || cifras === '0') return;
      var n = Number(cifras).toLocaleString(es ? 'es-ES' : 'en-GB');
      var a = document.createElement('a');
      a.href = PANEL;
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = es ? 'estadísticas' : 'statistics';
      pie.textContent = (es ? 'Páginas vistas: ' : 'Page views: ') + n + ' · ';
      pie.appendChild(a);
    })
    .catch(function () {});
})();
