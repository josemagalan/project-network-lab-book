"""Figura del capítulo 1: diagrama de Gantt de barras de Mecánicas del Sureste, sin enlaces.

Cada barra va del comienzo temprano al fin temprano de la actividad (los del portal, ruta guiada,
ejemplo ej6). No marca el camino crítico ni las dependencias: es el Gantt «de barras» de la
sección 1.2. Uso, desde figuras/: python3 01-gantt.py  →  01-gantt.svg
"""
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt

plt.rcParams['svg.fonttype'] = 'none'        # texto como texto, no como trazos
plt.rcParams['svg.hashsalt'] = 'pnl-01-gantt'  # identificadores estables entre ejecuciones
plt.rcParams['font.family'] = 'sans-serif'

# (actividad, duración, sucesoras) del ejemplo ej6 del portal
TABLA = [('A', 2, 'E'), ('B', 3, 'EFG'), ('C', 2, 'G'), ('D', 8, 'K'), ('E', 4, 'HI'), ('F', 3, 'HI'),
         ('G', 2, 'I'), ('H', 1, 'K'), ('I', 2, 'J'), ('J', 3, 'K'), ('K', 1, '')]
dur = {a: d for a, d, _ in TABLA}
pred = {a: [b for b, _, s in TABLA if a in s] for a, _, _ in TABLA}
es = {}
for a, _, _ in TABLA:                       # la tabla ya está en orden topológico
    es[a] = max((es[p] + dur[p] for p in pred[a]), default=0)
assert es == {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 3, 'F': 3, 'G': 3, 'H': 7, 'I': 7, 'J': 9, 'K': 12}
assert max(es[a] + dur[a] for a in dur) == 13

fig, ax = plt.subplots(figsize=(7.2, 3.6))
for i, (a, d, _) in enumerate(TABLA):
    ax.barh(i, d, left=es[a], height=0.6, color='#9fb8d6', edgecolor='#1f4e79', linewidth=0.8)
ax.set_yticks(range(len(TABLA)), [a for a, _, _ in TABLA])
ax.invert_yaxis()
ax.set_xlim(0, 13)
ax.set_xticks(range(0, 14))
ax.set_xlabel('Día')
ax.grid(axis='x', color='#dddddd', linewidth=0.6)
ax.set_axisbelow(True)
for lado in ('top', 'right'):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
fig.savefig('01-gantt.svg', metadata={'Date': None})
print('01-gantt.svg')
