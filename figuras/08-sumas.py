"""Figura del capítulo 8: el teorema central del límite a la vista. Sumas de 1, 2, 3 y 10 copias independientes de
tres duraciones muy distintas, cada una con la normal de su misma media y varianza encima:

- la uniforme entre 0 y 12;
- una de dos valores, 6 o 10 semanas al 50 % (Klastorin, 2004, pp. 200-201);
- la beta-PERT (0, 0, 12), la del caso «Pocas actividades» del portal: una beta(1, 5) escalada, con la cola a la derecha.

Las densidades de las sumas se calculan por convolución en una rejilla (las de dos valores, exactas: binomial), sin
simular y sin depender de NumPy ni de SciPy. Comprueba la media y la varianza de cada suma, y la asimetría de la
beta-PERT: √(7/5) ≈ 1,18 con una actividad, 0,68 con tres y 0,37 con diez (se divide por √n).
Se escribe el SVG a mano para que el texto quede como texto y el archivo no cambie entre ejecuciones.
Uso, desde figuras/: python3 08-sumas.py  →  08-sumas.svg
"""
from math import comb, exp, pi, sqrt

H = 0.05                       # paso de la rejilla (semanas)
NS = (1, 2, 3, 10)


def rejilla(pdf, lo, hi):
    n = round((hi - lo) / H)
    return [pdf(lo + (k + 0.5) * H) * H for k in range(n)]    # masa de cada celda


def convolucion(p, q):
    out = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return out


def momentos(masas, origen):
    # la celda k de una suma de n copias va de origen + k·H a origen + (k + 1)·H; su centro, a mitad
    xs = [origen + (k + 0.5) * H for k in range(len(masas))]
    tot = sum(masas)
    m = sum(x * w for x, w in zip(xs, masas)) / tot
    v = sum((x - m) ** 2 * w for x, w in zip(xs, masas)) / tot
    g = sum((x - m) ** 3 * w for x, w in zip(xs, masas)) / tot / v ** 1.5
    return m, v, g


uniforme = rejilla(lambda x: 1 / 12, 0, 12)
beta = rejilla(lambda x: 5 * (1 - x / 12) ** 4 / 12, 0, 12)   # beta(1, 5) en [0, 12]: α = 1, β = 5 (beta-PERT, m = a)


def sumas(base):
    out, acc = {}, base
    for n in range(1, max(NS) + 1):
        if n > 1:
            acc = convolucion(acc, base)
        if n in NS:
            # la suma de n celdas centradas desplaza el origen media celda por sumando: se recoloca
            out[n] = (acc, n * 0.5 * H - 0.5 * H)
    return out


SUMAS = {'uniforme': sumas(uniforme), 'beta': sumas(beta)}
# comprobaciones: media 6n y varianza 12n (uniforme); media 2n y varianza 20n/7 (beta(1, 5)·12)
for clave, (mu1, v1) in (('uniforme', (6, 12)), ('beta', (2, 20 / 7))):
    for n in NS:
        masas, desplaz = SUMAS[clave][n]
        m, v, g = momentos(masas, desplaz)
        assert abs(m - n * mu1) < 0.01 and abs(v - n * v1) / (n * v1) < 0.01, (clave, n, m, v)
        if clave == 'beta':
            assert abs(g - sqrt(7 / 5) / sqrt(n)) < 0.01, (n, g)
ASIM = {n: momentos(*SUMAS['beta'][n])[2] for n in NS}


def dos_valores(n):
    # 6 o 10 al 50 %: la suma vale 6n + 4k con probabilidad C(n, k)/2ⁿ; media 8n, varianza 4n
    return [(6 * n + 4 * k, comb(n, k) / 2 ** n) for k in range(n + 1)]


assert [p for _, p in dos_valores(2)] == [0.25, 0.5, 0.25]

AZUL, NARANJA, TINTA, SUAVE, BARRA = '#1f5f8b', '#b4561d', '#222222', '#6b6862', '#9dbcd4'
FUENTE = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
ANCHO, ALTO = 900, 588
IZQ, ARR = 150, 46            # margen para el nombre de cada fila y para los títulos de columna
CW, CH = 180, 140             # caja de cada panel
GX, GY = 10, 32
f2 = lambda v: f'{v:.2f}'.replace('.', ',')

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" width="{ANCHO}" height="{ALTO}" '
     f'font-family="{FUENTE}">']


def texto(x, y, t, tam=13, peso=400, color=TINTA, ancla='middle'):
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ancla}" font-size="{tam}" font-weight="{peso}" '
             f'fill="{color}">{t}</text>')


def normal(x, m, v):
    return exp(-(x - m) ** 2 / (2 * v)) / sqrt(2 * pi * v)


FILAS = [
    ('Uniforme', 'entre 0 y 12', 'uniforme', 6, 12),
    ('Dos valores', '6 o 10, al 50 %', 'dos', 8, 4),
    ('Beta-PERT', '(0, 0, 12)', 'beta', 2, 20 / 7),
]
for c, n in enumerate(NS):
    texto(IZQ + c * (CW + GX) + CW / 2, ARR - 18, '1 actividad' if n == 1 else f'suma de {n}', 14, 700)
for r, (nombre, detalle, clave, mu1, v1) in enumerate(FILAS):
    y0 = ARR + r * (CH + GY) + CH           # base del panel
    texto(IZQ - 14, y0 - CH / 2 - 4, nombre, 14, 700, TINTA, 'end')
    texto(IZQ - 14, y0 - CH / 2 + 14, detalle, 12, 400, SUAVE, 'end')
    for c, n in enumerate(NS):
        x0 = IZQ + c * (CW + GX)
        m, v = n * mu1, n * v1
        lo, hi = m - 4 * sqrt(v), m + 4 * sqrt(v)
        if clave != 'dos':
            lo = max(lo, 0)
        hi = min(hi, 12 * n) if clave != 'dos' else hi
        sx = lambda x: x0 + (x - lo) / (hi - lo) * CW
        # datos: densidad (por semana) en puntos
        if clave == 'dos':
            puntos = [(x, p / 4) for x, p in dos_valores(n)]   # separación 4: la densidad equivalente es p/4
            ymax = max(max(d for _, d in puntos), normal(m, m, v)) * 1.12
        else:
            masas, desplaz = SUMAS[clave][n]
            curva = [(desplaz + (k + 0.5) * H, w / H) for k, w in enumerate(masas)]
            curva = [(x, d) for x, d in curva if lo <= x <= hi]
            ymax = max(max(d for _, d in curva), normal(m, m, v)) * 1.12
        sy = lambda d: y0 - d / ymax * CH
        s.append(f'<rect x="{x0}" y="{y0 - CH}" width="{CW}" height="{CH}" fill="none" stroke="#e3e0da" stroke-width="1"/>')
        if clave == 'dos':
            ancho = max(2.0, min(14.0, 4 / (hi - lo) * CW * 0.55))
            for x, d in puntos:
                if lo <= x <= hi:
                    s.append(f'<rect x="{sx(x) - ancho / 2:.1f}" y="{sy(d):.1f}" width="{ancho:.1f}" '
                             f'height="{y0 - sy(d):.1f}" fill="{BARRA}"/>')
        else:
            pts = ' '.join(f'{sx(x):.1f},{sy(d):.1f}' for x, d in curva[::max(1, len(curva) // 240)])
            s.append(f'<polyline fill="none" stroke="{AZUL}" stroke-width="2.2" points="{pts}"/>')
        npts = ' '.join(f'{sx(lo + k * (hi - lo) / 160):.1f},{sy(normal(lo + k * (hi - lo) / 160, m, v)):.1f}'
                        for k in range(161))
        s.append(f'<polyline fill="none" stroke="{NARANJA}" stroke-width="1.6" stroke-dasharray="5 4" points="{npts}"/>')
        texto(x0 + 4, y0 + 15, f'{lo:.0f}', 11, 400, SUAVE, 'start')
        texto(x0 + CW - 4, y0 + 15, f'{hi:.0f}', 11, 400, SUAVE, 'end')
        if clave == 'beta':
            texto(x0 + CW - 6, y0 - CH + 16, f'asimetría {f2(ASIM[n])}', 11, 400, SUAVE, 'end')
# leyenda
yl = ALTO - 18
s.append(f'<line x1="{IZQ}" y1="{yl - 4}" x2="{IZQ + 28}" y2="{yl - 4}" stroke="{AZUL}" stroke-width="2.2"/>')
texto(IZQ + 34, yl, 'suma de duraciones independientes (las de dos valores, en barras)', 12, 400, TINTA, 'start')
s.append(f'<line x1="{IZQ + 470}" y1="{yl - 4}" x2="{IZQ + 498}" y2="{yl - 4}" stroke="{NARANJA}" stroke-width="1.6" '
         f'stroke-dasharray="5 4"/>')
texto(IZQ + 504, yl, 'normal de la misma media y varianza', 12, 400, TINTA, 'start')
s.append('</svg>')
with open('08-sumas.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(s) + '\n')
print('08-sumas.svg', ' '.join(f'n={n}: {f2(ASIM[n])}' for n in NS))
