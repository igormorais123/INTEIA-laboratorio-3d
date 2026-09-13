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
     node.inputs['Roughness'].default_value=.29
     node.inputs['Metallic'].default_value=0
     node.inputs['Coat Weight'].default_value=1
     node.inputs['Coat Roughness'].default_value=.12
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=64
scene.world=bpy.data.worlds.new('Workshop ambient');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.24,.28,.32,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
for i,y in enumerate([-3,0,3]):
 data=bpy.data.lights.new('Workshop softbox '+str(i),'AREA');data.energy=300;data.shape='RECTANGLE';data.size=4.4;data.size_y=.8
 obj=bpy.data.objects.new(data.name,data);scene.collection.objects.link(obj);obj.location=(0,y,3.2)
camdata=bpy.data.cameras.new('Camera | Box geral');cam=bpy.data.objects.new(camdata.name,camdata);scene.collection.objects.link(cam);cam.location=(4.7,-5.0,2.5);direction=Vector((0,1.0,.9))-cam.location;cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();camdata.lens=25;scene.camera=cam
scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.35
scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene['description']='Box-laboratorio INTEIA. Original environment inspired by public F1 garages, not an exact team replica. No real telemetry.'
scene['web_source']='web/src/garage.js'
bpy.ops.file.pack_all()
out=repo/'ambientes/INTEIA_Box_com_carro.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
report={'blend':out.name,'garage_meshes':len([o for o in box_collection.objects if o.type=='MESH']),'car_meshes':len(mesh_objects),'car_original_bounds':[list(lo),list(hi)],'packed_images':len([im for im in bpy.data.images if im.packed_file]),'external_images':[im.filepath for im in bpy.data.images if im.source=='FILE' and not im.packed_file]}
(repo/'ambientes/validacao-box.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
