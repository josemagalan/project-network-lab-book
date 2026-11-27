"""Figuras del capítulo 9: el problema de la diagonal de la Primitiva.

- 09-boleto.svg: un bloque del boleto (los números del 1 al 49 en una cuadrícula de 10 filas y 5 columnas: el número n
  está en la fila n mod 10 y la columna n div 10; la casilla de la fila 0 y la columna 0 está vacía), con una diagonal
  en cada sentido: 11, 22 y 33 (↘: n, n + 11, n + 22) y 27, 36 y 45 (↗: n, n + 9, n + 18).
- 09-loteria.svg: la estimación por Montecarlo de dos probabilidades a medida que se añaden sorteos (escala
  logarítmica), con su banda al 95 % y el valor exacto: «tres de los seis números forman una diagonal de tres casillas,
  en un sentido o en el otro» y, como contraste, «hay al menos dos números consecutivos».

Los valores exactos se calculan sin simular: la diagonal, por inclusión y exclusión sobre las 47 diagonales posibles
(680 371 de las 13 983 816 combinaciones, 0,0487; coincide con la enumeración completa); los consecutivos, con
1 − C(44, 6)/C(49, 6) = 0,4952. La simulación usa random.Random(2026), así que el archivo no cambia entre ejecuciones.
Se escribe el SVG a mano para que el texto quede como texto, como en 08-sumas.py.
Uso, desde figuras/: python3 09-loteria.py  →  09-boleto.svg y 09-loteria.svg
"""
import random
from math import comb, log10, sqrt

TOTAL = comb(49, 6)


def pos(n):
    return n % 10, n // 10                        # fila, columna del boleto


def diagonales():
    out = []
    for n in range(1, 50):
        f, c = pos(n)
        if f <= 7 and c <= 2:                     # ↘: n, n + 11, n + 22
            out.append((n, n + 11, n + 22))
        if f >= 2 and c <= 2:                     # ↗ (o ↙): n, n + 9, n + 18
            out.append((n, n + 9, n + 18))
    return out


DIAG = diagonales()
assert len(DIAG) == 47
for t in DIAG:                                   # las tres casillas, en filas y columnas seguidas
    (f0, c0), (f1, c1), (f2, c2) = map(pos, t)
    assert c1 == c0 + 1 and c2 == c0 + 2 and abs(f1 - f0) == 1 and f2 - f1 == f1 - f0 and max(t) <= 49


def exacta_diagonal():
    # inclusión y exclusión: cada conjunto de diagonales cuya unión cabe en 6 números aporta C(49 − u, 6 − u)
    tri = [frozenset(t) for t in DIAG]
    total = 0

    def rec(desde, union, k):
        nonlocal total
        for i in range(desde, len(tri)):
            u = union | tri[i]
            if len(u) <= 6:
                total += (-1) ** k * comb(49 - len(u), 6 - len(u))
                rec(i + 1, u, k + 1)

    rec(0, frozenset(), 0)
    return total


N_DIAG = exacta_diagonal()
assert N_DIAG == 680371, N_DIAG
P_DIAG = N_DIAG / TOTAL
P_CONS = 1 - comb(44, 6) / TOTAL
assert abs(P_CONS - 0.4952) < 5e-5

TRIPLES = [set(t) for t in DIAG]
rng = random.Random(2026)
N_MAX = 10 ** 6
PUNTOS = sorted({round(10 ** (1 + 5 * k / 50)) for k in range(51)})
serie = {'diag': [], 'cons': []}
cd = cc = 0
for i in range(1, N_MAX + 1):
    s = rng.sample(range(1, 50), 6)
    ss = set(s)
    if any(t <= ss for t in TRIPLES):
        cd += 1
    o = sorted(s)
    if any(o[j + 1] == o[j] + 1 for j in range(5)):
        cc += 1
    if i in PUNTOS:
        serie['diag'].append((i, cd / i))
        serie['cons'].append((i, cc / i))
FINAL = {k: v[-1][1] for k, v in serie.items()}

AZUL, NARANJA, TINTA, SUAVE, BANDA, REJA = '#1f5f8b', '#b4561d', '#222222', '#6b6862', '#dbe7f0', '#e3e0da'
FUENTE = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
f3 = lambda v: f'{v:.3f}'.replace('.', ',')
f4 = lambda v: f'{v:.4f}'.replace('.', ',')
miles = lambda n: f'{n:,}'.replace(',', ' ')


def svg(ancho, alto):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" '
            f'font-family="{FUENTE}">']


def texto(s, x, y, t, tam=13, peso=400, color=TINTA, ancla='middle'):
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ancla}" font-size="{tam}" font-weight="{peso}" '
             f'fill="{color}">{t}</text>')


# ---------- el boleto ----------
LADO, X0, Y0 = 46, 20, 20
s = svg(X0 * 2 + 5 * LADO, Y0 * 2 + 10 * LADO)
marca = {11: AZUL, 22: AZUL, 33: AZUL, 27: NARANJA, 36: NARANJA, 45: NARANJA}
for f in range(10):
    for c in range(5):
        n = 10 * c + f
        x, y = X0 + c * LADO, Y0 + f * LADO
        if n == 0:
            continue
        color = marca.get(n)
        relleno = color if color else '#ffffff'
        s.append(f'<rect x="{x + 3}" y="{y + 3}" width="{LADO - 6}" height="{LADO - 6}" rx="4" fill="{relleno}" '
                 f'stroke="{color or "#c9c4bb"}" stroke-width="1.2"/>')
        texto(s, x + LADO / 2, y + LADO / 2 + 5, str(n), 15, 700 if color else 400, '#ffffff' if color else TINTA)
s.append('</svg>')
with open('09-boleto.svg', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(s) + '\n')

# ---------- la convergencia ----------
ANCHO, ALTO = 940, 380
PW, PH, IZQ, ARR, GX = 360, 250, 70, 50, 90
s = svg(ANCHO, ALTO)
PANELES = [
    ('Tres números en diagonal', 'diag', P_DIAG, 0.0, 0.15, (0, 0.05, 0.10, 0.15)),
    ('Dos números consecutivos', 'cons', P_CONS, 0.3, 0.7, (0.3, 0.4, 0.5, 0.6, 0.7)),
]
lx = lambda n, x0: x0 + (log10(n) - 1) / 5 * PW
for k, (titulo, clave, p, ylo, yhi, marcas_y) in enumerate(PANELES):
    x0 = IZQ + k * (PW + GX)
    sy = lambda v: ARR + PH - (min(max(v, ylo), yhi) - ylo) / (yhi - ylo) * PH
    texto(s, x0 + PW / 2, ARR - 22, titulo, 14, 700)
    s.append(f'<rect x="{x0}" y="{ARR}" width="{PW}" height="{PH}" fill="none" stroke="{REJA}"/>')
    # banda al 95 % alrededor del valor exacto
    arriba = [(n, p + 1.96 * sqrt(p * (1 - p) / n)) for n, _ in serie[clave]]
    abajo = [(n, p - 1.96 * sqrt(p * (1 - p) / n)) for n, _ in serie[clave]]
    pts = ' '.join(f'{lx(n, x0):.1f},{sy(v):.1f}' for n, v in arriba + abajo[::-1])
    s.append(f'<polygon points="{pts}" fill="{BANDA}"/>')
    s.append(f'<line x1="{x0}" y1="{sy(p):.1f}" x2="{x0 + PW}" y2="{sy(p):.1f}" stroke="{NARANJA}" stroke-width="1.6" '
             f'stroke-dasharray="5 4"/>')
    pts = ' '.join(f'{lx(n, x0):.1f},{sy(v):.1f}' for n, v in serie[clave])
    s.append(f'<polyline fill="none" stroke="{AZUL}" stroke-width="2" points="{pts}"/>')
    for e in range(1, 7):
        x = lx(10 ** e, x0)
        s.append(f'<line x1="{x:.1f}" y1="{ARR + PH}" x2="{x:.1f}" y2="{ARR + PH + 5}" stroke="{SUAVE}"/>')
        texto(s, x, ARR + PH + 20, miles(10 ** e), 11, 400, SUAVE)
    for v in marcas_y:
        s.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + PW}" y2="{sy(v):.1f}" stroke="{REJA}"/>')
        texto(s, x0 - 8, sy(v) + 4, f'{v:.2f}'.replace('.', ','), 11, 400, SUAVE, 'end')
    texto(s, x0 + PW - 6, sy(p) - 8, f'exacta {f4(p)}', 12, 400, NARANJA, 'end')
    texto(s, x0 + PW / 2, ARR + PH + 40, 'sorteos simulados (escala logarítmica)', 12, 400, SUAVE)
yl = ALTO - 14
s.append(f'<line x1="{IZQ}" y1="{yl - 4}" x2="{IZQ + 28}" y2="{yl - 4}" stroke="{AZUL}" stroke-width="2"/>')
texto(s, IZQ + 34, yl, 'estimación (proporción de sorteos en que pasa)', 12, 400, TINTA, 'start')
s.append(f'<rect x="{IZQ + 340}" y="{yl - 11}" width="28" height="12" fill="{BANDA}"/>')
texto(s, IZQ + 374, yl, 'banda al 95 % alrededor del valor exacto', 12, 400, TINTA, 'start')
s.append('</svg>')
with open('09-loteria.svg', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(s) + '\n')

for clave, p in (('diag', P_DIAG), ('cons', P_CONS)):
    marcas = {n: v for n, v in serie[clave] if n in (10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6)}
    print(clave, 'exacta', f4(p), ' '.join(f'{miles(n)}: {f4(v)}' for n, v in marcas.items()))
