"""Prévia do bake: mostra a oclusão como cor emissiva, de quatro ângulos.

blender -b --factory-startup --python previa_oclusao.py -- <malhas.bin> <ao.bin> <prefixo_png>
"""
import bpy
import json
import math
import struct
import sys
import numpy as np
from mathutils import Vector

args = sys.argv[sys.argv.index('--') + 1:]
src, ao_path, prefix = args[:3]
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x, scene.render.resolution_y = 1200, 700
scene.world = bpy.data.worlds.new('w')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.35, .45, .6, 1)
scene.view_settings.view_transform = 'Standard'

mat = bpy.data.materials.new('ao')
mat.use_nodes = True
nt = mat.node_tree
nt.nodes.clear()
attr = nt.nodes.new('ShaderNodeVertexColor'); attr.layer_name = 'ao'
em = nt.nodes.new('ShaderNodeEmission')
out = nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(attr.outputs['Color'], em.inputs['Color'])
nt.links.new(em.outputs['Emission'], out.inputs['Surface'])

raw = open(src, 'rb').read()
hlen = struct.unpack_from('<I', raw, 0)[0]
header = json.loads(raw[4:4 + hlen])
blob = open(ao_path, 'rb').read()
count = struct.unpack_from('<I', blob, 4)[0] if blob[:4] == b'AOV1' else None
occl = np.frombuffer(blob, np.uint8, offset=8 + 4 * count) if count is not None else np.frombuffer(blob, np.uint8)
off, vo = 4 + hlen, 0
lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
for k, m in enumerate(header['meshes']):
    n, ni = m['vertices'], m['indices']
    p = np.frombuffer(raw, np.float32, n * 3, off).reshape(-1, 3); off += n * 24
    idx = np.frombuffer(raw, np.uint32, ni, off); off += ni * 4
    bl = np.column_stack([p[:, 0], -p[:, 2], p[:, 1]]).astype(np.float32)
    me = bpy.data.meshes.new(m['name'])
    me.from_pydata(bl.tolist(), [], idx.reshape(-1, 3).tolist())
    a = 1 - occl[vo:vo + n] / 255.0; vo += n
    ca = me.color_attributes.new('ao', 'FLOAT_COLOR', 'POINT')
    ca.data.foreach_set('color', np.column_stack([a, a, a, np.ones(n)]).astype(np.float32).ravel())
    me.materials.append(mat)
    ob = bpy.data.objects.new(me.name, me)
    scene.collection.objects.link(ob)
    for c in bl.min(0), bl.max(0):
        lo = Vector(np.minimum(lo, c)); hi = Vector(np.maximum(hi, c))

center = (lo + hi) / 2
size = (hi - lo).length
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
cam.data.lens = 50
scene.collection.objects.link(cam)
scene.camera = cam
for name, d in {'34': (1.1, -1.2, .55), 'topo': (.05, -.25, 1), 'lado': (1, 0, .12), 'traseira': (-.6, 1, .5)}.items():
    direction = Vector(d).normalized()
    cam.location = center + direction * size * 1.05
    cam.rotation_euler = (center - cam.location).to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = f'{prefix}-{name}.png'
    bpy.ops.render.render(write_still=True)
