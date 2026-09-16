"""Gera web/assets/sobressalentes-v1.glb: peças sobressalentes do Box INTEIA para cenários de corrida
(pista rápida, pista travada, chuva, intermediário, calor). Cada nó do GLB substitui a geometria de um
nó do carro v2 (modo `geometry`, mesma origem e mesmo referencial local) ou é anexado a um nó (modo `attach`).

  blender -b --python ferramentas/gerar_sobressalentes.py

Slots e variantes:
  tyres       macio · medio · duro · intermediario · chuva      (front_tire__01/02, rear_tire__01/02)
  rear_wing   baixa · alta                                        (rear_wing_main_part__01 + rear_wing_drs__01)
  front_wing  baixa · alta                                        (front_wing_top__01)
  beam_wing   dupla                                               (rear_wing_bottom_holder__01)
  cooling     aberto                                              (anexo em main_body__01: venezianas)
A variante `original` de cada slot é o próprio carro (nada a gerar).
"""
import bpy, bmesh, math, sys, json, hashlib, time
from pathlib import Path
from mathutils import Vector, Matrix
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SYS_DIR = ROOT / 'ferramentas' / 'sistemas'
OUT = ROOT / 'web' / 'assets'
sys.path.insert(0, str(SYS_DIR))
import lib
from lib import *

started = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'; scene.unit_settings.scale_length = 1.0
m = Materials()
ctx = Context(scene, m)
ctx.system('spares', 'Sobressalentes')

# ----------------------------------------------------------------------------- carro v2: origens e superfície
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(OUT / 'carro-aula-v2.glb'))
car = [o for o in bpy.data.objects if o not in before]
ORIGIN = {}
BODY = []
for o in car:
    if o.type != 'MESH':
        continue
    mw = o.matrix_world
    rot = mw.to_3x3()
    assert all(abs(rot[i][j] - (1 if i == j else 0)) < 1e-4 for i in range(3) for j in range(3)), f'{o.name}: nó com rotação/escala; o modo geometry exige translação pura'
    ORIGIN[o.name] = to_web(mw.translation)
    if o.name == 'main_body__01':
        BODY = [to_web(mw @ v.co) for v in o.data.vertices]
for o in car:
    bpy.data.objects.remove(o, do_unlink=True)
assert BODY, 'main_body__01 não encontrado'
BODY_NP = np.array(BODY)

def surface_y(x, z, r=.035):
    sel = BODY_NP[(abs(BODY_NP[:, 0] - x) < r) & (abs(BODY_NP[:, 2] - z) < r)]
    return float(sel[:, 1].max()) if len(sel) else None

# ----------------------------------------------------------------------------- registro dos sobressalentes
SPARES = []

def spare(obj, slot, variant, target, label, mode='geometry', **extra):
    """Rebaseia a malha na origem do nó alvo (coordenadas locais idênticas às do carro) e marca os extras."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    origin = W(ORIGIN[target])
    for v in obj.data.vertices:
        v.co -= origin
    obj.location = origin
    obj.name = f'spare__{slot}__{variant}__{target}'[:63]
    obj['spare'] = 1; obj['slot'] = slot; obj['variant'] = variant; obj['target'] = target; obj['mode'] = mode; obj['label'] = label
    for k, v in extra.items():
        obj[k] = v
    SPARES.append(obj)
    return obj

# ----------------------------------------------------------------------------- pneus
TYRE = {
    # slot, cor da faixa, tipo de sulco, rótulo
    'macio': ((.85, .06, .06), 'slick', 'Pneu macio (faixa vermelha)'),
    'medio': ((.95, .72, .05), 'slick', 'Pneu médio (faixa amarela)'),
    'duro': ((.92, .92, .90), 'slick', 'Pneu duro (faixa branca)'),
    'intermediario': ((.05, .60, .22), 'inter', 'Pneu intermediário (faixa verde)'),
    'chuva': ((.05, .32, .88), 'wet', 'Pneu de chuva extrema (faixa azul)'),
}
WHEELS = {  # nó alvo: (centro web, largura, raio da banda)
    'front_tire__01': ((-.743, .300, 1.520), .362, .329),
    'front_tire__02': ((.743, .300, 1.520), .362, .329),
    'rear_tire__01': ((-.720, .313, -1.840), .407, .341),
    'rear_tire__02': ((.720, .313, -1.840), .407, .341),
}

def tyre_profile(width, R):
    h = width / 2
    return [(.215, -h + .022), (.240, -h + .010), (.282, -h), (.312, -h + .010), (.324, -h + .036), (R - .002, -h + .070), (R, -h + .10),
            (R, 0), (R, h - .10), (R - .002, h - .070), (.324, h - .036), (.312, h - .010), (.282, h), (.240, h - .010), (.215, h - .022)]

def tyre_texture(kind, band, size=(1024, 512)):
    """Textura do pneu em (u = volta, v = perfil): banda colorida no flanco, sulcos na banda de rodagem."""
    w, h = size
    v = np.linspace(0, 1, h)[:, None] * np.ones((1, w)); u = np.ones((h, 1)) * np.linspace(0, 1, w)[None, :]
    rng = np.random.default_rng(5)
    col = np.zeros((h, w, 3)) + np.array((.030, .030, .033))
    # flancos um pouco mais claros com grão radial
    flank = (v < .34) | (v > .66)
    col[flank] += .012 + .006 * rng.random((h, w))[flank, None]
    # faixa colorida (dois flancos), estreita, como a marcação do composto
    for a, b in ((.105, .135), (.865, .895)):   # faixa no flanco, como a marcação de composto
        band_m = (v >= a) & (v <= b)
        col[band_m] = np.array(band)
    height = np.zeros((h, w))
    tread = (v >= .36) & (v <= .64)
    if kind == 'slick':
        grain = .35 * (rng.random((h, w)) - .5) * (np.sin(u * 2 * math.pi * 300) > .3)
        height += grain * tread
        col[tread] += .004 * np.sin(u[tread] * 2 * math.pi * 300)[:, None]
    else:
        n_circ = 4 if kind == 'wet' else 3
        gw = .010 if kind == 'wet' else .007
        for k in range(n_circ):
            vc = .36 + .28 * (k + 1) / (n_circ + 1)
            g = abs(v - vc) < gw
            height[g] = -1; col[g] = (.006, .006, .008)
        periods = 72 if kind == 'wet' else 54
        slope = 1.4 if kind == 'wet' else 1.0
        phase = (u * periods + (v - .5) * slope * periods / 6) % 1.0
        diag = (abs(phase - .5) < (.10 if kind == 'wet' else .07)) & tread & (abs(v - .5) < (.13 if kind == 'wet' else .10))
        height[diag] = -1; col[diag] = (.007, .007, .009)
    normal = lib._encode_normal(height * (1.6 if kind == 'wet' else 1.2), 2.2)
    rgba = np.concatenate([np.clip(col, 0, 1), np.ones((h, w, 1))], -1)
    return lib.image_from_array(f'Pneu {kind} {band} · cor', rgba), lib.image_from_array(f'Pneu {kind} {band} · normal', normal, False)

TYRE_MAT = {}
for variant, (band, kind, label) in TYRE.items():
    tex, nrm = tyre_texture(kind, band)
    TYRE_MAT[variant] = lib.material(f'Pneu · {variant}', (1, 1, 1), 0.0, .86, base_tex=tex, normal_tex=nrm, uv_scale=1.0)

def build_tyre(name, center, width, R, mat):
    prof = tyre_profile(width, R)
    # comprimento de arco para v proporcional
    acc = [0.0]
    for i in range(1, len(prof)):
        acc.append(acc[-1] + math.hypot(prof[i][0] - prof[i - 1][0], prof[i][1] - prof[i - 1][1]))
    vs = [a / acc[-1] for a in acc]
    seg = 112
    bm = bmesh.new(); uv_layer = bm.loops.layers.uv.new('UVMap')
    rings = []
    for r, hx in prof:
        ring = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            p = (center[0] + hx, center[1] + r * math.cos(a), center[2] + r * math.sin(a))
            ring.append(bm.verts.new(W(p)))
        rings.append(ring)
    for j in range(len(rings) - 1):
        for i in range(seg):
            i2 = (i + 1) % seg
            f = bm.faces.new((rings[j][i], rings[j][i2], rings[j + 1][i2], rings[j + 1][i]))
            uvs = ((i / seg, vs[j]), ((i + 1) / seg, vs[j]), ((i + 1) / seg, vs[j + 1]), (i / seg, vs[j + 1]))
            for loop, uv in zip(f.loops, uvs):
                loop[uv_layer].uv = uv
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = lib.bm_to_object(name, bm, smooth=True)
    lib.set_material(o, mat)
    return ctx.register(o, name)

for variant, (band, kind, label) in TYRE.items():
    for target, (center, width, R) in WHEELS.items():
        o = build_tyre(f'{label} · {target}', center, width, R, TYRE_MAT[variant])
        spare(o, 'tyres', variant, target, label, band=[float(c) for c in band], kind=kind)

# ----------------------------------------------------------------------------- asas
def wing_section(le, chord, angle_deg, thick=.10, camber=-.05, n=16):
    """Anel 3D de um perfil no plano (z, y): bordo de ataque em `le` = (x, y, z), corda para −Z, bordo de fuga
    levantado por `angle_deg` (asa geradora de carga: arqueamento negativo)."""
    pts = []
    a = math.radians(angle_deg)
    for ax, by in airfoil(chord, thick, camber, n):
        s = ax + chord / 2          # distância ao longo da corda a partir do bordo de ataque
        dz, dy = -s, by
        # gira em torno do bordo de ataque levantando o bordo de fuga
        rz = dz * math.cos(a) + dy * math.sin(a)
        ry = -dz * math.sin(a) + dy * math.cos(a)
        pts.append((le[0], le[1] + ry, le[2] + rz))
    return pts

def span_loft(name, xs, section_at, mat):
    return loft(ctx, name, [section_at(x) for x in xs], mat, cap=True)

XS = [-.60, -.45, -.30, -.15, 0.0, .15, .30, .45, .60]
# --- asa traseira: plano principal + flap (o DRS/flap do carro é substituído junto)
REAR = {
    'baixa': dict(main=dict(le=(.704, -2.060), chord=.28, angle=4, thick=.07, camber=-.02), flap=dict(le=(.722, -2.235), chord=.12, angle=18, thick=.08, camber=-.03), gurney=False,
                  label='Asa traseira de baixa carga (pista rápida)'),
    'alta': dict(main=dict(le=(.700, -2.036), chord=.36, angle=9, thick=.11, camber=-.07), flap=dict(le=(.730, -2.225), chord=.20, angle=36, thick=.10, camber=-.05), gurney=True,
                 label='Asa traseira de alta carga (pista travada / chuva)'),
}
for variant, cfg in REAR.items():
    mp = cfg['main']
    main = span_loft(f'{cfg["label"]} · plano principal', XS, lambda x: wing_section((x, mp['le'][0], mp['le'][1]), mp['chord'], mp['angle'], mp['thick'], mp['camber']), m.carbon)
    if cfg['gurney']:
        a = math.radians(mp['angle']); c = mp['chord']
        te = (mp['le'][0] + c * math.sin(a), mp['le'][1] - c * math.cos(a))
        g = cube(ctx, 'Gurney', (0, te[0] + .008, te[1] + .002), (1.20, .016, .004), m.carbon, bev=.0005)
        main = join(ctx, [main, g], part=f'{cfg["label"]} · plano principal')
    spare(main, 'rear_wing', variant, 'rear_wing_main_part__01', cfg['label'], element='plano principal')
    fp = cfg['flap']
    flap = span_loft(f'{cfg["label"]} · flap', XS, lambda x: wing_section((x, fp['le'][0], fp['le'][1]), fp['chord'], fp['angle'], fp['thick'], fp['camber']), m.carbon)
    spare(flap, 'rear_wing', variant, 'rear_wing_drs__01', cfg['label'], element='flap móvel')

# --- flap superior da asa dianteira: seções medidas no carro v2 (|x|: LE z, LE y, corda, ângulo)
FW = [(0.0, 2.268, .139, .065, 15), (.15, 2.256, .158, .078, 18), (.30, 2.226, .192, .105, 25), (.45, 2.202, .228, .110, 26), (.60, 2.177, .225, .080, 30), (.638, 2.170, .222, .070, 30)]
def fw_at(ax, d_angle, k_chord):
    ax = abs(ax)
    for (x0, z0, y0, c0, a0), (x1, z1, y1, c1, a1) in zip(FW, FW[1:]):
        if x0 <= ax <= x1:
            t = (ax - x0) / (x1 - x0)
            return (z0 + (z1 - z0) * t, y0 + (y1 - y0) * t, (c0 + (c1 - c0) * t) * k_chord, a0 + (a1 - a0) * t + d_angle)
    z, y, c, a = FW[-1][1:]
    return (z, y, c * k_chord, a + d_angle)
FRONT = {'baixa': (-7, .88, 'Flap dianteiro de baixa carga (pista rápida)'), 'alta': (9, 1.18, 'Flap dianteiro de alta carga (pista travada / chuva)')}
FXS = [-.636, -.55, -.45, -.30, -.15, 0.0, .15, .30, .45, .55, .636]
for variant, (da, kc, label) in FRONT.items():
    def sec(x, da=da, kc=kc):
        z, y, c, a = fw_at(x, da, kc)
        return wing_section((x, y, z), c, a, .09, -.04)
    o = span_loft(label, FXS, sec, m.carbon)
    spare(o, 'front_wing', variant, 'front_wing_top__01', label)

# --- asa de viga dupla
b1 = span_loft('Asa de viga dupla · elemento inferior', [-.417, -.2, 0, .2, .417], lambda x: wing_section((x, .372, -2.092), .26, 8, .08, -.03), m.carbon)
b2 = span_loft('Asa de viga dupla · elemento superior', [-.40, -.2, 0, .2, .40], lambda x: wing_section((x, .432, -2.200), .15, 22, .10, -.04), m.carbon)
beam = join(ctx, [b1, b2], part='Asa de viga dupla (pista travada / chuva)')
spare(beam, 'beam_wing', 'dupla', 'rear_wing_bottom_holder__01', 'Asa de viga dupla (pista travada / chuva)')

# ----------------------------------------------------------------------------- arrefecimento: venezianas na tampa do motor
slats = []
for side in (-1, 1):
    x = side * .21
    for k in range(8):
        z = -.56 - k * .045
        y = surface_y(x, z)
        if y is None:
            continue
        slats.append(cube(ctx, f'Veneziana {k + 1} {lado(side, True)}', (x, y + .004, z), (.15, .003, .022), m.carbon_matte, rot=(35, 0, 0), bev=.0004))
    y0 = surface_y(x, -.56); y1 = surface_y(x, -.56 - 7 * .045)
    if y0 is not None and y1 is not None:
        slats.append(cube(ctx, f'Moldura das venezianas {lado(side, True)}', (x, (y0 + y1) / 2 + .001, -.56 - 3.5 * .045), (.17, .002, .40), m.carbon_matte, rot=(math.degrees(math.atan2(y1 - y0, -7 * .045)), 0, 0), bev=.0003))
assert len(slats) >= 12, f'poucas venezianas geradas ({len(slats)}): superfície da tampa não encontrada'
louvres = join(ctx, slats, part='Venezianas de arrefecimento da tampa do motor (calor)')
spare(louvres, 'cooling', 'aberto', 'main_body__01', 'Venezianas de arrefecimento (calor extremo)', mode='attach')

# ----------------------------------------------------------------------------- exportação
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in SPARES:
    o.parent = None
    o.select_set(True)
bpy.context.view_layer.objects.active = SPARES[0]
glb = OUT / 'sobressalentes-v1.glb'
bpy.ops.export_scene.gltf(filepath=str(glb), use_selection=True, export_format='GLB', export_apply=True, export_yup=True,
                          export_animations=False, export_extras=True, export_image_format='AUTO', export_materials='EXPORT',
                          export_cameras=False, export_lights=False, export_normals=True, export_texcoords=True, export_tangents=False)

def bbox_web(o):
    deps = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(deps)
    pts = [to_web(ev.matrix_world @ Vector(c)) for c in ev.bound_box]
    return [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]

entries = []
for o in SPARES:
    mn, mx = bbox_web(o)
    deps = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(deps)
    entries.append({'node': o.name, 'slot': o['slot'], 'variant': o['variant'], 'target': o['target'], 'mode': o['mode'], 'label': o['label'],
                    'min': [round(v, 4) for v in mn], 'max': [round(v, 4) for v in mx], 'triangles': sum(len(p.vertices) - 2 for p in ev.data.polygons)})
manifest = {
    'asset': glb.name, 'bytes': glb.stat().st_size, 'sha256': hashlib.sha256(glb.read_bytes()).hexdigest(),
    'generated_by': 'ferramentas/gerar_sobressalentes.py', 'blender': bpy.app.version_string,
    'slots': {
        'tyres': {'label': 'Pneus', 'variants': ['original'] + list(TYRE)},
        'rear_wing': {'label': 'Asa traseira', 'variants': ['original'] + list(REAR)},
        'front_wing': {'label': 'Flap dianteiro', 'variants': ['original'] + list(FRONT)},
        'beam_wing': {'label': 'Asa de viga', 'variants': ['original', 'dupla']},
        'cooling': {'label': 'Arrefecimento', 'variants': ['original', 'aberto']},
    },
    'entries': entries,
    'totals': {'nodes': len(entries), 'triangles': sum(e['triangles'] for e in entries)},
}
(OUT / 'sobressalentes-v1.manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')
print('SOBRESSALENTES_OK', glb.name, len(entries), 'nós', manifest['totals']['triangles'], 'triângulos', f'{manifest["bytes"] / 1e6:.2f} MB', f'{time.time() - started:.1f}s')
