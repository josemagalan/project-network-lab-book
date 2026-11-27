# Proyectos a la vista

*Redes PERT, CPM y ROY en un laboratorio interactivo*

> **Borrador, versión 0.1.** El libro se está escribiendo. La versión y la fecha de revisión están en `_quarto.yml` (`libro-version` y `libro-revision`).

Libro para aprender a planificar proyectos con redes, con actividades sobre el portal [Project Network Lab](https://josemagalan.github.io/project-network-lab/) ([repositorio](https://github.com/josemagalan/project-network-lab)). Está pensado para estudiantes de grado en ingeniería, y sus secciones avanzadas sirven también para el máster. Es el libro hermano de [*Evolución a la vista*](https://josemagalan.github.io/genetic-algorithms-lab-book/), y sigue sus convenciones.

**Leer:** https://josemagalan.github.io/project-network-lab-book/

## Estructura

- **Parte I · Teoría y práctica.** Un capítulo de introducción, uno por módulo del portal (de la tabla de precedencias al Montecarlo), un caso de principio a fin, las extensiones (desfases, coste–tiempo y recursos) y la recapitulación.
- **Parte II · El portal en clase.** Guías para el profesorado: el taller, los ejercicios, los exámenes imprimibles y los bancos de Moodle.
- **Apéndices de referencia.** Catálogo de ejercicios, notaciones, glosario español–inglés, parámetros de la dirección y exportaciones.

Primero se escribe la edición en español; la inglesa, al final.

## Cómo está hecho

- Libro de [Quarto](https://quarto.org) (`_quarto.yml`); cada capítulo es un archivo `.qmd`.
- Cada capítulo combina explicaciones, ejemplos reproducibles que abren el portal en un estado fijado, instrucciones para explorar en el portal, ejercicios y, al final del recorrido, una caja «Más en el portal». Las secciones se marcan por nivel: Básico, Avanzado y Para saber más.
- La numeración es automática. Quarto numera capítulos, secciones y figuras, y las referencias se escriben con su identificador (`sección -@sec-redes-ejemplo`). Los ejemplos y ejercicios llevan el número de su sección; los escribe `filtros/numeracion.lua` a partir de `_numeracion.json`.
- `indice.qmd` (índice general) y `actividades.qmd` (índice de actividades) los genera `filtros/indices.py` en cada `quarto render`. No se editan a mano.
- Bibliografía en `referencias.bib`, con estilo APA en castellano (`vendor/csl/`).
- Sin dependencias externas en la página: KaTeX va en local (`vendor/katex/`).
- Al hacer *push* a `main`, GitHub Actions genera el libro, comprueba el HTML (`comprobaciones/html.cjs`) y lo publica en GitHub Pages (`.github/workflows/publish.yml`).
- `comprobaciones/comprobar.cjs` avisa si el portal cambia o si una dirección del libro pide un estado que el portal no acepta; lo ejecuta `.github/workflows/comprobar.yml` en cada *push* y cada lunes (`comprobaciones/LEEME.md`).

Para generarlo en local hacen falta Quarto (≥ 1.10), Python 3 y, para las comprobaciones, Node 22:

```bash
quarto render      # resultado en _book/
quarto preview     # vista previa que se actualiza al guardar
node comprobaciones/html.cjs
node comprobaciones/comprobar.cjs
```

Las figuras propias están en `figuras/`, junto al guion que las genera; los SVG y PNG se versionan, así que para generar el libro no hace falta ejecutar los guiones. La [portada vectorial](figuras/portada.svg) aparece en la página inicial del libro. Su [guion editable](figuras/portada.py) genera también una [adaptación horizontal](figuras/portada-horizontal.svg); la [ficha de la portada](figuras/portada.md) explica cómo regenerarla y su licencia.

## Comentarios

Cada página del libro tiene el enlace «Enviar un comentario sobre esta página», que abre un formulario de GitHub (`.github/ISSUE_TEMPLATE/comentario.yml`) con la página, el capítulo y la versión ya rellenos.

## Autores

José Manuel Galán\*, Silvia Díaz-de la Fuente, Virginia Ahedo, María Pereda y José Ignacio Santos. Filiaciones y ORCID en `_quarto.yml` y en el libro (Agradecimientos y avisos).

\* Autor de correspondencia.

## Agradecimientos y uso de IA

Los autores agradecen el apoyo del plan Claude Team para científicos de Anthropic. En la elaboración de este material se han utilizado asistentes de inteligencia artificial; los contenidos originales son obra de los autores, que revisan, corrigen y verifican todos los materiales y son los responsables de esta publicación.

## Licencia

- Texto, figuras propias y ejercicios: [CC BY 4.0](LICENSE-CONTENT.md).
- Código (`filtros/`, `comprobaciones/`, `figuras/` y `comentarios.js`): [MIT](LICENSE).
- Los componentes de terceros conservan su licencia: KaTeX (MIT, `vendor/katex/LICENSE`) y el estilo APA de CSL (CC BY-SA 3.0, `vendor/csl/LEEME.md`).
- La licencia del portal no se extiende al libro: cada recurso indica la suya.
