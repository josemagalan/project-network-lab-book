"""Portada vectorial de «Proyectos a la vista» y adaptación horizontal.

Uso: python3 figuras/portada.py
Solo biblioteca estándar. Los SVG se escriben junto a este archivo.
Misma composición que la portada de «Evolución a la vista» (libro hermano de algoritmos genéticos), con el violeta
del Real Valladolid como color principal. Ilustración editorial original: la tabla, las redes, el Gantt y el
histograma son esquemáticos, no capturas del portal; la red sí es coherente (ver portada.md).
Contenido: CC BY 4.0; código: MIT (licencias del repositorio).
"""

from html import escape
from math import exp
from pathlib import Path


INK = "#2b1630"          # tinta oscura con un punto de violeta
MUTED = "#6a5d6c"
VIOLET = "#921b88"       # violeta del Real Valladolid (Pantone 248)
BLUE = "#1f63b0"         # el azul del recorrido básico del libro y del favicon
PALE_VIOLET = "#f3e6f1"
PALE_BLUE = "#e3ecf7"
PAPER = "#f7f5f2"
LINE = "#ddd5db"
TITLE = "Proyectos a la vista. Redes PERT, CPM y ROY en un laboratorio interactivo"
AUTHORS = [
    "José Manuel Galán", "Silvia Díaz-de la Fuente", "Virginia Ahedo",
    "María Pereda", "José Ignacio Santos",
]

# La red del panel: seis actividades con sus duraciones y predecesoras. Camino crítico A–C–E–F, de 12 días;
# B tiene 2 días de holgura total y D, 1. En la red PERT hace falta una ficticia (2 → 3) para que D espere a A y a B.
ACTS = [("A", 3, ""), ("B", 2, ""), ("C", 4, "A"), ("D", 5, "A, B"), ("E", 2, "C"), ("F", 3, "D, E")]
FECHAS = {"A": (0, 3), "B": (0, 2), "C": (3, 7), "D": (3, 8), "E": (7, 9), "F": (9, 12)}
HOLGURA = {"A": 0, "B": 2, "C": 0, "D": 1, "E": 0, "F": 0}
CRITICAS = {k for k, v in HOLGURA.items() if v == 0}


def comprobar_red():
    d = {a: dur for a, dur, _ in ACTS}
    pred = {a: [p.strip() for p in ps.split(",") if p.strip()] for a, _, ps in ACTS}
    es, ef = {}, {}
    for a, _, _ in ACTS:
        es[a] = max((ef[p] for p in pred[a]), default=0)
        ef[a] = es[a] + d[a]
    fin = max(ef.values())
    lf = {}
    for a, _, _ in reversed(ACTS):
        suc = [b for b in pred if a in pred[b]]
        lf[a] = min((lf[b] - d[b] for b in suc), default=fin)
    assert fin == 12
    for a in d:
        assert FECHAS[a] == (es[a], ef[a]), a
        assert HOLGURA[a] == lf[a] - ef[a], a


comprobar_red()


def text(x, y, value, size=24, fill=INK, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" {extra}>{escape(str(value))}</text>')


def rect(x, y, w, h, fill, radius=0, stroke="none", sw=1, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def line(x1, y1, x2, y2, color=LINE, width=2, extra=""):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" {extra}/>')


def path(d, color, width=2, fill="none", extra=""):
    return (f'<path d="{d}" stroke="{color}" stroke-width="{width}" '
            f'fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def circle(cx, cy, r, fill, stroke="none", sw=1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def label(x, y, value, fill=MUTED, size=17):
    return text(x, y, value, size, fill, 600, 'letter-spacing="2"')


def flecha(x1, y1, x2, y2, color, width=2.5, dash=False):
    """Segmento con punta de flecha en (x2, y2)."""
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    bx, by = x2 - 11 * ux, y2 - 11 * uy
    px, py = -uy * 5.5, ux * 5.5
    extra = 'stroke-dasharray="5 5"' if dash else ""
    return (line(x1, y1, bx, by, color, width, extra)
            + f'<path d="M {x2:.1f} {y2:.1f} L {bx + px:.1f} {by + py:.1f} L {bx - px:.1f} {by - py:.1f} Z" fill="{color}"/>')


def tabla(x, y):
    """Tabla de precedencias de la red (01 / DEFINE)."""
    out = [label(x, y, "ACT.", MUTED, 12), label(x + 64, y, "PRED.", MUTED, 12), label(x + 152, y, "D", MUTED, 12)]
    for i, (a, d, p) in enumerate(ACTS):
        yy = y + 24 + i * 40
        color = VIOLET if a in CRITICAS else BLUE
        out.append(rect(x, yy, 36, 30, color, 6))
        out.append(text(x + 18, yy + 22, a, 19, "#ffffff", 700, 'text-anchor="middle"'))
        out.append(text(x + 64, yy + 22, p or "—", 19, INK, 500))
        out.append(text(x + 166, yy + 22, d, 19, INK, 500, 'text-anchor="end"'))
    return "".join(out)


ROY = {"A": (302, 262), "B": (302, 352), "C": (412, 242), "D": (412, 352), "E": (522, 242), "F": (632, 302)}
ROY_ARCOS = [("A", "C"), ("A", "D"), ("B", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
NODO_W, NODO_H = 62, 46


def roy():
    out = []
    for a, b in ROY_ARCOS:
        (x1, y1), (x2, y2) = ROY[a], ROY[b]
        crit = a in CRITICAS and b in CRITICAS
        sx, sy = x1 + NODO_W, y1 + NODO_H / 2
        ex, ey = x2, y2 + NODO_H / 2
        out.append(flecha(sx, sy, ex - 2, ey, VIOLET if crit else "#9fb4cf", 3 if crit else 2))
    for a, (x, y) in ROY.items():
        d = dict((k, v) for k, v, _ in ACTS)[a]
        crit = a in CRITICAS
        out.append(rect(x, y, NODO_W, NODO_H, VIOLET if crit else "#ffffff", 8, VIOLET if crit else BLUE, 2.5))
        out.append(text(x + 21, y + 31, a, 23, "#ffffff" if crit else BLUE, 700, 'text-anchor="middle"'))
        out.append(line(x + 40, y + 9, x + 40, y + NODO_H - 9, "#ffffff" if crit else LINE, 1.5))
        out.append(text(x + 51, y + 30, d, 17, "#ffffff" if crit else INK, 500, 'text-anchor="middle"'))
    return "".join(out)


# Red PERT de la misma tabla: sucesos 1–6 y una ficticia 2 → 3.
PERT = {1: (748, 322), 2: (808, 258), 3: (808, 386), 4: (878, 258), 5: (928, 386), 6: (985, 322)}
PERT_ARCOS = [(1, 2, "A"), (1, 3, "B"), (2, 3, None), (2, 4, "C"), (3, 5, "D"), (4, 5, "E"), (5, 6, "F")]
R_SUCESO = 15


def pert():
    out = []
    for i, j, a in PERT_ARCOS:
        (x1, y1), (x2, y2) = PERT[i], PERT[j]
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5
        sx, sy = x1 + dx / n * R_SUCESO, y1 + dy / n * R_SUCESO
        ex, ey = x2 - dx / n * (R_SUCESO + 1), y2 - dy / n * (R_SUCESO + 1)
        crit = a in CRITICAS if a else False
        color = VIOLET if crit else ("#9fb4cf" if a else MUTED)
        out.append(flecha(sx, sy, ex, ey, color, 3 if crit else 2, dash=a is None))
        if a:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ox, oy = (-dy / n * 13, dx / n * 13)
            if (i, j) in ((1, 3), (3, 5), (5, 6)):
                ox, oy = -ox, -oy
            out.append(text(f"{mx + ox:.1f}", f"{my + oy + 6:.1f}", a, 16, VIOLET if crit else BLUE, 700,
                            'text-anchor="middle"'))
    for k, (x, y) in PERT.items():
        out.append(circle(x, y, R_SUCESO, "#ffffff", INK, 2))
        out.append(text(x, y + 6, k, 16, INK, 600, 'text-anchor="middle"'))
    return "".join(out)


def gantt(x, y):
    """Diagrama de Gantt de la red a fechas tempranas (03 / CALCULA)."""
    out = [text(x, y, "Calendario", 22, INK, 500)]
    escala = 256 / 12
    for t in (0, 3, 6, 9, 12):
        out.append(line(x + t * escala, y + 23, x + t * escala, y + 134, "#ece7eb", 1))
    out.extend([line(x, y + 23, x, y + 134, LINE, 1.5), line(x, y + 134, x + 256, y + 134, LINE, 1.5)])
    for i, (a, _, _) in enumerate(ACTS):
        es, ef = FECHAS[a]
        yy = y + 30 + i * 17
        crit = a in CRITICAS
        out.append(rect(f"{x + es * escala:.1f}", yy, f"{(ef - es) * escala:.1f}", 11, VIOLET if crit else BLUE, 3))
        if HOLGURA[a]:
            out.append(line(f"{x + ef * escala:.1f}", yy + 5.5, f"{x + (ef + HOLGURA[a]) * escala:.1f}", yy + 5.5,
                            BLUE, 2, 'stroke-dasharray="3 3"'))
    return "".join(out)


def riesgo(x, y):
    """Duración del proyecto: histograma y normal esquemáticos, con el plazo (03 / CALCULA)."""
    out = [text(x, y, "Riesgo del plazo", 22, INK, 500)]
    for yy in (y + 35, y + 76, y + 117):
        out.append(line(x, yy, x + 256, yy, "#ece7eb", 1))
    out.extend([line(x, y + 23, x, y + 134, LINE, 1.5), line(x, y + 134, x + 256, y + 134, LINE, 1.5)])
    # Histograma esquemático con la cola a la derecha (la fusión de caminos) y la normal, más a la izquierda.
    alturas = [3, 8, 18, 34, 55, 76, 92, 98, 95, 84, 70, 55, 41, 30, 21, 14, 9, 6, 3, 2]
    w = 256 / (len(alturas) + 2)
    for i, h in enumerate(alturas):
        out.append(rect(f"{x + (i + 1) * w + 1:.1f}", f"{y + 134 - h:.1f}", f"{w - 2:.1f}", h, PALE_BLUE, 1.5,
                        "#9fb4cf", 1))
    pts = []
    for k in range(0, 129):
        u = k / 128 * 256
        z = (u - 112) / 34
        pts.append(f"{x + u:.1f} {y + 134 - 104 * exp(-z * z / 2):.1f}")
    out.append(path("M " + " L ".join(pts), VIOLET, 3.5))
    out.append(line(x + 170, y + 23, x + 170, y + 134, INK, 2, 'stroke-dasharray="5 4"'))
    out.append(text(x + 176, y + 40, "plazo", 15, INK, 600))
    return "".join(out)


def panel():
    """Laboratorio esquemático; coordenadas locales de 1020 × 730."""
    out = [
        rect(6, 12, 1020, 730, "#e9e3e7", 25),
        rect(0, 0, 1020, 730, "#ffffff", 25, LINE, 2),
        path("M 25 0 H 995 Q 1020 0 1020 25 V 72 H 0 V 25 Q 0 0 25 0", INK, 0, INK),
        circle(35, 36, 5, "#d9a6d3"),
        label(56, 42, "LABORATORIO / REDES DE PROYECTOS", "#ffffff", 16),
        # Pequeña marca: una red de tres nudos.
        line(936, 36, 958, 24, "#ffffff", 2), line(936, 36, 958, 48, "#ffffff", 2),
        line(958, 24, 980, 36, "#ffffff", 2), line(958, 48, 980, 36, "#ffffff", 2),
        circle(936, 36, 5, "#d9a6d3"), circle(958, 24, 5, "#a9c4e6"), circle(958, 48, 5, "#a9c4e6"),
        circle(980, 36, 5, "#ffffff"),
        rect(20, 92, 244, 616, "#f7f2f6", 14),
        label(43, 130, "01 / DEFINE", VIOLET, 16),
        tabla(43, 175),
        rect(43, 493, 193, 58, VIOLET, 9),
        path("M 63 511 L 63 533 L 80 522 Z", "none", 0, "#ffffff"),
        text(98, 531, "Calcula", 24, "#ffffff", 600),
        # Un círculo con interrogación: el modo predicción del portal.
        circle(114, 624, 20, "none", MUTED, 2),
        text(114, 632, "?", 22, MUTED, 600, 'text-anchor="middle"'),
        text(149, 630, "Predice", 20, MUTED),
        label(302, 130, "02 / DIBUJA", BLUE, 16),
        text(302, 172, "Una red, dos lenguajes", 30, INK, 600),
        label(302, 220, "ROY", MUTED, 13),
        label(720, 220, "PERT", MUTED, 13),
        line(698, 214, 698, 418, "#d8cfd6", 1.5, 'stroke-dasharray="4 5"'),
        roy(),
        pert(),
        line(302, 449, 975, 449, LINE, 1.5),
        label(302, 488, "03 / CALCULA", VIOLET, 16),
        gantt(302, 533),
        riesgo(650, 533),
        # Leyenda: crítica (violeta) y con holgura (azul).
        rect(822, 476, 16, 12, VIOLET, 3),
        text(844, 487, "crítica", 15, MUTED),
        rect(905, 476, 16, 12, BLUE, 3),
        text(927, 487, "con holgura", 15, MUTED),
    ]
    return "".join(out)


def svg_document(width, height, body, description):
    # SVG autónomo, fuentes del sistema, texto editable y sin recursos enlazados.
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="cover-title cover-desc">
<title id="cover-title">{escape(TITLE)}</title>
<desc id="cover-desc">{escape(description)}</desc>
<metadata>Ilustración editorial original, adaptada de la portada de «Evolución a la vista» con asistencia de Claude, 2026-11-27. Contenido CC BY 4.0. Tabla, redes, Gantt e histograma esquemáticos; la red es coherente. Texto editable; fuentes de sistema.</metadata>
<g font-family="Arial, Helvetica, sans-serif">{body}</g>
</svg>
'''


def portrait():
    out = [
        rect(0, 0, 1200, 1800, PAPER),
        rect(0, 0, 16, 1800, VIOLET),
        label(90, 99, "DEFINE · DIBUJA · CALCULA", VIOLET, 19),
        line(90, 134, 1110, 134, LINE, 2),
        text(83, 273, "Proyectos", 132, INK, 700, 'letter-spacing="-6"'),
        text(83, 410, "a la vista.", 132, INK, 700, 'letter-spacing="-6"'),
        text(90, 508, "Redes PERT, CPM y ROY", 66, VIOLET, 600, 'letter-spacing="-2"'),
        text(90, 567, "en un laboratorio interactivo", 43, INK, 400, 'letter-spacing="-0.5"'),
        '<g transform="translate(90 654)">' + panel() + '</g>',
        line(90, 1451, 150, 1451, VIOLET, 3),
        text(173, 1461, "Predice. Calcula. Comprende.", 34, INK, 500),
        line(90, 1545, 1110, 1545, LINE, 2),
        label(90, 1597, "AUTORES", MUTED, 16),
        text(90, 1648, "José Manuel Galán · Silvia Díaz-de la Fuente", 30, INK, 500),
        text(90, 1694, "Virginia Ahedo · María Pereda · José Ignacio Santos", 30, INK, 500),
        label(90, 1760, "PROJECT NETWORK LAB · PERT · CPM · ROY", VIOLET, 16),
        rect(1005, 1735, 28, 28, VIOLET, 5),
        rect(1043, 1735, 28, 28, BLUE, 5),
        rect(1081, 1735, 28, 28, PALE_VIOLET, 5),
    ]
    return svg_document(1200, 1800, "".join(out),
        "Portada con el título completo y los cinco autores. Un panel de laboratorio conecta una tabla de "
        "precedencias, la misma red dibujada en ROY y en PERT con el camino crítico en violeta, un diagrama de "
        "Gantt y un histograma de la duración con la normal y el plazo.")


def landscape():
    out = [
        rect(0, 0, 1800, 1000, PAPER),
        rect(0, 0, 16, 1000, VIOLET),
        label(80, 96, "DEFINE · DIBUJA · CALCULA", VIOLET, 17),
        text(74, 242, "Proyectos", 100, INK, 700, 'letter-spacing="-4.5"'),
        text(74, 350, "a la vista.", 100, INK, 700, 'letter-spacing="-4.5"'),
        text(80, 435, "Redes PERT, CPM y ROY", 50, VIOLET, 600, 'letter-spacing="-1.5"'),
        text(80, 486, "en un laboratorio", 38, INK),
        text(80, 534, "interactivo", 38, INK),
        line(80, 624, 126, 624, VIOLET, 3),
        text(149, 634, "Predice. Calcula. Comprende.", 26, INK, 500),
        '<g transform="translate(745 178) scale(0.94)">' + panel() + '</g>',
        line(80, 748, 650, 748, LINE, 2),
        text(80, 798, AUTHORS[0], 25, INK, 500),
        text(80, 837, AUTHORS[1], 25, INK, 500),
        text(80, 876, AUTHORS[2] + " · " + AUTHORS[3], 25, INK, 500),
        text(80, 915, AUTHORS[4], 25, INK, 500),
        label(745, 96, "PROJECT NETWORK LAB · PERT · CPM · ROY", VIOLET, 16),
    ]
    return svg_document(1800, 1000, "".join(out),
        "Adaptación horizontal: título y autores a la izquierda; a la derecha, el panel del laboratorio con la "
        "tabla, las redes ROY y PERT, el Gantt y el riesgo del plazo.")


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    for name, content in (("portada.svg", portrait()), ("portada-horizontal.svg", landscape())):
        target = folder / name
        target.write_text(content, encoding="utf-8", newline="\n")
        print(target)
