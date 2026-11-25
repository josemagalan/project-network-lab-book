# Comprobaciones del libro

Los ejemplos del libro abren el portal [Project Network Lab](https://josemagalan.github.io/project-network-lab/) en un estado fijado, y el portal se actualiza por separado. Aquí están:

- `portal.json`: el commit del portal revisado para el libro (`revisado`) y los archivos cuyos cambios no afectan a los ejemplos (`ignorar`).
- `comprobar.cjs`: comprueba el libro frente al portal (Node 22 y git).
- `html.cjs`: comprueba el libro generado (solo Node 22).

## Frente al portal (`comprobar.cjs`)

1. **Versión.** Clona el portal y lo compara con `revisado`. Si han cambiado archivos que pueden alterar los ejemplos, falla y dice qué capítulos enlazan con el portal. Los cambios en README, pruebas, imágenes o la integración continua solo se anotan.
2. **Direcciones.** Descodifica cada dirección del portal que hay en los capítulos con el propio `js/core/urlstate.js` del portal. Falla si lleva un parámetro desconocido o un valor que el portal no acepta (el portal abriría su estado por defecto y el resultado no coincidiría con el del libro), o si la página no existe. Las instrucciones del texto que piden un estado sin enlace se comprueban con una anotación invisible junto a ellas:

   ```html
   <!-- comprobar: https://josemagalan.github.io/project-network-lab/cpm.html?lang=es#v=unc&um=m7 -->
   ```

`.github/workflows/comprobar.yml` lo ejecuta en cada *push* y *pull request*, cada lunes y a mano. No bloquea la publicación.

En local: `node comprobaciones/comprobar.cjs` (con `--sin-versiones`, solo las direcciones; con `PNL_PORTAL=/ruta/al/portal`, usa esa copia en lugar de clonar).

Al volver a comprobar el portal: repetir los ejemplos afectados, actualizar `revisado` en `portal.json` y explicar en `comentario` qué ha cambiado.

## El HTML generado (`html.cjs`)

Comprueba archivos y anclas locales, identificadores duplicados, referencias sin resolver, textos alternativos, títulos de iframe y, en cada capítulo, que el resumen y la continuación cierran el recorrido básico. También que los capítulos generados son los de `_quarto.yml`.

```bash
quarto render
node comprobaciones/html.cjs
```

`.github/workflows/publish.yml` lo ejecuta antes de publicar: si falla, no se publica.
