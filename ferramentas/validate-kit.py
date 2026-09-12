import bpy,json,struct,os
from mathutils import Vector
from pathlib import Path
ROOT=str(Path(__file__).resolve().parents[1])
bpy.ops.wm.open_mainfile(filepath=ROOT+'/INTEIA_F1_Master.blend')
s=bpy.context.scene;meshes=[o for o in s.objects if o.get('INTEIA_componente')]
def matrices():
    bpy.context.view_layer.update();return {o.name:o.matrix_world.copy() for o in meshes}
s.frame_set(1);first=matrices();s.frame_set(90);moved=sum((o.matrix_world.translation-first[o.name].translation).length>.01 for o in meshes)
s.frame_set(210);end=matrices();error=max(abs(end[n][r][c]-first[n][r][c]) for n in first for r in range(4) for c in range(4))
triangles=0
for o in meshes:o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
assert len(meshes)==97 and moved==97 and error<1e-5
report={'blend_reopened':True,'components':len(meshes),'triangles':triangles,'components_moved_frame90':moved,'reassembly_matrix_error_frame210':error,'images_missing':[i.name for i in bpy.data.images if i.source=='FILE' and not i.packed_file and not os.path.isfile(bpy.path.abspath(i.filepath))],'exports':{}}
for filename in ['INTEIA_F1_estatico.glb','INTEIA_F1_animado.glb']:
    p=ROOT+'/modelos/'+filename;data=open(p,'rb').read();length=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+length])
    count=sum(doc['accessors'][p['indices']]['count']//3 for m in doc['meshes'] for p in m['primitives'])
    animations=[{'name':a.get('name'), 'channels':len(a['channels'])} for a in doc.get('animations',[])]
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=p)
    imported=[o for o in bpy.context.scene.objects if o.type=='MESH']
    assert len(imported)==97
    report['exports'][filename]={'reimported':True,'meshes':len(imported),'triangles':count,'animations':animations,'bytes':len(data)}
assert not report['images_missing']
assert report['exports']['INTEIA_F1_animado.glb']['animations']
open(ROOT+'/validacao-reabertura.json','w').write(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
