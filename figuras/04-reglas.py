"""Figura del capítulo 4: las tres reglas de los conjuntos, en miniatura.

Iguales (ficticia de unicidad, detrás de la actividad que va después en orden alfabético, como en la
ruta guiada del portal), contenidos (ficticia del suceso del conjunto mayor al del menor) y
compartidos (un suceso para la parte común, con una ficticia desde cada uno). Fragmentos con flechas
abiertas en los extremos. Uso, desde figuras/: python3 04-reglas.py  →  04-reglas.svg
"""
from pertsvg import panel, documento

W, H = 290, 250

PANELES = [
    ('Iguales', 'D y E: precedente C, posterior H',
     {'3': (95, 135, '3'), '4': (170, 95, '4'), '5': (220, 135, '5')},
     [('C', (22, 135), '3', False), ('D', '3', '5', False), ('E', '3', '4', False), ('F1', '4', '5', True),
      ('H', '5', (282, 135), False)],
     'Ficticia de unicidad'),
    ('Contenidos', 'post(E) = {A, B, C} ⊃ post(F) = {B, C}',
     {'3': (130, 95, '3'), '4': (130, 175, '4')},
     [('E', (30, 95), '3', False), ('F', (30, 175), '4', False), ('F1', '3', '4', True),
      ('A', '3', (250, 95), False), ('B', '4', (245, 145), False), ('C', '4', (245, 205), False)],
     'Del conjunto mayor al menor'),
    ('Compartidos', 'post(E) = {A, B, C} · post(F) = {B, C, D}',
     {'3': (110, 90, '3'), '4': (110, 185, '4'), '5': (185, 137, '5')},
     [('E', (25, 90), '3', False), ('F', (25, 185), '4', False), ('A', '3', (220, 75), False), ('D', '4', (220, 200), False),
      ('F1', '3', '5', True), ('F2', '4', '5', True), ('B', '5', (282, 110), False), ('C', '5', (282, 160), False)],
     'Un suceso para la parte común {B, C}'),
]

cuerpo, seps = [], []
for i, (titulo, sub, sucesos, flechas, nota) in enumerate(PANELES):
    x0 = i * W
    cuerpo += panel(x0, 0, W, titulo, sub, sucesos, flechas, nota)
    if i:
        seps.append((x0, 14, x0, H - 14))

with open('04-reglas.svg', 'w', encoding='utf-8') as f:
    f.write(documento(3 * W, H - 10, cuerpo, seps))
print('04-reglas.svg')
