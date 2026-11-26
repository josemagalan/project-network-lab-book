"""Figura del capítulo 4: las tres reglas de los conjuntos, en miniatura.

Arriba, el trozo de red; abajo, el trozo de la tabla de precedencias en el que se ve la regla, con lo
que comparten las columnas en rojo, y la condición con notación de conjuntos, como en las transparencias de clase de José Manuel Galán.
Iguales (ficticia de unicidad, detrás de la actividad que va después en orden alfabético, como en la
ruta guiada del portal; es una de las cuatro formas posibles), contenidos (ficticia del suceso del
conjunto mayor al del menor) y compartidos (un suceso para la parte común, con una ficticia desde
cada uno). Uso, desde figuras/: python3 04-reglas.py  →  04-reglas.svg
"""
from pertsvg import panel, tabla, documento

W, H = 290, 350
Y_TABLA = 238
Y_FORMAL = 340

R = lambda *xs: [(x, True) for x in xs]     # celdas resaltadas
N = lambda *xs: [(x, False) for x in xs]    # celdas normales

PANELES = [
    ('Iguales', 'mismas precedentes y mismas posteriores',
     {'3': (95, 135, '3'), '4': (170, 95, '4'), '5': (220, 135, '5')},
     [('C', (22, 135), '3', False), ('D', '3', '5', False), ('E', '3', '4', False), ('F1', '4', '5', True),
      ('H', '5', (282, 135), False)],
     'Ficticia de unicidad',
     [('Precedentes', [R('C'), R('C')], False), ('Actividad', [N('D'), N('E')], True), ('Posteriores', [R('H'), R('H')], False)],
     'pre(D) = pre(E) · post(D) = post(E)'),
    ('Contenidos', 'las posteriores de F, dentro de las de E',
     {'3': (130, 95, '3'), '4': (130, 175, '4')},
     [('E', (30, 95), '3', False), ('F', (30, 175), '4', False), ('F1', '3', '4', True),
      ('A', '3', (250, 95), False), ('B', '4', (245, 145), False), ('C', '4', (245, 205), False)],
     'Del conjunto mayor al menor',
     [('Actividad', [N('E'), N('F')], True), ('Posteriores', [N('A') + R('B', 'C'), R('B', 'C')], False)],
     'post(F) = {B, C} ⊂ post(E) = {A, B, C}'),
    ('Compartidos', 'E y F comparten parte de sus posteriores',
     {'3': (110, 90, '3'), '4': (110, 185, '4'), '5': (185, 137, '5')},
     [('E', (25, 90), '3', False), ('F', (25, 185), '4', False), ('A', '3', (220, 75), False), ('D', '4', (220, 200), False),
      ('F1', '3', '5', True), ('F2', '4', '5', True), ('B', '5', (282, 110), False), ('C', '5', (282, 160), False)],
     'Un suceso para la parte común',
     [('Actividad', [N('E'), N('F')], True), ('Posteriores', [N('A') + R('B', 'C'), N('D') + R('B', 'C')], False)],
     'post(E) ∩ post(F) = {B, C}, sin inclusión'),
]

cuerpo, seps = [], []
for i, (titulo, sub, sucesos, flechas, nota, filas, formal) in enumerate(PANELES):
    x0 = i * W
    cuerpo += panel(x0, 0, W, titulo, sub, sucesos, flechas, nota)
    _, ancho = tabla(0, 0, filas)                  # medir para centrar
    piezas, _ = tabla(x0 + (W - ancho) / 2, Y_TABLA, filas)
    cuerpo += piezas
    cuerpo.append(f'<text x="{x0 + W / 2}" y="{Y_FORMAL}" text-anchor="middle" font-size="13" fill="#222222">{formal}</text>')
    if i:
        seps.append((x0, 14, x0, H - 14))

with open('04-reglas.svg', 'w', encoding='utf-8') as f:
    f.write(documento(3 * W, H, cuerpo, seps))
print('04-reglas.svg')
