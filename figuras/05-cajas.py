"""Figura del capítulo 5: la caja de la actividad F de Mecánicas del Sureste en los tres formatos del portal.

7 campos (ES · d · EF arriba, actividad en medio, LS · TF · LF abajo), 4 campos (actividad arriba, ES a la izquierda,
LS a la derecha y duración abajo) y compacta (ES / d / LS sobre el nodo), con el aspecto de las redes del portal.
Las cifras se comprueban con las de la ruta guiada (js/core/cpm.js, portal 74055bb). Se escribe el SVG a mano para
que el texto quede como texto y el archivo no cambie entre ejecuciones.
Uso, desde figuras/: python3 05-cajas.py  →  05-cajas.svg
"""

GRIS = '#8a8781'      # bordes, como en el portal
TINTA = '#222222'
SUAVE = '#6b6862'
LINEA = '#c9c6bf'     # separaciones internas de la caja
FUENTE = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

# Actividad F de Mecánicas del Sureste: d 3, ES 3, EF 6, LS 4, LF 7, TF 1.
F = {'act': 'F', 'd': 3, 'ES': 3, 'EF': 6, 'LS': 4, 'LF': 7, 'TF': 1}
assert F['EF'] == F['ES'] + F['d'] and F['LF'] == F['LS'] + F['d'] and F['TF'] == F['LS'] - F['ES']

PANEL = 250
ancho, alto = PANEL * 3, 232
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" '
     f'font-family="{FUENTE}">']


def texto(x, y, t, tam=15, peso=400, color=TINTA, ancla='middle'):
    s.append(f'<text x="{x}" y="{y}" text-anchor="{ancla}" font-size="{tam}" font-weight="{peso}" '
             f'fill="{color}">{t}</text>')


def titulo(i, t, sub):
    cx = i * PANEL + PANEL / 2
    texto(cx, 28, t, 15, 600)
    texto(cx, 48, sub, 12.5, 400, SUAVE)
    if i:
        s.append(f'<line x1="{i * PANEL}" y1="14" x2="{i * PANEL}" y2="{alto - 14}" stroke="#e2e0da" stroke-width="1"/>')


# --- 7 campos: tres filas; arriba ES · d · EF, en medio la actividad, abajo LS · TF · LF ---
titulo(0, '7 campos', 'el formato por defecto del portal')
w, h = 132, 96
x, y = (PANEL - w) / 2, 92
s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" stroke="{GRIS}" stroke-width="1.6"/>')
for yy in (y + h / 3, y + 2 * h / 3):
    s.append(f'<line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{LINEA}" stroke-width="1"/>')
for xx in (x + w / 3, x + 2 * w / 3):
    for y0 in (y, y + 2 * h / 3):
        s.append(f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y0 + h / 3}" stroke="{LINEA}" stroke-width="1"/>')
for k, campo in enumerate(('ES', 'd', 'EF')):
    texto(x + w / 6 + k * w / 3, y + h / 6 + 5, F[campo])
    texto(x + w / 6 + k * w / 3, y - 8, campo, 12, 400, SUAVE)
texto(x + w / 2, y + h / 2 + 6, F['act'], 17, 700)
for k, campo in enumerate(('LS', 'TF', 'LF')):
    texto(x + w / 6 + k * w / 3, y + 5 * h / 6 + 5, F[campo])
    texto(x + w / 6 + k * w / 3, y + h + 20, campo, 12, 400, SUAVE)

# --- 4 campos: actividad arriba, ES (t) a la izquierda, LS (T) a la derecha, duración abajo ---
titulo(1, '4 campos', 'actividad, ES, LS y duración')
w, h = 112, 96
x, y = PANEL + (PANEL - w) / 2, 92
s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" stroke="{GRIS}" stroke-width="1.6"/>')
for yy in (y + h / 3, y + 2 * h / 3):
    s.append(f'<line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{LINEA}" stroke-width="1"/>')
s.append(f'<line x1="{x + w / 2}" y1="{y + h / 3}" x2="{x + w / 2}" y2="{y + 2 * h / 3}" stroke="{LINEA}" stroke-width="1"/>')
texto(x + w / 2, y + h / 6 + 6, F['act'], 17, 700)
texto(x + w / 4, y + h / 2 + 5, F['ES'])
texto(x + 3 * w / 4, y + h / 2 + 5, F['LS'])
texto(x + w / 2, y + 5 * h / 6 + 5, F['d'])
texto(x - 10, y + h / 2 + 5, 'ES', 12, 400, SUAVE, 'end')
texto(x + w + 10, y + h / 2 + 5, 'LS', 12, 400, SUAVE, 'start')
texto(x + w / 2, y + h + 20, 'd', 12, 400, SUAVE)

# --- compacta: nodo redondeado con ES / d / LS encima ---
titulo(2, 'Compacta', 'tres cifras sobre el nodo')
w, h = 64, 40
x, y = 2 * PANEL + (PANEL - w) / 2, 120
s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#ffffff" stroke="{GRIS}" stroke-width="1.6"/>')
texto(x + w / 2, y + h / 2 + 6, F['act'], 17, 700)
texto(x + w / 2, y - 10, f"{F['ES']}/{F['d']}/{F['LS']}")
texto(x + w / 2, y - 32, 'ES / d / LS', 12, 400, SUAVE)

s.append('</svg>')
with open('05-cajas.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(s) + '\n')
print('05-cajas.svg')
