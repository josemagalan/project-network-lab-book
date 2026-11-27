"""Figura del capítulo 10: diagrama de Gantt de Electrona a fechas tempranas, con la holgura total.

Cada barra va del comienzo temprano al fin temprano de la actividad; las críticas van en rojo, como en el portal y, a la
derecha de las demás, un rectángulo de trazos marca su holgura total (hasta el fin tardío). Fechas del
taller del portal con la tabla de Electrona (enunciado ej5 de «Del enunciado a la tabla»), comprobadas
aquí con una pasada hacia delante y otra hacia atrás. Uso, desde figuras/: python3 10-gantt.py → 10-gantt.svg
"""
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['svg.hashsalt'] = 'pnl-10-gantt'
plt.rcParams['font.family'] = 'sans-serif'

# (actividad, nombre, duración, predecesoras) de Electrona
TABLA = [('A', 'Materiales de X e Y', 3, ''), ('B', 'Puesta a punto', 1, ''), ('C', 'Materiales de Z', 2, ''),
         ('D', 'Fabricar Y', 7, 'AB'), ('E', 'Fabricar Z', 5, 'BC'), ('F', 'Fabricar X', 6, 'AB'),
         ('G', 'Transportar X', 1, 'F'), ('H', 'Ensamblar YZ', 2, 'DE'), ('I', 'Transportar YZ', 1, 'H'),
         ('J', 'Ensamblar XYZ', 3, 'GI'), ('K', 'Envasar', 1, 'J')]
dur = {a: d for a, _, d, _ in TABLA}
pred = {a: list(p) for a, _, _, p in TABLA}
succ = {a: [b for b, _, _, p in TABLA if a in p] for a in dur}
es = {}
for a, _, _, _ in TABLA:
    es[a] = max((es[p] + dur[p] for p in pred[a]), default=0)
T = max(es[a] + dur[a] for a in dur)
lf = {}
for a, _, _, _ in reversed(TABLA):
    lf[a] = min((lf[s] - dur[s] for s in succ[a]), default=T)
tf = {a: lf[a] - es[a] - dur[a] for a in dur}
assert T == 17
assert es == {'A': 0, 'B': 0, 'C': 0, 'D': 3, 'E': 2, 'F': 3, 'G': 9, 'H': 10, 'I': 12, 'J': 13, 'K': 16}
assert tf == {'A': 0, 'B': 2, 'C': 3, 'D': 0, 'E': 3, 'F': 3, 'G': 3, 'H': 0, 'I': 0, 'J': 0, 'K': 0}

CRIT, CRIT_BORDE = '#a3271d', '#6e1a13'     # rojo del portal: camino crítico
NORMAL, NORMAL_BORDE = '#9fb8d6', '#1f4e79'
fig, ax = plt.subplots(figsize=(7.6, 4.2))
for i, (a, nombre, d, _) in enumerate(TABLA):
    critica = tf[a] == 0
    ax.barh(i, d, left=es[a], height=0.6, color=CRIT if critica else NORMAL,
            edgecolor=CRIT_BORDE if critica else NORMAL_BORDE, linewidth=0.8)
    if tf[a]:
        ax.add_patch(Rectangle((es[a] + d, i - 0.3), tf[a], 0.6, fill=False, edgecolor=NORMAL_BORDE,
                               linewidth=0.8, linestyle=(0, (3, 2))))
ax.set_yticks(range(len(TABLA)), [f'{a}  {n}' for a, n, _, _ in TABLA])
ax.invert_yaxis()
ax.set_xlim(0, T)
ax.set_xticks(range(0, T + 1))
ax.set_xlabel('Día')
ax.grid(axis='x', color='#dddddd', linewidth=0.6)
ax.set_axisbelow(True)
for lado in ('top', 'right'):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
fig.savefig('10-gantt.svg', metadata={'Date': None})
print('10-gantt.svg')
