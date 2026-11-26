"""Ayuda para las figuras propias de redes PERT (capítulo 4): fragmentos con sucesos y flechas.

Cada panel tiene título, subtítulo, sucesos (círculos, con número o sin él), actividades (flechas
continuas con su letra) y ficticias (flechas de trazos con su nombre en cursiva). Un extremo puede
ser un suceso o un punto suelto: así se dibujan fragmentos de red, con flechas abiertas, como en los
esquemas del portal. Mismo estilo que figuras/03-prelaciones.py. El SVG se escribe a mano para que el
texto quede como texto y el archivo no cambie entre ejecuciones.
"""
import math

GRIS = '#8a8781'      # bordes y flechas, como en el portal
TINTA = '#222222'
SUAVE = '#6b6862'
AVISO = '#a0522d'     # nota bajo el panel
R = 14                # radio de los sucesos
FUENTE = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def _punto(extremo, sucesos):
    """Centro y si es un suceso (para recortar la flecha en su borde)."""
    if isinstance(extremo, str):
        x, y = sucesos[extremo][:2]
        return x, y, True
    return extremo[0], extremo[1], False


def panel(x0, y0, ancho, titulo, subtitulo, sucesos, flechas, nota=None):
    """Devuelve los elementos SVG de un panel con origen en (x0, y0).

    sucesos: {clave: (x, y, etiqueta)}; flechas: [(etiqueta, desde, hasta, ficticia)], con desde y
    hasta como clave de suceso o como punto (x, y) suelto.
    """
    s = []
    cx = x0 + ancho / 2
    s.append(f'<text x="{cx:.1f}" y="{y0 + 26}" text-anchor="middle" font-size="15" font-weight="600" fill="{TINTA}">{titulo}</text>')
    s.append(f'<text x="{cx:.1f}" y="{y0 + 46}" text-anchor="middle" font-size="12.5" fill="{SUAVE}">{subtitulo}</text>')
    for etiqueta, desde, hasta, ficticia in flechas:
        x1, y1, s1 = _punto(desde, sucesos)
        x2, y2, s2 = _punto(hasta, sucesos)
        x1, y1, x2, y2 = x0 + x1, y0 + y1, x0 + x2, y0 + y2
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        if s1:
            x1, y1 = x1 + ux * R, y1 + uy * R
        if s2:
            x2, y2 = x2 - ux * (R + 1), y2 - uy * (R + 1)
        trazo = ' stroke-dasharray="5 4"' if ficticia else ''
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GRIS}" stroke-width="1.6"{trazo} '
                 'marker-end="url(#punta)"/>')
        # Etiqueta: a la izquierda de la flecha según su sentido (encima si va hacia la derecha).
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nx, ny = uy, -ux
        if abs(ux) < 0.2:          # casi vertical: la etiqueta, a la derecha
            nx, ny = 1, 0
        lx, ly = mx + nx * 11, my + ny * 11
        ancla = 'start' if nx > 0.5 else ('end' if nx < -0.5 else 'middle')
        estilo = ' font-style="italic"' if ficticia else ' font-weight="600"'
        s.append(f'<text x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="{ancla}" font-size="14"{estilo} fill="{TINTA}">{etiqueta}</text>')
    for x, y, etiqueta in sucesos.values():
        s.append(f'<circle cx="{x0 + x}" cy="{y0 + y}" r="{R}" fill="#ffffff" stroke="{GRIS}" stroke-width="1.6"/>')
        if etiqueta:
            s.append(f'<text x="{x0 + x}" y="{y0 + y + 5}" text-anchor="middle" font-size="13.5" font-weight="600" fill="{TINTA}">{etiqueta}</text>')
    if nota:
        s.append(f'<text x="{cx:.1f}" y="{y0 + 222}" text-anchor="middle" font-size="12.5" fill="{AVISO}">{nota}</text>')
    return s


def documento(ancho, alto, cuerpo, separadores=()):
    """SVG completo. separadores: [(x1, y1, x2, y2)] líneas finas entre paneles."""
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" font-family="{FUENTE}">',
         '<defs><marker id="punta" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" '
         f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GRIS}"/></marker></defs>']
    for x1, y1, x2, y2 in separadores:
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e2e0da" stroke-width="1"/>')
    s += cuerpo
    s.append('</svg>')
    return '\n'.join(s) + '\n'


AZUL = '#dbe7f5'      # fila de las actividades, como en las transparencias
ROJO = '#c0392b'      # lo que comparten las columnas


def tabla(x0, y0, filas, ancho_etiqueta=92, ancho_col=64, alto=26, hueco=16):
    """Tabla de precedencias en miniatura, como en las transparencias de clase.

    filas: [(etiqueta, [celda, celda], es_actividad)], con cada celda como lista de (texto, resaltado).
    Las columnas de los extremos van en blanco y con trazo discontinuo: es un trozo de una tabla mayor.
    """
    s = []
    n = len(filas[0][1])
    xs = [x0, x0 + ancho_etiqueta, x0 + ancho_etiqueta + hueco]
    for _ in range(n):
        xs.append(xs[-1] + ancho_col)
    xs.append(xs[-1] + hueco)
    total_alto = alto * len(filas)
    for i, (etiqueta, celdas, es_act) in enumerate(filas):
        y = y0 + i * alto
        if es_act:
            s.append(f'<rect x="{x0}" y="{y}" width="{xs[-1] - x0}" height="{alto}" fill="{AZUL}"/>')
        s.append(f'<text x="{x0 + 6}" y="{y + 17.5}" font-size="12.5" font-weight="600" fill="{TINTA}">{etiqueta}</text>')
        for j, celda in enumerate(celdas):
            cx = (xs[2 + j] + xs[3 + j]) / 2
            partes = []
            for k, (texto, resaltado) in enumerate(celda):
                sep = ', ' if k else ''
                color = ROJO if resaltado else TINTA
                peso = ' font-weight="600"' if resaltado else ''
                partes.append(f'<tspan fill="{TINTA}">{sep}</tspan><tspan fill="{color}"{peso}>{texto}</tspan>')
            s.append(f'<text x="{cx}" y="{y + 17.5}" text-anchor="middle" font-size="13">{"".join(partes)}</text>')
        if i:
            s.append(f'<line x1="{x0}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{TINTA}" stroke-width="0.8"/>')
    # Bordes: macizos en la etiqueta y en las columnas con datos; discontinuos en las columnas en blanco.
    y1, y2 = y0, y0 + total_alto
    d = ' stroke-dasharray="4 3"'
    s.append(f'<rect x="{x0}" y="{y1}" width="{xs[1] - x0}" height="{total_alto}" fill="none" stroke="{TINTA}" stroke-width="1.4"/>')
    s.append(f'<rect x="{xs[2]}" y="{y1}" width="{xs[-2] - xs[2]}" height="{total_alto}" fill="none" stroke="{TINTA}" stroke-width="1.4"/>')
    for x in xs[3:-2]:
        s.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{TINTA}" stroke-width="1"/>')
    for a, b in ((xs[1], xs[2]), (xs[-2], xs[-1])):
        for y in (y1, y2):
            s.append(f'<line x1="{a}" y1="{y}" x2="{b}" y2="{y}" stroke="{TINTA}" stroke-width="1.4"{d}/>')
    s.append(f'<line x1="{xs[-1]}" y1="{y1}" x2="{xs[-1]}" y2="{y2}" stroke="{TINTA}" stroke-width="1.4"{d}/>')
    return s, xs[-1] - x0
