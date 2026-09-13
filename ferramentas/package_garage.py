import bpy, sys, json
from pathlib import Path
from mathutils import Vector
repo=Path(sys.argv[sys.argv.index('--')+1])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(repo/'ambientes/INTEIA-box-laboratorio.glb'))
box_collection=bpy.data.collections.new('INTEIA | BOX E EQUIPAMENTOS');bpy.context.scene.collection.children.link(box_collection)
for obj in list(bpy.context.scene.objects):
 for collection in list(obj.users_collection):collection.objects.unlink(obj)
 box_collection.objects.link(obj)
before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(repo/'modelos/INTEIA_F1_estatico.glb'))
car_objects=[o for o in bpy.data.objects if o not in before]
car_collection=bpy.data.collections.new('INTEIA | CARRO');bpy.context.scene.collection.children.link(car_collection)
for obj in car_objects:
 for collection in list(obj.users_collection):collection.objects.unlink(obj)
 car_collection.objects.link(obj)
mesh_objects=[o for o in car_objects if o.type=='MESH']
coords=[o.matrix_world@Vector(c) for o in mesh_objects for c in o.bound_box]
lo=Vector(tuple(min(v[i] for v in coords) for i in range(3)));hi=Vector(tuple(max(v[i] for v in coords) for i in range(3)))
shift=Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z))
for o in car_objects:
 if o.parent not in car_objects:o.location+=shift
for obj in mesh_objects:
 for m in obj.data.materials:
  if m and 'pintura' in m.name.lower() and m.use_nodes:
   for node in m.node_tree.nodes:
    if node.type=='BSDF_PRINCIPLED':
     node.inputs['Base Color'].default_value=(.617,0,.007,1)
     for channel in ['Base Color','Roughness','Metallic','Normal','Coat Normal']:
      for link in list(node.inputs[channel].links):m.node_tree.links.remove(link)
     node.inputs['Roughness'].default_value=.21
     node.inputs['Metallic'].default_value=0
     node.inputs['Coat Weight'].default_value=1
     node.inputs['Coat Roughness'].default_value=.065
# Physical surface detail, independent of the web renderer.
for m in bpy.data.materials:
 if not m.use_nodes:continue
 bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if not bs:continue
 name=m.name.lower()
 if name in ['pneus','borracha']:
  for key in ['Base Color','Roughness','Normal']:
   for link in list(bs.inputs[key].links):m.node_tree.links.remove(link)
  bs.inputs['Base Color'].default_value=(.014,.016,.019,1);bs.inputs['Roughness'].default_value=.64
  noise=m.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=480;noise.inputs['Detail'].default_value=2
  bump=m.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.00035
  m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
 if name=='aço':bs.inputs['Metallic'].default_value=1;bs.inputs['Roughness'].default_value=.25
 # Shading-only bevel preserves geometry and articulation while catching edge light.
 if bs.inputs['Metallic'].default_value>.65 and not bs.inputs['Normal'].is_linked:
  bevel=m.node_tree.nodes.new('ShaderNodeBevel');bevel.inputs['Radius'].default_value=.0008;bevel.samples=2;m.node_tree.links.new(bevel.outputs['Normal'],bs.inputs['Normal'])
# Remove imported directional lights; the Blender rig uses finite workshop sources.
for obj in list(bpy.context.scene.objects):
 if obj.type=='LIGHT':bpy.data.objects.remove(obj,do_unlink=True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=128
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.015
scene.cycles.max_bounces=10;scene.cycles.glossy_bounces=6
scene.world=bpy.data.worlds.new('Workshop ambient');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.24,.28,.32,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.18
for i,y in enumerate([-3,0,3]):
 data=bpy.data.lights.new('Workshop softbox '+str(i),'AREA');data.energy=180;data.shape='RECTANGLE';data.size=4.4;data.size_y=.8
 obj=bpy.data.objects.new(data.name,data);scene.collection.objects.link(obj);obj.location=(0,y,3.2)
for i,x in enumerate([-3.8,3.8]):
 data=bpy.data.lights.new('Bodywork reflection strip '+str(i),'AREA');data.energy=140;data.shape='RECTANGLE';data.size=5;data.size_y=1.1
 obj=bpy.data.objects.new(data.name,data);scene.collection.objects.link(obj);obj.location=(x,0,2.6);obj.rotation_euler=(Vector((0,0,.65))-obj.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('Camera | Box geral');cam=bpy.data.objects.new(camdata.name,camdata);scene.collection.objects.link(cam);cam.location=(4.4,-5.8,2.1);direction=Vector((0,.5,.85))-cam.location;cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();camdata.lens=30;scene.camera=cam
scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.65
scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene['description']='Box-laboratorio INTEIA. Original environment inspired by public F1 garages, not an exact team replica. No real telemetry.'
scene['web_source']='web/src/garage.js'
bpy.ops.file.pack_all()
out=repo/'ambientes/INTEIA_Box_com_carro.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
report={'blend':out.name,'garage_meshes':len([o for o in box_collection.objects if o.type=='MESH']),'car_meshes':len(mesh_objects),'car_original_bounds':[list(lo),list(hi)],'packed_images':len([im for im in bpy.data.images if im.packed_file]),'external_images':[im.filepath for im in bpy.data.images if im.source=='FILE' and not im.packed_file]}
(repo/'ambientes/validacao-box.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
