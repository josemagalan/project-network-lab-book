"""Numeración de las cajas e índices del libro. Se ejecuta como «pre-render» (_quarto.yml).

Quarto numera los capítulos, las secciones y las figuras (number-sections). Este
guion calcula lo que Quarto no sabe numerar y genera tres archivos:

- _numeracion.json (no se versiona): número de cada sección, ejemplo y ejercicio, y
  archivo en el que está. Lo lee filtros/numeracion.lua para escribir el número en
  el título de cada caja y en las referencias [](#ejemplo-…), [](#ejercicio-…) y
  [](#sec-…){.capitulo}.
- indice.qmd: índice general detallado (capítulos y secciones, con su nivel).
- actividades.qmd: ejemplos reproducibles, cajas «En el portal» y ejercicios,
  por pestaña del portal y por capítulo.

Regla de las cajas: un ejemplo o ejercicio lleva el número de su sección (el
ejemplo 5.3 está en la sección 5.3), así que solo puede haber uno de cada tipo por
sección. Un capítulo con «numeracion-cajas: correlativa» en su cabecera YAML los
numera seguidos (1.1, 1.2, 1.3…) en todo el capítulo.

Solo reescribe un archivo si su contenido cambia. También puede lanzarse a mano:
python3 filtros/indices.py

Lee lo que ya marca cada capítulo:
  ## Título [[…]{.largo}[…]{.corto}]{.nivel .basico|.avanzado|.saber-mas} {#sec-…}
  ## Resumen {.unnumbered #resumen}
  ::: {.callout-tip .ejemplo #ejemplo-… title="Ejemplo reproducible · …"}
  ::: {.callout-note .en-app title="En el portal · pestaña, «…»"}
  :::: {.callout-note .ejercicio #ejercicio-… title="Ejercicio · …"}
"""
import json
import os
import re
import sys
from collections import OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NIVELES = {
    'basico': ('Básico', 'B'),
    'avanzado': ('Avanzado', 'A'),
    'saber-mas': ('Para saber más', '+'),
}
# Pestañas y páginas del portal, en el orden de su barra. Las claves salen de la dirección de
# cada botón: la página (examen.html, moodle.html) o el parámetro v= de cpm.html (sin v, la ruta guiada).
# Desfases (v=gpr) y coste–tiempo (v=ct) van juntos en «Extensiones», como en el portal (F5b, opción A).
HERRAMIENTAS = OrderedDict([
    ('portada', 'Portada del portal'),
    ('m0', 'Del enunciado a la tabla'),
    ('route', 'Ruta guiada'),
    ('work', 'Taller'),
    ('ext', 'Extensiones'),
    ('unc', 'Duraciones inciertas'),
    ('ex', 'Ejercicios'),
    ('examen', 'Examen imprimible'),
    ('moodle', 'Bancos de preguntas para Moodle'),
])
PESTANA_DE_V = {'route': 'route', 'work': 'work', 'm0': 'm0', 'ex': 'ex', 'unc': 'unc',
                'gpr': 'ext', 'ct': 'ext', 'moodle': 'moodle'}
TIPOS = {
    'ejemplo': 'Ejemplo reproducible',
    'en-app': 'En el portal',
    'ejercicio': 'Ejercicio',
}

CAPITULO = re.compile(r'^# (.+?)\s*\{#([\w-]+)[^}]*\}\s*$')
SECCION = re.compile(
    r'^## (.+?) \[\[[^\]]*\]\{\.largo\}\[[^\]]*\]\{\.corto\}\]'
    r'\{\.nivel \.([\w-]+)\}\s*\{#([\w-]+)\}\s*$')
SECCION_SIN_NIVEL = re.compile(r'^## (.+?)\s*\{([^}]*)\}\s*$')
CAJA = re.compile(r'^(:{3,}) \{\.callout-\w+ \.(ejemplo|en-app|ejercicio)(?: #([\w-]+))? title="([^"]*)"\}\s*$')
URL = re.compile(r'https?://[^\s)\]"\'>]+')


def herramientas_de(texto):
    """Pestañas del portal a las que enlaza una caja (por las direcciones de sus botones)."""
    vistas = []
    for u in URL.findall(texto):
        m = re.match(r'https://josemagalan\.github\.io/project-network-lab/([\w.-]*)(?:\?[^#]*)?(?:#(.*))?$', u)
        if not m:
            continue
        pagina, hash_ = m.group(1), m.group(2) or ''
        if pagina in ('', 'index.html'):
            clave = 'portada'
        elif pagina == 'examen.html':
            clave = 'examen'
        elif pagina == 'moodle.html':
            clave = 'moodle'
        elif pagina == 'cpm.html':
            v = re.search(r'(?:^|&)v=([\w-]+)', hash_)
            clave = PESTANA_DE_V.get(v.group(1) if v else 'route')
        else:
            clave = None
        if clave and clave not in vistas:
            vistas.append(clave)
    return vistas


def capitulos():
    """Archivos de capítulo en el orden de _quarto.yml (los que empiezan por número)."""
    with open(os.path.join(RAIZ, '_quarto.yml'), encoding='utf-8') as fh:
        yml = fh.read()
    bloque = yml.split('chapters:', 1)[1]
    return [a for a in re.findall(r'^\s+-\s+([\w-]+\.qmd)', bloque, re.M) if re.match(r'\d\d-', a)]


class ErrorNumeracion(Exception):
    pass


def leer(archivo, numero):
    with open(os.path.join(RAIZ, archivo), encoding='utf-8') as fh:
        texto = fh.read()
    cabecera = re.match(r'^---\n(.*?)\n---\n', texto, re.S)
    correlativa = bool(cabecera and re.search(r'^numeracion-cajas:\s*correlativa\b', cabecera.group(1), re.M))
    lineas = texto.split('\n')
    cap = {'archivo': archivo, 'numero': numero, 'titulo': None, 'id': None, 'secciones': [], 'cajas': []}
    seccion = None
    n_seccion = 0
    usados = {}                 # (tipo, sección) -> id de la caja, para detectar repeticiones
    seguidos = {'ejemplo': 0, 'ejercicio': 0}
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if cap['titulo'] is None:
            m = CAPITULO.match(linea)
            if m:
                cap['titulo'], cap['id'] = m.group(1).strip(), m.group(2)
        if linea.startswith('## '):
            m = SECCION.match(linea)
            if m:
                n_seccion += 1
                seccion = {'num': f'{numero}.{n_seccion}', 'titulo': m.group(1).strip(),
                           'nivel': m.group(2), 'ancla': m.group(3)}
                cap['secciones'].append(seccion)
            else:
                m = SECCION_SIN_NIVEL.match(linea)
                if m and '.unnumbered' in m.group(2):
                    seccion = None          # Resumen, Referencias…
                else:
                    raise ErrorNumeracion(f'{archivo}: la sección «{linea[3:]}» no lleva etiqueta de nivel '
                                          'ni {.unnumbered}; Quarto la numeraría y los índices no la verían.')
        m = CAJA.match(linea)
        if m:
            cierre = m.group(1)
            j = i + 1
            while j < len(lineas) and lineas[j].strip() != cierre:
                j += 1
            contenido = '\n'.join(lineas[i + 1:j])
            tipo, ancla, titulo = m.group(2), m.group(3), m.group(4)
            partes = titulo.split(' · ', 1)
            nombre = partes[1] if len(partes) > 1 else ''
            num = None
            if tipo in seguidos:
                if re.search(r'\d+\.\d+', partes[0]):
                    raise ErrorNumeracion(f'{archivo}: la caja #{ancla} lleva el número escrito en el título '
                                          f'(«{titulo}»); quítalo, lo pone el filtro.')
                if not ancla:
                    raise ErrorNumeracion(f'{archivo}: una caja «{titulo}» no tiene identificador (#{tipo}-…).')
                if correlativa:
                    seguidos[tipo] += 1
                    num = f'{numero}.{seguidos[tipo]}'
                else:
                    if seccion is None:
                        raise ErrorNumeracion(f'{archivo}: la caja #{ancla} está fuera de una sección numerada.')
                    if (tipo, seccion['num']) in usados:
                        raise ErrorNumeracion(
                            f'{archivo}: la sección {seccion["num"]} tiene dos cajas de tipo {tipo} '
                            f'(#{usados[(tipo, seccion["num"])]} y #{ancla}). Con la numeración por sección solo '
                            'cabe una; muévela o pon «numeracion-cajas: correlativa» en la cabecera del capítulo.')
                    usados[(tipo, seccion['num'])] = ancla
                    num = seccion['num']
            cap['cajas'].append({
                'tipo': tipo, 'ancla': ancla, 'numero': num,
                'nombre': nombre, 'seccion': seccion,
                'herramientas': herramientas_de(contenido),
            })
            i = j
        i += 1
    return cap


def insignia(nivel, larga=False):
    largo, corto = NIVELES[nivel]
    if larga:
        return f'[[{largo}]{{.largo}}[{corto}]{{.corto}}]{{.nivel .{nivel}}}'
    return f'[[{corto}]{{.corto}}]{{.nivel .{nivel} .solo-corto}}'


def celda(texto):
    return texto.replace('|', '\\|')


def enlace_caja(cap, caja):
    destino = caja['ancla'] or (caja['seccion']['ancla'] if caja['seccion'] else None)
    if caja['tipo'] == 'en-app':
        texto = TIPOS['en-app']
    else:
        texto = f"{'Ejemplo' if caja['tipo'] == 'ejemplo' else 'Ejercicio'} {caja['numero']}"
    return f"[{texto}]({cap['archivo']}#{destino})" if destino else texto


def nombre_caja(caja):
    nombre = caja['nombre']
    if caja['tipo'] == 'en-app':
        # «Taller, «Tu propia red»» → «Tu propia red»; sin subtítulo, la caja explora la sección
        m = re.match(r'^[^,«]+(?:,\s*(.*))?$', nombre)
        nombre = (m.group(1) or '').strip() if m else nombre
        if not nombre:
            nombre = 'Exploración libre'
    return nombre


def enlace_seccion(cap, s):
    return f"[{s['num']}]({cap['archivo']}#{s['ancla']})" if s else '—'


def nombres_herramientas(claves):
    return ', '.join(HERRAMIENTAS.get(c, c) for c in claves) or '—'


AVISO = ('<!-- Archivo generado por filtros/indices.py en cada «quarto render» (pre-render). '
         'No lo edites a mano: los cambios se perderían. Para cambiar el contenido, '
         'cambia los capítulos; para cambiar el formato, cambia el script. -->')


def indice_general(caps):
    total = {k: 0 for k in NIVELES}
    cajas = {k: 0 for k in TIPOS}
    for c in caps:
        for s in c['secciones']:
            total[s['nivel']] += 1
        for b in c['cajas']:
            cajas[b['tipo']] += 1
    o = ['# Índice general {.unnumbered #sec-indice}', '', AVISO, '',
         f"El libro tiene {len(caps)} capítulos y {sum(total.values())} secciones: "
         f"{total['basico']} de nivel {insignia('basico', True)}, {total['avanzado']} de nivel "
         f"{insignia('avanzado', True)} y {total['saber-mas']} de nivel {insignia('saber-mas', True)}. "
         'El **recorrido básico** son las secciones azules: se leen seguidas, capítulo a capítulo, '
         'sin las demás. Las avanzadas amplían el recorrido básico y suelen apoyarse en él; '
         '«Para saber más» cierra cada capítulo con lecturas y temas que el libro no desarrolla.', '',
         f"Las actividades —{cajas['ejemplo']} ejemplos reproducibles, {cajas['en-app']} cajas "
         f"«En el portal» y {cajas['ejercicio']} ejercicios— están listadas en el "
         '[índice de actividades](actividades.qmd), por capítulo y por pestaña del portal.', '',
         '## El libro de un vistazo {.unnumbered #vistazo}', '',
         '| Capítulo | B | A | + | Ejemplos | En el portal | Ejercicios |',
         '|---|:-:|:-:|:-:|:-:|:-:|:-:|']
    for c in caps:
        n = {k: sum(1 for s in c['secciones'] if s['nivel'] == k) for k in NIVELES}
        b = {k: sum(1 for x in c['cajas'] if x['tipo'] == k) for k in TIPOS}
        o.append(f"| [{c['numero']}. {celda(c['titulo'])}]({c['archivo']}) | {n['basico']} | {n['avanzado']} | "
                 f"{n['saber-mas']} | {b['ejemplo']} | {b['en-app']} | {b['ejercicio']} |")
    o.append(f"| **Total** | **{total['basico']}** | **{total['avanzado']}** | **{total['saber-mas']}** | "
             f"**{cajas['ejemplo']}** | **{cajas['en-app']}** | **{cajas['ejercicio']}** |")
    o.append('')
    for c in caps:
        o += [f"## {c['numero']}. {c['titulo']} {{.unnumbered #cap-{c['numero']}}}", '']
        for s in c['secciones']:
            o.append(f"- [{s['num']} {s['titulo']}]({c['archivo']}#{s['ancla']}) {insignia(s['nivel'])}")
        o.append('')
    return '\n'.join(o)


def indice_actividades(caps):
    o = ['# Índice de actividades {.unnumbered #sec-actividades}', '', AVISO, '',
         'Aquí están todas las cajas de trabajo del libro. Los **ejemplos reproducibles** abren '
         'el portal en un estado fijado, de modo que el resultado coincide con el del libro; '
         'las cajas **En el portal** proponen explorar sin resultados fijados; los **ejercicios** '
         'se resuelven con papel y lápiz. La primera parte las ordena por pestaña del portal, para preparar '
         'una sesión con una pestaña concreta; la segunda, por capítulo. La columna de nivel es '
         'la de la sección en la que está la caja.', '']
    # --- Por pestaña
    o += ['## Por pestaña del portal {.unnumbered #por-pestana}', '']
    for clave, nombre in HERRAMIENTAS.items():
        filas = [(c, b) for c in caps for b in c['cajas'] if clave in b['herramientas']]
        if not filas:
            continue
        n_ej = sum(1 for _, b in filas if b['tipo'] == 'ejemplo')
        n_app = sum(1 for _, b in filas if b['tipo'] == 'en-app')
        n_ejer = sum(1 for _, b in filas if b['tipo'] == 'ejercicio')
        resumen = [texto for n, uno, varios in ((n_ej, 'ejemplo reproducible', 'ejemplos reproducibles'),
                                                (n_app, 'caja «En el portal»', 'cajas «En el portal»'),
                                                (n_ejer, 'ejercicio', 'ejercicios'))
                   if n for texto in [f'{n} {uno if n == 1 else varios}']]
        frase = resumen[0] if len(resumen) == 1 else ', '.join(resumen[:-1]) + ' y ' + resumen[-1]
        o += [f"### {nombre} {{.unnumbered #h-{clave}}}", '', frase[0].upper() + frase[1:] + '.', '',
              '| Actividad | Título | Sección | Nivel |', '|---|---|:-:|:-:|']
        for c, b in filas:
            nivel = insignia(b['seccion']['nivel']) if b['seccion'] else ''
            o.append(f"| {enlace_caja(c, b)} | {celda(nombre_caja(b))} | {enlace_seccion(c, b['seccion'])} | {nivel} |")
        o.append('')
    # --- Por capítulo
    o += ['## Por capítulo {.unnumbered #por-capitulo}', '']
    for c in caps:
        if not c['cajas']:
            continue
        o += [f"### {c['numero']}. {c['titulo']} {{.unnumbered #a-cap-{c['numero']}}}", '',
              '| Actividad | Título | Sección | Pestaña | Nivel |', '|---|---|:-:|---|:-:|']
        for b in c['cajas']:
            nivel = insignia(b['seccion']['nivel']) if b['seccion'] else ''
            o.append(f"| {enlace_caja(c, b)} | {celda(nombre_caja(b))} | {enlace_seccion(c, b['seccion'])} | "
                     f"{nombres_herramientas(b['herramientas'])} | {nivel} |")
        o.append('')
    return '\n'.join(o)


def escribir(nombre, texto):
    ruta = os.path.join(RAIZ, nombre)
    texto = texto.rstrip('\n') + '\n'
    try:
        with open(ruta, encoding='utf-8') as fh:
            if fh.read() == texto:
                return
    except FileNotFoundError:
        pass
    with open(ruta, 'w', encoding='utf-8') as fh:
        fh.write(texto)
    print(f'indices.py: {nombre} actualizado')


def numeracion(caps):
    datos = {'capitulos': {}, 'secciones': {}, 'cajas': {}}
    for c in caps:
        datos['capitulos'][c['id']] = {'archivo': c['archivo'], 'numero': str(c['numero'])}
        for s in c['secciones']:
            datos['secciones'][s['ancla']] = {'archivo': c['archivo'], 'numero': s['num'],
                                              'capitulo': str(c['numero'])}
        for b in c['cajas']:
            if b['numero']:
                if b['ancla'] in datos['cajas']:
                    raise ErrorNumeracion(f'identificador repetido: #{b["ancla"]}')
                datos['cajas'][b['ancla']] = {'archivo': c['archivo'], 'numero': b['numero'], 'tipo': b['tipo']}
    return json.dumps(datos, ensure_ascii=False, indent=1, sort_keys=True)


def main():
    try:
        caps = [leer(a, n) for n, a in enumerate(capitulos(), 1)]
    except ErrorNumeracion as e:
        sys.exit(f'indices.py: {e}')
    escribir('_numeracion.json', numeracion(caps))
    escribir('indice.qmd', indice_general(caps))
    escribir('actividades.qmd', indice_actividades(caps))


if __name__ == '__main__':
    main()
