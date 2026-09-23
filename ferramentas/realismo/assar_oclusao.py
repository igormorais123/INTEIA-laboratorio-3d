"""Assa oclusão de ambiente por vértice com Cycles/OptiX.

Entrada: arquivo de exportar_malhas.mjs (vértices na ordem do GLTFLoader).
Saída (formato AOV1): um byte por vértice, na mesma ordem, com a OCLUSÃO (0 = livre,
255 = fechado). O site usa 1 - oclusão; atributo ausente vale 0, ou seja,
peça sem bake nunca escurece.

blender -b --factory-startup --python assar_oclusao.py -- <in.bin> <out.bin> [distancia] [amostras] [piso]
"""
import bpy
import json
import struct
import sys
import time
import numpy as np

args = sys.argv[sys.argv.index('--') + 1:]
src, dst = args[0], args[1]
distance = float(args[2]) if len(args) > 2 else .35
samples = int(args[3]) if len(args) > 3 else 256
# Piso opcional (altura Y do site): a peça "sente" o chão, útil para motor e sistemas em bancada.
floor_y = float(args[4]) if len(args) > 4 and args[4] != 'none' else None
DOMAIN = args[5] if len(args) > 5 else 'CORNER'

t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == 'OPTIX'
assert any(d.use for d in prefs.devices), 'OptiX GPU required'
scene.cycles.device = 'GPU'
scene.cycles.samples = samples
scene.cycles.use_denoising = False
scene.world = bpy.data.worlds.new('AO world')
scene.world.light_settings.distance = distance

raw = open(src, 'rb').read()
hlen = struct.unpack_from('<I', raw, 0)[0]
header = json.loads(raw[4:4 + hlen])
off = 4 + hlen
# Todas as malhas num único objeto, na ordem do arquivo: um bake só (o Cycles prepara a cena por objeto,
# e 1.228 objetos levavam mais de 20 min). Cada malha continua sendo um intervalo contíguo de vértices.
positions, faces, counts = [], [], []
flipped = 0
base = 0
for m in header['meshes']:
    n, ni = m['vertices'], m['indices']
    pos = np.frombuffer(raw, np.float32, n * 3, off); off += n * 12
    nrm = np.frombuffer(raw, np.float32, n * 3, off).reshape(-1, 3); off += n * 12
    idx = np.frombuffer(raw, np.uint32, ni, off).reshape(-1, 3).astype(np.int64); off += ni * 4
    # Face cujo enrolamento contraria as normais de sombreamento do GLB é invertida:
    # o AO dispara raios pelo lado que o site realmente mostra.
    p3 = pos.reshape(-1, 3)
    face_n = np.cross(p3[idx[:, 1]] - p3[idx[:, 0]], p3[idx[:, 2]] - p3[idx[:, 0]])
    shade_n = nrm[idx[:, 0]] + nrm[idx[:, 1]] + nrm[idx[:, 2]]
    flip = (face_n * shade_n).sum(1) < 0
    idx[flip] = idx[flip][:, [0, 2, 1]]
    flipped += int(flip.sum())
    # Site (x, y, z) com Y para cima -> Blender (x, -z, y).
    positions.append(np.column_stack([p3[:, 0], -p3[:, 2], p3[:, 1]]).astype(np.float32))
    faces.append(idx + base)
    counts.append(n)
    base += n
verts = np.concatenate(positions)
tris = np.concatenate(faces).astype(np.int32)
me = bpy.data.meshes.new('conjunto')
me.vertices.add(len(verts))
me.vertices.foreach_set('co', verts.ravel())
me.loops.add(tris.size)
me.loops.foreach_set('vertex_index', tris.ravel())
me.polygons.add(len(tris))
me.polygons.foreach_set('loop_start', np.arange(0, tris.size, 3, dtype=np.int32))
me.polygons.foreach_set('loop_total', np.full(len(tris), 3, np.int32))
me.update(calc_edges=True)
assert len(me.vertices) == len(verts)
me.shade_smooth()
ob = bpy.data.objects.new('conjunto', me)
scene.collection.objects.link(ob)
attr = me.color_attributes.new('ao', 'FLOAT_COLOR', DOMAIN)
me.color_attributes.active_color = attr
me.materials.append(bpy.data.materials.new('ao'))

if floor_y is not None:
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, floor_y))

for o in scene.objects:
    o.select_set(o is ob)
bpy.context.view_layer.objects.active = ob
print(f'cena pronta {time.time() - t0:.1f}s; assando {len(counts)} malhas, {len(verts)} vértices')
bpy.ops.object.bake(type='AO', target='VERTEX_COLORS', margin=0, use_clear=True)
print(f'bake {time.time() - t0:.1f}s')

data = me.color_attributes['ao'].data
col = np.empty(len(data) * 4, np.float32)
data.foreach_get('color', col)
ao = col[0::4]
if DOMAIN == 'CORNER':
    # Média dos cantos de cada vértice: amostras dentro das faces vizinhas.
    vi = np.empty(len(me.loops), np.int32)
    me.loops.foreach_get('vertex_index', vi)
    acc = np.bincount(vi, ao, len(me.vertices))
    cnt = np.bincount(vi, None, len(me.vertices))
    ao = np.where(cnt > 0, acc / np.maximum(cnt, 1), 1.0)
occlusion = np.clip(np.round((1 - ao) * 255), 0, 255).astype(np.uint8)
stats = [float(a.mean()) for a in np.split(ao, np.cumsum(counts)[:-1])]
# Formato AOV1: 'AOV1', uint32 malhas, uint32 vértices por malha, bytes de oclusão.
open(dst, 'wb').write(b'AOV1' + struct.pack('<I', len(counts)) + np.array(counts, np.uint32).tobytes() + occlusion.tobytes())
print(json.dumps({'meshes': len(counts), 'vertices': int(len(occlusion)),
                  'meanAO': round(float(np.mean(stats)), 3), 'flippedFaces': flipped, 'seconds': round(time.time() - t0, 1),
                  'distance': distance, 'samples': samples, 'floor': floor_y,
                  'device': [d.name for d in prefs.devices if d.use]}))
