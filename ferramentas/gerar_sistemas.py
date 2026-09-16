"""Gera o asset dos sistemas internos do carro (web/assets/sistemas-v1.glb) com Blender 5.2.

Uso:
  blender -b --python ferramentas/gerar_sistemas.py                # todos os sistemas
  SISTEMAS=brakes,power blender -b --python ferramentas/gerar_sistemas.py
  PREVIEW=1 ... gera renders de conferência em ferramentas/sistemas/previews/

Convenções: cada módulo `ferramentas/sistemas/sNN_<id>.py` expõe SYSTEM=(id, rótulo) e build(ctx).
Todo o posicionamento usa o referencial do site (glTF: Y para cima, Z para a frente, metros).
O exportador converte o referencial e grava os extras (part, spin, flow, era, explode) nos nós.
"""
import bpy, os, sys, json, math, hashlib, importlib, subprocess, time
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SYS_DIR = ROOT / 'ferramentas' / 'sistemas'
OUT = ROOT / 'web' / 'assets'
PREVIEW_DIR = SYS_DIR / 'previews'
sys.path.insert(0, str(SYS_DIR))
import lib
importlib.reload(lib)

started = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene['authorship'] = 'Geometria original INTEIA; camada didática dos sistemas internos, não CAD de fabricante.'

mats = lib.Materials()
ctx = lib.Context(scene, mats)

# ----------------------------------------------------------------------------- referência: carro e motor
_reference = []
CAR_GLB = OUT / 'carro-aula-v2.glb'
POWER_GLB = OUT / 'power-unit-v1.glb'
ICE_CENTER = (0, .43, -.92)     # centro do V6 na camada Sistemas (site frame)
ICE_LENGTH = .85                # mesmo comprimento usado pelo compartimento do motor

def _import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    return [o for o in bpy.data.objects if o not in before]

def _bbox(objs):
    deps = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in objs:
        if o.type != 'MESH':
            continue
        ev = o.evaluated_get(deps)
        pts += [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    if not pts:
        return None
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
    return lo, hi

def import_car_reference(alpha=.045):
    """Carro fantasma para os renders de conferência (não exportado)."""
    objs = _import_glb(CAR_GLB)
    lo, hi = _bbox(objs)
    center = (lo + hi) / 2
    root = bpy.data.objects.new('ref_car', None); scene.collection.objects.link(root)
    for o in objs:
        if o.parent is None:
            o.parent = root
    root.location = Vector((-center.x, -center.y, -lo.z))
    ghost = lib.material('Referência · carro fantasma', (.55, .58, .6), 0, .6, alpha=alpha)
    for o in objs:
        if o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(ghost)
    _reference.extend(objs + [root])
    return root

_power_ref = {}
def power_unit_reference():
    """Importa power-unit-v1.glb na pose da camada Sistemas e devolve bounds por conjunto (site frame)."""
    if _power_ref:
        return _power_ref
    objs = _import_glb(POWER_GLB)
    lo, hi = _bbox(objs)
    size = hi - lo
    scale = ICE_LENGTH / max(size)
    center = (lo + hi) / 2
    root = bpy.data.objects.new('ref_power_unit', None); scene.collection.objects.link(root)
    for o in objs:
        if o.parent is None:
            o.parent = root
    root.scale = (scale, scale, scale)
    root.location = lib.W(ICE_CENTER) - center * scale
    bpy.context.view_layer.update()
    groups = {}
    for o in objs:
        if o.type == 'EMPTY' and o.name.startswith('assembly_'):
            meshes = [c for c in o.children_recursive if c.type == 'MESH']
            bb = _bbox(meshes)
            if bb:
                groups[o.name.split('.')[0]] = (lib.to_web(bb[0]) if False else None, bb)
    result = {'scale': scale, 'root': root, 'assemblies': {}}
    for name, (_, (lo2, hi2)) in groups.items():
        # bounds em site frame: x=x, y=z_blender, z=-y_blender
        result['assemblies'][name] = {'min': (lo2.x, lo2.z, -hi2.y), 'max': (hi2.x, hi2.z, -lo2.y)}
    bb = _bbox([o for o in objs if o.type == 'MESH'])
    result['bounds'] = {'min': (bb[0].x, bb[0].z, -bb[1].y), 'max': (bb[1].x, bb[1].z, -bb[0].y)}
    _reference.extend(objs + [root])
    _power_ref.update(result)
    return _power_ref

ctx.power_unit_reference = power_unit_reference
ctx.ICE_CENTER = ICE_CENTER
ctx.ICE_LENGTH = ICE_LENGTH

# ----------------------------------------------------------------------------- módulos
wanted = [s.strip() for s in os.environ.get('SISTEMAS', '').split(',') if s.strip()]
modules = sorted(p.stem for p in SYS_DIR.glob('s[0-9][0-9]_*.py'))
built = []
shots = {}
for name in modules:
    mod = importlib.import_module(name)
    importlib.reload(mod)
    sid, label = mod.SYSTEM
    if wanted and sid not in wanted:
        continue
    t0 = time.time()
    ctx.system(sid, label)
    mod.build(ctx)
    lib.auto_explode(ctx, sid)
    # Convenção de lados: o piloto olha para +Z, logo a esquerda real é +X. Módulos escritos antes dessa
    # correção (sem X_CONVENTION) rotulam −X como esquerda e são espelhados no lugar.
    if getattr(mod, 'X_CONVENTION', 'legado') == 'legado':
        lib.mirror_system(ctx, sid)
    built.append(sid)
    shots[sid] = getattr(mod, 'SHOTS', {})
    print(f'SISTEMA {sid}: {sum(1 for p in ctx.parts if p.get("system") == sid)} peças em {time.time() - t0:.1f}s')

# ----------------------------------------------------------------------------- exportação
bpy.context.view_layer.update()
export_objects = []
for sid, empty in ctx.systems.items():
    export_objects.append(empty)
    export_objects += [c for c in empty.children_recursive]
bpy.ops.object.select_all(action='DESELECT')
for o in export_objects:
    o.select_set(True)
bpy.context.view_layer.objects.active = export_objects[0]

suffix = ('-' + '-'.join(built)) if wanted else ''
# Builds parciais (SISTEMAS=...) ficam fora de web/assets; só o asset completo é publicado.
glb = (OUT if not wanted else PREVIEW_DIR) / f'sistemas-v1{suffix}.glb'
glb.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(glb), use_selection=True, export_format='GLB', export_apply=True,
                          export_yup=True, export_animations=False, export_extras=True, export_image_format='AUTO',
                          export_materials='EXPORT', export_cameras=False, export_lights=False, export_normals=True,
                          export_texcoords=True, export_tangents=False)
raw_bytes = glb.stat().st_size

# ----------------------------------------------------------------------------- manifesto
def measure_glb(path):
    raw = path.read_bytes()
    chunklen = int.from_bytes(raw[12:16], 'little')
    gltf = json.loads(raw[20:20 + chunklen])
    # Triângulos renderizados: soma por nó (instância), não por malha única (o otimizador deduplica malhas iguais).
    per_mesh = [sum(gltf['accessors'][p['indices']]['count'] // 3 for p in m['primitives'] if 'indices' in p) for m in gltf.get('meshes', [])]
    tris = sum(per_mesh[n['mesh']] for n in gltf.get('nodes', []) if 'mesh' in n)
    return raw, gltf, tris

deps = bpy.context.evaluated_depsgraph_get()
systems_manifest = {}
for sid, empty in ctx.systems.items():
    parts = [p for p in ctx.parts if p.get('system') == sid]
    entries = []
    for p in parts:
        ev = p.evaluated_get(deps)
        pts = [ev.matrix_world @ Vector(c) for c in ev.bound_box]
        lo = [min(q[i] for q in pts) for i in range(3)]; hi = [max(q[i] for q in pts) for i in range(3)]
        entry = {'node': p.name, 'part': p['part'], 'min': [round(lo[0], 4), round(lo[2], 4), round(-hi[1], 4)], 'max': [round(hi[0], 4), round(hi[2], 4), round(-lo[1], 4)],
                 'triangles': sum(len(poly.vertices) - 2 for poly in ev.data.polygons)}
        for k in ('spin', 'spin_axis', 'flow', 'era', 'explode', 'hide_group', 'tag'):
            if k in p:
                v = p[k]
                entry[k] = list(v) if hasattr(v, '__len__') and not isinstance(v, str) else v
        entries.append(entry)
    systems_manifest[sid] = {'label': empty['label'], 'parts': len(entries), 'triangles': sum(e['triangles'] for e in entries), 'nodes': entries}

def write_manifest(path_glb, optimized):
    raw, gltf, tris = measure_glb(path_glb)
    manifest = {
        'name': 'Sistemas internos do carro · camada didática INTEIA',
        'version': 1,
        'authorship': 'Geometria procedural original INTEIA (Blender 5.2 + bpy); sem CAD de fabricante.',
        'scope': 'Catorze sistemas em escala do carro v2, com materiais físicos e peças nomeadas; representação didática, não engenharia ou homologação.',
        'units': 'metres', 'axes': 'glTF Y up, longitudinal Z (frente = +Z)',
        'ice_center': list(ICE_CENTER), 'ice_length': ICE_LENGTH,
        'systems': systems_manifest,
        'totals': {'systems': len(systems_manifest), 'parts': sum(s['parts'] for s in systems_manifest.values()), 'triangles': tris,
                   'meshes': len(gltf.get('meshes', [])), 'nodes': len(gltf.get('nodes', [])), 'materials': len(gltf.get('materials', [])),
                   'images': len(gltf.get('images', [])), 'bytes': len(raw), 'raw_bytes': raw_bytes},
        'extensions_required': gltf.get('extensionsRequired', []),
        'extensions_used': gltf.get('extensionsUsed', []),
        'optimized': optimized,
        'sha256': hashlib.sha256(raw).hexdigest(),
        'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'library_sha256': hashlib.sha256((SYS_DIR / 'lib.py').read_bytes()).hexdigest(),
        'license': '© 2026 INTEIA — todos os direitos reservados; geometria didática original.',
    }
    (glb.parent / f'sistemas-v1{suffix}.manifest.json').write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding='utf-8')
    return manifest

optimized = False
tool_root = os.environ.get('F1_ASSET_TOOL_ROOT') or str(Path(os.environ.get('TEMP', '/tmp')) / 'claude' / 'f1-assets')
if os.environ.get('OTIMIZAR', '1') != '0' and Path(tool_root, 'node_modules').exists():
    env = dict(os.environ); env['F1_ASSET_TOOL_ROOT'] = tool_root; env['SISTEMAS_GLB'] = str(glb)
    try:
        subprocess.run(['node', str(ROOT / 'ferramentas' / 'otimizar_sistemas.mjs')], check=True, env=env)
        optimized = True
    except Exception as e:
        print('OTIMIZACAO_FALHOU', e)
manifest = write_manifest(glb, optimized)
print('SISTEMAS_MANIFEST', json.dumps({k: manifest[k] for k in ('totals', 'extensions_required', 'optimized')}))

# ----------------------------------------------------------------------------- renders de conferência
if os.environ.get('PREVIEW'):
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    car = import_car_reference()
    for o in _reference:
        o.hide_render = False
    # iluminação de estúdio
    world = bpy.data.worlds.new('Estúdio'); scene.world = world; world.use_nodes = True
    bg = world.node_tree.nodes['Background']; bg.inputs[0].default_value = (.36, .37, .39, 1); bg.inputs[1].default_value = .55
    def light(name, kind, loc, energy, size=2.0):
        l = bpy.data.lights.new(name, kind); l.energy = energy
        if kind == 'AREA':
            l.size = size
        o = bpy.data.objects.new(name, l); scene.collection.objects.link(o); o.location = lib.W(loc)
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (-lib.W(loc)).normalized().to_track_quat('-Z', 'Y')
        return o
    light('Chave', 'AREA', (3, 4, 3), 900, 3); light('Preenchimento', 'AREA', (-4, 3, -1), 420, 4); light('Contra', 'AREA', (1, 3.5, -4), 700, 2.5)
    light('Sol', 'SUN', (2, 6, 2), .9)
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except TypeError:
        scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280; scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'AgX'
    cam_data = bpy.data.cameras.new('Câmera'); cam_data.lens = 40
    cam = bpy.data.objects.new('Câmera', cam_data); scene.collection.objects.link(cam); scene.camera = cam
    def frame(objs, direction, pad=1.25):
        bb = _bbox(objs)
        if not bb:
            return
        lo, hi = bb; center = (lo + hi) / 2; radius = (hi - lo).length / 2
        d = lib.W(direction).normalized()
        dist = radius * pad / math.tan(cam_data.angle / 2)
        cam.location = center + d * dist
        cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = d.to_track_quat('Z', 'Y')
    views = {'hero': (1, .45, 1.1), 'side': (1, .15, 0), 'top': (.001, 1, .05), 'rear': (.6, .3, -1)}
    for sid, empty in ctx.systems.items():
        for s2, e2 in ctx.systems.items():
            e2.hide_render = s2 != sid
            for c in e2.children_recursive:
                c.hide_render = s2 != sid
        meshes = [c for c in empty.children_recursive if c.type == 'MESH']
        for vname in [v for v in os.environ.get('VISTAS', 'hero,side').split(',') if v in views]:
            frame(meshes, views[vname])
            scene.render.filepath = str(PREVIEW_DIR / f'{sid}-{vname}.png')
            bpy.ops.render.render(write_still=True)
        # detalhes definidos pelo módulo: nome -> (centro, raio, direção), tudo no referencial do site
        for sname, (center, radius, direction) in shots.get(sid, {}).items():
            d = lib.W(direction).normalized()
            cam.location = lib.W(center) + d * (radius * 1.15 / math.tan(cam_data.angle / 2))
            cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = d.to_track_quat('Z', 'Y')
            scene.render.filepath = str(PREVIEW_DIR / f'{sid}-{sname}.png')
            bpy.ops.render.render(write_still=True)
    for e2 in ctx.systems.values():
        e2.hide_render = False
        for c in e2.children_recursive:
            c.hide_render = False
    all_meshes = [c for e in ctx.systems.values() for c in e.children_recursive if c.type == 'MESH']
    frame(all_meshes, views['hero'], 1.05)
    scene.render.filepath = str(PREVIEW_DIR / 'overview-hero.png'); bpy.ops.render.render(write_still=True)
    print('PREVIEWS', str(PREVIEW_DIR))

if os.environ.get('SALVAR_BLEND'):
    bpy.ops.wm.save_as_mainfile(filepath=str(SYS_DIR / 'previews' / 'sistemas-trabalho.blend'))
print(f'SISTEMAS_OK {glb.name} {len(ctx.parts)} peças {time.time() - started:.1f}s')
