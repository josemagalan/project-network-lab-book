# Portada: laboratorio de redes de proyectos

## Archivos y regeneración

- `portada.svg`: composición vertical, proporción 2:3, espacio de diseño de 1200 × 1800 unidades.
- `portada-horizontal.svg`: adaptación horizontal, 1800 × 1000 unidades.
- `portada.py`: fuente reproducible, solo con la biblioteca estándar de Python 3.

Desde la raíz del repositorio:

```sh
python3 figuras/portada.py
```

Los SVG son autónomos: sin imágenes enlazadas, JavaScript ni fuentes descargadas.
El texto permanece editable. Se utiliza Arial, con alternativas Helvetica y sans-serif.
La tipografía puede variar si esas fuentes no están instaladas en el sistema que abre el SVG.

## Concepto y procedencia

La portada vertical se incorpora a la página inicial mediante `book.cover-image`
y `book.cover-image-alt` en `_quarto.yml`. Su tamaño adaptable se define con
`img.quarto-cover-image` en `estilos.css`. El título, autores y enlaces de contacto
del libro se mantienen también como texto HTML accesible.

Ilustración editorial original, preparada con asistencia de Claude el 27 de noviembre
de 2026 a petición de José Manuel Galán: la misma composición que la portada de
*Evolución a la vista*, el libro hermano de algoritmos genéticos (`figuras/portada.py`
de su repositorio), para que los dos libros hagan serie, con el violeta del Real
Valladolid (`#921b88`) como color principal en lugar del verde. El azul `#1f63b0`
es el del recorrido básico del libro y el del favicon.

La composición conecta tres acciones del portal: definir la tabla de precedencias,
dibujar la red y calcular. El título completo y los cinco nombres proceden de los
metadatos del libro, conservando su orden. No se ha reproducido ninguna captura
ni ilustración de terceros.

La tabla, las redes, el Gantt y el histograma son esquemáticos y no reproducen la
interfaz del portal, pero la red es coherente. Seis actividades: A (3), B (2),
C (4, tras A), D (5, tras A y B), E (2, tras C) y F (3, tras D y E). El camino crítico
es A–C–E–F, de 12 días, en violeta; B tiene 2 días de holgura total y D, 1 (en azul,
con la holgura de trazos en el Gantt, dibujado a fechas tempranas). La red PERT de la
misma tabla tiene seis sucesos y una ficticia, 2 → 3, para que D espere a A y a B.
El guion comprueba las fechas y las holguras antes de dibujar. El histograma y la
normal del panel «Riesgo del plazo» no representan datos: solo sugieren que la
duración simulada tiene la cola a la derecha de la normal del camino crítico
(capítulo 8).

## Licencia

La ilustración se ofrece bajo CC BY 4.0, como el contenido propio del libro
(`LICENSE-CONTENT.md`). El guion está bajo MIT, como el código del repositorio
(`LICENSE`). Las fuentes del sistema no se distribuyen con estos archivos.
