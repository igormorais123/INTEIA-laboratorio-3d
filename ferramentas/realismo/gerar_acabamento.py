"""Generate the shared web lighting probe and lacquer maps with Cycles/OptiX.

Run in an isolated Blender --background --factory-startup process. No source
car is changed: geometry, part IDs and the lesson's assembly rig are preserved.
"""
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'web' / 'assets'
scene = bpy.context.scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
for device in prefs.devices:
    device.use = device.type == 'OPTIX'
assert any(d.use for d in prefs.devices), 'OptiX GPU required'
scene.cycles.device = 'GPU'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6
scene.render.resolution_percentage = 100
scene.world.use_nodes = True
world = next(n for n in scene.world.node_tree.nodes if n.type == 'BACKGROUND')
world.inputs['Color'].default_value = (.12, .15, .2, 1)
world.inputs['Strength'].default_value = .12

def material(name, color, roughness=.5, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = roughness
    if emission:
        p.inputs['Emission Color'].default_value = (*color, 1)
        p.inputs['Emission Strength'].default_value = emission
    return m

def box(name, size, pos, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = bpy.context.object
    o.name = name
    o.scale = size
    o.data.materials.append(mat)
    return o

wall = material('Neutral bay walls', (.19,.21,.23), .72)
floor = material('Epoxy bounce', (.095,.11,.12), .38)
dark = material('Negative fill / graphite', (.009,.012,.016), .7)
white = material('Ceiling diffusion', (.92,.96,1), emission=7)
warm = material('Warm edge diffusion', (1,.82,.65), emission=4)
box('Floor',(12,14,.1),(0,0,-.06),floor)
box('Ceiling',(12,14,.1),(0,0,3.85),wall)
box('Rear wall',(12,.1,3.8),(0,6.5,1.9),wall)
box('Left wall',(.1,14,3.8),(-5.5,0,1.9),wall)
box('Right wall',(.1,14,3.8),(5.5,0,1.9),dark)
for y in [-3,-.6,1.8,4.2]:
    box('Ceiling softbox',(4.4,.42,.02),(0,y,3.22),white)
box('Front soft fill',(8,.035,2.8),(0,-6,2.2),material('Daylight fill',(.8,.9,1),emission=1.2))
box('Side strip',(.025,6,1.1),(-4.6,0,2.3),white)
box('Rear edge',(6,.025,.28),(0,6,2.7),warm)
for x in [-3,0,3]:
    box('Rear cabinets',(2.7,.8,1.1),(x,5.8,.6),dark)
    box('Monitor',(1.4,.04,.7),(x,5.32,1.8),material('Screen '+str(x),(.06,.13,.21),emission=.6))
bpy.ops.object.camera_add(location=(0,0,.75))
camera = bpy.context.object
camera.rotation_euler = (math.pi/2,0,0)
camera.data.type = 'PANO'
camera.data.panorama_type = 'EQUIRECTANGULAR'
scene.camera = camera
scene.render.resolution_x = 2048
scene.render.resolution_y = 1024
scene.render.image_settings.file_format = 'HDR'
scene.view_settings.view_transform = 'Standard'
scene.render.filepath = str(OUT / 'pitlane-cycles.hdr')
bpy.ops.wm.save_as_mainfile(filepath=str(Path(__file__).parent / 'pitlane-lighting.blend'))
bpy.ops.render.render(write_still=True)
mobile_probe = bpy.data.images.load(str(OUT / 'pitlane-cycles.hdr'))
mobile_probe.scale(1024, 512)
mobile_probe.filepath_raw = str(OUT / 'pitlane-cycles-mobile.hdr')
mobile_probe.file_format = 'HDR'
mobile_probe.save()

# Bake seamless three-dimensional lacquer noise, instead of regular sine waves.
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_plane_add(size=2, location=(0,0,8))
plane = bpy.context.object
mat = material('Lacquer microsurface',(.4,.4,.4))
plane.data.materials.append(mat)
nodes, links = mat.node_tree.nodes, mat.node_tree.links
p = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
tex = nodes.new('ShaderNodeTexNoise')
tex.noise_dimensions = '4D'
tex.inputs['Scale'].default_value = 38
tex.inputs['Detail'].default_value = 3
tex.inputs['Roughness'].default_value = .65
coords = nodes.new('ShaderNodeTexCoord')
# Periodic torus mapping makes opposite tile edges meet without seams.
sep = nodes.new('ShaderNodeSeparateXYZ')
links.new(coords.outputs['UV'], sep.inputs[0])
combine = nodes.new('ShaderNodeCombineXYZ')
for axis, trig, dest in [('X','SINE','X'),('X','COSINE','Y'),('Y','SINE','Z')]:
    scale=nodes.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=2*math.pi
    wave=nodes.new('ShaderNodeMath');wave.operation=trig
    links.new(sep.outputs[axis],scale.inputs[0]);links.new(scale.outputs[0],wave.inputs[0]);links.new(wave.outputs[0],combine.inputs[dest])
links.new(combine.outputs[0],tex.inputs['Vector'])
scale=nodes.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=2*math.pi
wave=nodes.new('ShaderNodeMath');wave.operation='COSINE'
links.new(sep.outputs['Y'],scale.inputs[0]);links.new(scale.outputs[0],wave.inputs[0]);links.new(wave.outputs[0],tex.inputs['W'])
bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.2;bump.inputs['Distance'].default_value=.015
links.new(tex.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],p.inputs['Normal'])
scene.cycles.samples=16
scene.render.bake.margin=8
image_node=nodes.new('ShaderNodeTexImage');nodes.active=image_node
for kind in ['normal','roughness']:
    im=bpy.data.images.new('Lacquer '+kind,512,512,alpha=False)
    im.colorspace_settings.name='Non-Color'
    image_node.image=im
    if kind=='roughness':
        ramp=nodes.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=.65;ramp.inputs['To Max'].default_value=1
        links.new(tex.outputs['Fac'],ramp.inputs['Value']);links.new(ramp.outputs[0],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=1
    bpy.ops.object.bake(type='NORMAL' if kind=='normal' else 'EMIT')
    im.filepath_raw=str(OUT / ('lacquer-cycles-'+kind+'.png'));im.file_format='PNG';im.save()

report={'blender':bpy.app.version_string,'engine':'Cycles','device':'OPTIX',
        'gpu':[d.name for d in prefs.devices if d.use],'hdri':[2048,1024],
        'samples':96,'maps':[512,512],'source':'Procedural original INTEIA bay; no third-party assets',
        'geometryModified':False}
(Path(__file__).parent/'generation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('REALISM_COMPLETE',json.dumps(report))
