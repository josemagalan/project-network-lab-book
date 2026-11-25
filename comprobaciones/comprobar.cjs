#!/usr/bin/env node
/*
 * Comprobaciones del libro frente al portal Project Network Lab.
 *
 * 1. Versión: compara la versión actual del portal con la última revisada para el libro
 *    (portal.json, «revisado»). Si han cambiado archivos que pueden alterar los ejemplos, falla,
 *    los enumera y dice qué capítulos enlazan con el portal. Los cambios en README, pruebas,
 *    imágenes o la integración continua solo se anotan.
 * 2. Enlaces: lee las direcciones del portal que hay en los capítulos, y las que se anotan con
 *    <!-- comprobar: URL -->, y las descodifica con el propio core/urlstate.js del portal. Falla si
 *    una dirección lleva un parámetro desconocido o un valor que el portal no acepta (en ese caso
 *    el portal abriría su estado por defecto y el ejemplo no coincidiría con el libro). Comprueba
 *    también que la página enlazada existe en el portal.
 *
 * Uso: node comprobaciones/comprobar.cjs                 (necesita git y conexión)
 *      node comprobaciones/comprobar.cjs --sin-versiones  (solo los enlaces)
 *      PNL_PORTAL=/ruta/al/portal node comprobaciones/comprobar.cjs   (usa una copia local)
 * Salida: anotaciones de GitHub Actions (::error:: / ::warning:: / ::notice::) y un resumen.
 */
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const RAIZ = path.resolve(__dirname, '..');
const MANIFIESTO = JSON.parse(fs.readFileSync(path.join(__dirname, 'portal.json'), 'utf8'));
const SIN_VERSIONES = process.argv.includes('--sin-versiones');
const resumen = [];
let errores = 0;

function anotar(nivel, texto, archivo, linea) {
  const donde = archivo ? ` file=${archivo}${linea ? ',line=' + linea : ''}` : '';
  console.log(`::${nivel}${donde}::${texto}`);
  resumen.push(`- **${nivel}**: ${texto}${archivo ? ` (${archivo}${linea ? ':' + linea : ''})` : ''}`);
  if (nivel === 'error') errores++;
}

function git(args, cwd) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

// Copia del portal: la indicada en PNL_PORTAL o un clon temporal.
function portal() {
  if (process.env.PNL_PORTAL) return path.resolve(process.env.PNL_PORTAL);
  const destino = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'portal-')), 'portal');
  git(['clone', '--quiet', '--filter=blob:none', `https://github.com/${MANIFIESTO.repositorio}.git`, destino]);
  return destino;
}

// Capítulos del libro (los .qmd que empiezan por dos cifras) y sus direcciones del portal.
const capitulos = fs.readdirSync(RAIZ).filter((f) => /^\d\d-.*\.qmd$/.test(f)).sort();
const URL_PORTAL = new RegExp(`${MANIFIESTO.url.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&')}[^\\s)\\]"'>]*`, 'g');

function enlaces() {
  const lista = [];
  for (const archivo of capitulos) {
    const lineas = fs.readFileSync(path.join(RAIZ, archivo), 'utf8').split('\n');
    lineas.forEach((texto, i) => {
      for (const m of texto.matchAll(URL_PORTAL)) lista.push({ url: m[0], archivo, linea: i + 1 });
    });
  }
  return lista;
}

function ignorado(archivo) {
  return MANIFIESTO.ignorar.some((p) => (p.endsWith('/') ? archivo.startsWith(p) : archivo === p));
}

// ---------- 1. Versión ----------
function comprobarVersion(dir, usan) {
  const actual = git(['rev-parse', '--short', 'HEAD'], dir);
  const revisado = MANIFIESTO.revisado;
  if (git(['rev-parse', 'HEAD'], dir).startsWith(git(['rev-parse', revisado], dir))) {
    anotar('notice', `portal en ${actual}, el revisado para el libro`);
    return;
  }
  const cambiados = git(['diff', '--name-only', revisado, 'HEAD'], dir).split('\n').filter(Boolean);
  const relevantes = cambiados.filter((f) => !ignorado(f));
  if (!relevantes.length) {
    anotar('notice', `portal en ${actual}: desde ${revisado} solo cambian archivos que no afectan a los ejemplos (${cambiados.length})`);
    return;
  }
  const muestra = relevantes.slice(0, 15).join(', ') + (relevantes.length > 15 ? `… (${relevantes.length} en total)` : '');
  anotar('error', `el portal ha cambiado desde ${revisado} (ahora ${actual}): ${muestra}. ` +
    `Hay que volver a comprobar los ejemplos de ${usan.join(', ') || 'ningún capítulo'} y actualizar comprobaciones/portal.json`);
}

// ---------- 2. Enlaces ----------
function comprobarEnlaces(dir, lista) {
  const urlstate = require(path.join(dir, 'js', 'core', 'urlstate.js'));
  let buenos = 0;
  for (const { url, archivo, linea } of lista) {
    let u;
    try { u = new URL(url); } catch { anotar('error', `dirección mal formada: ${url}`, archivo, linea); continue; }
    const pagina = u.pathname.slice(new URL(MANIFIESTO.url).pathname.length) || 'index.html';
    if (!fs.existsSync(path.join(dir, pagina))) { anotar('error', `el portal no tiene ${pagina}: ${url}`, archivo, linea); continue; }
    const lang = u.searchParams.get('lang');
    if (lang && !['es', 'en'].includes(lang)) anotar('error', `idioma desconocido (${lang}): ${url}`, archivo, linea);
    if (u.hash && pagina !== 'index.html') {
      const { warning } = urlstate.decode(u.hash);
      if (warning === 'malformed' || warning === 'unknownParam') {
        anotar('error', `el portal no acepta este estado (${warning === 'malformed' ? 'valor no válido' : 'parámetro desconocido'}): ${url}`, archivo, linea);
        continue;
      }
    }
    buenos++;
  }
  anotar('notice', `${buenos} de ${lista.length} direcciones del portal válidas`);
}

const lista = enlaces();
const usan = [...new Set(lista.map((e) => e.archivo))];
let dir;
try {
  dir = portal();
} catch (e) {
  anotar('error', `no se pudo obtener el portal: ${e.message}`);
}
if (dir) {
  if (!SIN_VERSIONES && !process.env.PNL_PORTAL) comprobarVersion(dir, usan);
  comprobarEnlaces(dir, lista);
}

if (process.env.GITHUB_STEP_SUMMARY) {
  fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, `## Comprobaciones frente al portal\n\n${resumen.join('\n')}\n`);
}
console.log(`\n${errores ? `${errores} error(es)` : 'Sin errores'}.`);
process.exit(errores ? 1 : 0);
