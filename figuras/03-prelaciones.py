"""Figura del capítulo 3: los cuatro tipos de prelación en una red ROY.

Lineal, convergente, divergente y convergente-divergente, en cuatro paneles, con cajas y flechas
del mismo estilo que las redes del portal. Se escribe el SVG a mano para que el texto quede como
texto y el archivo no cambie entre ejecuciones. Uso, desde figuras/: python3 03-prelaciones.py
→  03-prelaciones.svg
"""

GRIS = '#8a8781'      # bordes y flechas, como en el portal
TINTA = '#222222'
SUAVE = '#6b6862'
W, H = 50, 34         # caja de actividad
PANEL = 232           # ancho de cada panel
X1, X2 = 34, 148      # columnas de cajas dentro del panel (borde izquierdo)
ARRIBA, MEDIO, ABAJO = 88, 135, 182   # centros verticales

# (título, relaciones, cajas {letra: (columna, y)}, flechas [(origen, destino)])
PANELES = [
    ('Lineal', 'A → B',
     {'A': (X1, MEDIO), 'B': (X2, MEDIO)}, [('A', 'B')]),
    ('Convergente', 'A → C · B → C',
     {'A': (X1, ARRIBA), 'B': (X1, ABAJO), 'C': (X2, MEDIO)}, [('A', 'C'), ('B', 'C')]),
    ('Divergente', 'A → B · A → C',
     {'A': (X1, MEDIO), 'B': (X2, ARRIBA), 'C': (X2, ABAJO)}, [('A', 'B'), ('A', 'C')]),
    ('Convergente-divergente', 'A y B → C y D',
     {'A': (X1, ARRIBA), 'B': (X1, ABAJO), 'C': (X2, ARRIBA), 'D': (X2, ABAJO)},
     [('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D')]),
]

ancho, alto = PANEL * len(PANELES), 222
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" '
     'font-family="system-ui, -apple-system, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif">',
     '<defs><marker id="punta" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" '
     f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GRIS}"/></marker></defs>']
for i, (titulo, rel, cajas, flechas) in enumerate(PANELES):
    x0 = i * PANEL
    cx = x0 + (X1 + X2 + W) / 2
    s.append(f'<text x="{cx}" y="28" text-anchor="middle" font-size="15" font-weight="600" fill="{TINTA}">{titulo}</text>')
    s.append(f'<text x="{cx}" y="48" text-anchor="middle" font-size="12.5" fill="{SUAVE}">{rel}</text>')
    if i:
        s.append(f'<line x1="{x0}" y1="14" x2="{x0}" y2="{alto - 14}" stroke="#e2e0da" stroke-width="1"/>')
    for o, d in flechas:
        (xo, yo), (xd, yd) = cajas[o], cajas[d]
        s.append(f'<line x1="{x0 + xo + W}" y1="{yo}" x2="{x0 + xd}" y2="{yd}" stroke="{GRIS}" '
                 'stroke-width="1.6" marker-end="url(#punta)"/>')
    for letra, (xc, yc) in cajas.items():
        s.append(f'<rect x="{x0 + xc}" y="{yc - H / 2}" width="{W}" height="{H}" rx="5" fill="#ffffff" '
                 f'stroke="{GRIS}" stroke-width="1.6"/>')
        s.append(f'<text x="{x0 + xc + W / 2}" y="{yc + 6}" text-anchor="middle" font-size="17" '
                 f'font-weight="700" fill="{TINTA}">{letra}</text>')
s.append('</svg>')

with open('03-prelaciones.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(s) + '\n')
print('03-prelaciones.svg')
