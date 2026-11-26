"""Figura del capítulo 4: los tipos de prelación del capítulo 3, dibujados en una red PERT.

Fragmentos de red, con flechas abiertas en los extremos: lineal, convergente, divergente y
convergente-divergente no necesitan ficticias; la convergente-divergente incompleta (A y B preceden
a C, y solo B precede a D) necesita una. Uso, desde figuras/: python3 04-prelaciones-pert.py
→  04-prelaciones-pert.svg
"""
from pertsvg import panel, documento

W = 285          # ancho de cada panel
H = 240          # alto de cada fila
ARR, MED, ABA = 95, 135, 175   # alturas de las flechas dentro del panel

PANELES = [
    ('Lineal', 'A → B',
     {'e': (142, MED, '')},
     [('A', (40, MED), 'e', False), ('B', 'e', (244, MED), False)], None),
    ('Convergente', 'A → C · B → C',
     {'e': (152, MED, '')},
     [('A', (42, ARR), 'e', False), ('B', (42, ABA), 'e', False), ('C', 'e', (250, MED), False)], None),
    ('Divergente', 'A → B · A → C',
     {'e': (132, MED, '')},
     [('A', (34, MED), 'e', False), ('B', 'e', (242, ARR), False), ('C', 'e', (242, ABA), False)], None),
    ('Convergente-divergente', 'A y B → C y D',
     {'e': (142, MED, '')},
     [('A', (42, ARR), 'e', False), ('B', (42, ABA), 'e', False), ('C', 'e', (242, ARR), False), ('D', 'e', (242, ABA), False)],
     'Sin ficticias: un solo suceso'),
    ('Convergente-divergente incompleta', 'A y B → C · B → D',
     {'a': (142, ARR, ''), 'b': (142, ABA, '')},
     [('A', (42, ARR), 'a', False), ('B', (42, ABA), 'b', False), ('F1', 'b', 'a', True),
      ('C', 'a', (242, ARR), False), ('D', 'b', (242, ABA), False)],
     'Hace falta una ficticia'),
]

cuerpo, seps = [], []
for i, (titulo, sub, sucesos, flechas, nota) in enumerate(PANELES):
    fila, col = divmod(i, 3)
    x0 = col * W + (W / 2 if fila == 1 else 0)      # la segunda fila, centrada
    y0 = fila * H
    cuerpo += panel(x0, y0, W, titulo, sub, sucesos, flechas, nota)
    if col:
        seps.append((x0, y0 + 14, x0, y0 + H - 14))
seps.append((40, H, 3 * W - 40, H))

with open('04-prelaciones-pert.svg', 'w', encoding='utf-8') as f:
    f.write(documento(3 * W, 2 * H, cuerpo, seps))
print('04-prelaciones-pert.svg')
