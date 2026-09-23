"""Assa a sombra de contato do carro num plano de piso, com Cycles/OptiX.

Mesma entrada de assar_oclusao.py. O plano fica sob o carro, na altura do ponto
mais baixo, com margem; a textura guarda a OCLUSÃO do céu sobre o piso
(0 = piso livre, 255 = encoberto). Saída: PNG em tons de cinza e JSON com os
limites do plano no referencial do GLB (Y para cima).

blender -b --factory-startup --python assar_sombra.py -- <malhas.bin> <saida.png> [margem] [distancia] [amostras] [px_por_metro]
Depois: python gravar_sombra.py <saida.png> (converte o .npy em PNG de 8 bits).
"""
import bpy
import json
import struct
import sys
import time
import numpy as np

args = sys.argv[sys.argv.index('--') + 1:]
src, dst = args[0], args[1]
margin = float(args[2]) if len(args) > 2 else .9
distance = float(args[3]) if len(args) > 3 else 1.4
samples = int(args[4]) if len(args) > 4 else 512
density = float(args[5]) if len(args) > 5 else 128

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
lo, hi = np.full(3, 1e9), np.full(3, -1e9)
for k, m in enumerate(header['meshes']):
    n, ni = m['vertices'], m['indices']
    p = np.frombuffer(raw, np.float32, n * 3, off).reshape(-1, 3); off += n * 24
    idx = np.frombuffer(raw, np.uint32, ni, off); off += ni * 4
    bl = np.column_stack([p[:, 0], -p[:, 2], p[:, 1]]).astype(np.float32)
    lo, hi = np.minimum(lo, bl.min(0)), np.maximum(hi, bl.max(0))
    me = bpy.data.meshes.new(m['name'])
    me.from_pydata(bl.tolist(), [], idx.reshape(-1, 3).tolist())
    scene.collection.objects.link(bpy.data.objects.new(me.name, me))

x0, x1 = lo[0] - margin, hi[0] + margin
y0, y1 = lo[1] - margin, hi[1] + margin
z = lo[2] + .0005
width, height = int(round((x1 - x0) * density / 8) * 8), int(round((y1 - y0) * density / 8) * 8)
me = bpy.data.meshes.new('floor')
me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [(0, 1, 2, 3)])
uv = me.uv_layers.new(name='UV')
for loop, co in zip(uv.data, [(0, 0), (1, 0), (1, 1), (0, 1)]):
    loop.uv = co
floor = bpy.data.objects.new('floor', me)
scene.collection.objects.link(floor)
image = bpy.data.images.new('shadow', width, height, float_buffer=True, is_data=True)
mat = bpy.data.materials.new('floor')
node = mat.node_tree.nodes.new('ShaderNodeTexImage')
node.image = image
mat.node_tree.nodes.active = node
me.materials.append(mat)

for o in scene.objects:
    o.select_set(o is floor)
bpy.context.view_layer.objects.active = floor
bpy.ops.object.bake(type='AO', margin=2)
px = np.empty(width * height * 4, np.float32)
image.pixels.foreach_get(px)
occl = 1 - px[0::4].reshape(height, width)
# Borda do plano chega a zero para não recortar a sombra contra o piso.
fade = np.minimum.outer(np.minimum(np.linspace(0, 1, height), np.linspace(1, 0, height)),
                        np.minimum(np.linspace(0, 1, width), np.linspace(1, 0, width)))
occl *= np.clip(fade / .12, 0, 1)
gray = np.clip(occl, 0, 1)
# Linha 0 do Blender é a base da imagem (v = 0); o PNG começa pelo topo.
np.save(dst.rsplit('.', 1)[0] + '.npy', gray[::-1].copy())
# Limites no referencial do GLB: Blender (x, y, z) -> site (x, z, -y).
meta = {'minX': float(x0), 'maxX': float(x1), 'minZ': float(-y1), 'maxZ': float(-y0), 'y': float(lo[2]),
        'width': width, 'height': height, 'distance': distance, 'samples': samples,
        'maxOcclusion': round(float(gray.max()), 3), 'seconds': round(time.time() - t0, 1),
        'device': [d.name for d in prefs.devices if d.use]}
open(dst.rsplit('.', 1)[0] + '.json', 'w').write(json.dumps(meta, indent=1))
print(json.dumps(meta))
