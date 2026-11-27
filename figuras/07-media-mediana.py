"""Figura del capítulo 7: la beta-PERT de la actividad F de Mecánicas del Sureste con tres tiempos (a 2, m 3, b 9),
con la más probable (moda), la mediana y la media de examen, y el área hasta la más probable.

Las cifras se comprueban con js/core/threept.js del portal (b42bbfc): media 23/6 = 3,83, P(F ≤ 3) = 0,281,
P(F ≤ 3,83) = 0,560 y mediana 3,64. Se integra aquí la densidad (regla de Simpson) para no depender de SciPy.
Se escribe el SVG a mano para que el texto quede como texto y el archivo no cambie entre ejecuciones.
Uso, desde figuras/: python3 07-media-mediana.py  →  07-media-mediana.svg
"""
from math import lgamma, log, exp

A, M, B = 2, 3, 9
AL = 1 + 4 * (M - A) / (B - A)          # beta-PERT
BE = 1 + 4 * (B - M) / (B - A)
LB = lgamma(AL) + lgamma(BE) - lgamma(AL + BE)
MEDIA = (A + 4 * M + B) / 6


def pdf(x):
    if x <= A or x >= B:
        return 0.0
    t = (x - A) / (B - A)
    return exp((AL - 1) * log(t) + (BE - 1) * log(1 - t) - LB) / (B - A)


def cdf(x, n=4000):
    if x <= A:
        return 0.0
    h = (x - A) / n
    s = pdf(A) + pdf(x) + sum((4 if k % 2 else 2) * pdf(A + k * h) for k in range(1, n))
    return s * h / 3


def cuantil(p):
    lo, hi = A, B
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cdf(mid, 2000) < p else (lo, mid)
    return (lo + hi) / 2


P_M, P_MEDIA, MEDIANA = cdf(M), cdf(MEDIA), cuantil(0.5)
assert abs(P_M - 0.281) < 0.001 and abs(P_MEDIA - 0.560) < 0.001 and abs(MEDIANA - 3.64) < 0.005, (P_M, P_MEDIA, MEDIANA)

AZUL, TINTA, SUAVE, SOMBRA = '#1f5f8b', '#222222', '#6b6862', '#d6e4ee'
FUENTE = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
ANCHO, ALTO = 720, 330
X0, X1, Y0, Y1 = 60, 690, 270, 50           # caja del gráfico (Y0 abajo)
YMAX = max(pdf(A + k * (B - A) / 1000) for k in range(1, 1000)) * 1.08
sx = lambda x: X0 + (x - A) / (B - A) * (X1 - X0)
sy = lambda y: Y0 - y / YMAX * (Y0 - Y1)
f2 = lambda v: f'{v:.2f}'.replace('.', ',')

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" width="{ANCHO}" height="{ALTO}" '
     f'font-family="{FUENTE}">']


def texto(x, y, t, tam=14, peso=400, color=TINTA, ancla='middle'):
    s.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ancla}" font-size="{tam}" font-weight="{peso}" '
             f'fill="{color}">{t}</text>')


# área hasta la más probable
pts = [(A + k * (M - A) / 200) for k in range(201)]
area = ' '.join(f'{sx(x):.1f},{sy(pdf(x)):.1f}' for x in pts)
s.append(f'<polygon points="{sx(A):.1f},{Y0} {area} {sx(M):.1f},{Y0}" fill="{SOMBRA}"/>')
# curva
pts = [A + k * (B - A) / 600 for k in range(601)]
s.append('<polyline fill="none" stroke="%s" stroke-width="2.4" points="%s"/>'
         % (AZUL, ' '.join(f'{sx(x):.1f},{sy(pdf(x)):.1f}' for x in pts)))
# eje
s.append(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{SUAVE}" stroke-width="1"/>')
for d in range(A, B + 1):
    s.append(f'<line x1="{sx(d):.1f}" y1="{Y0}" x2="{sx(d):.1f}" y2="{Y0 + 5}" stroke="{SUAVE}" stroke-width="1"/>')
    texto(sx(d), Y0 + 21, d, 13, 400, SUAVE)
texto((X0 + X1) / 2, Y0 + 45, 'duración de F (días)', 13, 400, SUAVE)
# marcas: más probable, mediana y media
for x, nombre, dy, trazo in ((M, f'más probable, {M}', 0, '0'), (MEDIANA, f'mediana, {f2(MEDIANA)}', 20, '5 4'),
                             (MEDIA, f'media, {f2(MEDIA)}', 40, '0')):
    s.append(f'<line x1="{sx(x):.1f}" y1="{Y0}" x2="{sx(x):.1f}" y2="{Y1 - 8 + dy:.1f}" stroke="{TINTA}" '
             f'stroke-width="1.4" stroke-dasharray="{trazo}"/>')
    texto(sx(x) + 6, Y1 - 12 + dy, nombre, 13, 600 if x == MEDIA else 400, TINTA, 'start')
texto(sx(2.62), Y0 - 18, f'{round(P_M * 100)} %', 15, 700, AZUL)
texto(sx(6.6), 120, f'P(F ≤ 3) = {f2(P_M)}', 13, 400, TINTA, 'start')
texto(sx(6.6), 140, f'P(F ≤ media) = {f2(P_MEDIA)}', 13, 400, TINTA, 'start')
texto(sx(6.6), 160, 'P(F ≤ mediana) = 0,50', 13, 400, TINTA, 'start')
s.append('</svg>')
with open('07-media-mediana.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(s) + '\n')
print('07-media-mediana.svg', f2(P_M), f2(P_MEDIA), f2(MEDIANA))
