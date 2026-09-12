import bpy, math, os, json
from mathutils import Vector
from pathlib import Path
ROOT=str(Path(__file__).resolve().parents[1])
OUT=ROOT
os.makedirs(OUT+'/modelos',exist_ok=True)
os.makedirs(OUT+'/texturas',exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=ROOT+'/web/assets/carro-movable.glb')
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.render.fps=30
car=bpy.data.collections.new('INTEIA | Carro reutilizavel');scene.collection.children.link(car)
meshes=[o for o in scene.objects if o.type=='MESH']
source_matrices={o.name:o.matrix_world.copy() for o in meshes}
for o in meshes:
    world=o.matrix_world.copy();o.parent=None;o.matrix_world=world
    for c in list(o.users_collection):c.objects.unlink(o)
    car.objects.link(o)
for o in list(scene.objects):
    if o.type=='EMPTY':bpy.data.objects.remove(o,do_unlink=True)
root=bpy.data.objects.new('INTEIA_F1',None);car.objects.link(root)
for o in meshes:
    world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
root['origem']='Modelo exterior fornecido pelo usuario, tutorial F1 2026 parte 7'
root['movimentos']='Demonstracao ilustrativa; nao e simulacao mecanica certificada'
def linear(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
def col(h):return tuple(linear(int(h[i:i+2],16)/255) for i in (1,3,5))+(1,)
def base(m,h,metal,rough,coat=0,cr=.1):
    m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled');l.new(p.outputs['BSDF'],out.inputs['Surface'])
    p.inputs['Base Color'].default_value=col(h);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    p.inputs['Coat Weight'].default_value=coat;p.inputs['Coat Roughness'].default_value=cr
    m.diffuse_color=col(h);m.asset_mark();return p
# A portable texture plus planar UVs replaces the browser-only shader projection.
size=256;pixels=[]
for y in range(size):
    for x in range(size):
        xx=(x+y)%256;yy=(y-x+256)%256;across=((xx//16+yy//16)%4)<2;q=xx if across else yy
        fiber=70+math.sin(q%16/16*math.pi)*70+(.5+.5*math.sin(q*math.pi/2))*12
        grey=(35+fiber*.19)/255
        pixels.extend([linear(grey)*linear(210/255),linear(grey+1/255)*linear(212/255),linear(grey+2/255)*linear(214/255),1])
im=bpy.data.images.new('INTEIA_Carbono_BaseColor',width=size,height=size,alpha=False)
im.pixels.foreach_set(pixels);im.filepath_raw=OUT+'/texturas/INTEIA_Carbono_BaseColor.png';im.file_format='PNG';im.save();im.pack()
for m in list(bpy.data.materials):
    name=m.name.lower()
    if name.startswith('pintura'):base(m,'#ce0014',0,.27,1,.105)
    elif 'carbon' in name:
        p=base(m,'#ffffff',.05,.54,.12,.4)
        tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;tex.extension='REPEAT'
        m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
    elif name in ['pneus','borracha']:base(m,'#202124' if name=='pneus' else '#191a1b',0,.7)
    elif name=='rodas':base(m,'#282b30',.78,.29,.2,.2)
    elif name=='aço':base(m,'#656b73',.8,.48)
    elif name=='mirror':base(m,'#e0e4e7',1,.055)
    elif name=='vidro':
        p=base(m,'#bccbd0',.12,.1,1,.06);p.inputs['Alpha'].default_value=.38;m.surface_render_method='DITHERED'
    m.asset_mark()
for o in meshes:
    uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
    for f in o.data.polygons:
        mat=o.data.materials[f.material_index] if f.material_index<len(o.data.materials) else None
        if mat and 'carbon' in mat.name.lower():
            axis=max(range(3),key=lambda i:abs(f.normal[i]));axes=[i for i in range(3) if i!=axis]
            for li in f.loop_indices:
                p=o.data.vertices[o.data.loops[li].vertex_index].co
                uv.data[li].uv=(p[axes[0]]*3,p[axes[1]]*3)
    o['INTEIA_componente']=True
car.asset_mark()
# Preserve all embedded source textures.
for image in bpy.data.images:
    if image.source=='FILE' and image.has_data:
        image.pack()
def center(o):return sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
def reparent(o,p):
    bpy.context.view_layer.update()
    w=o.matrix_world.copy();o.parent=p;o.matrix_world=w
    bpy.context.view_layer.update()
wheel_pivots=[];spin_pivots=[]
for axle in ['front','rear']:
    for side in [-1,1]:
        tire=next(o for o in meshes if o.get('sourceObject')==axle+'_tire' and (1 if center(o).x>0 else -1)==side)
        p=bpy.data.objects.new('Direcao_'+axle+'_'+str(side),None);car.objects.link(p);p.parent=root;p.location=tire.location
        s=bpy.data.objects.new('Giro_'+axle+'_'+str(side),None);car.objects.link(s);s.parent=p
        for o in meshes:
            src=o.get('sourceObject','')
            if (1 if center(o).x>0 else -1)!=side:continue
            if src in [axle+'_tire',axle+'_wheel_cover']:reparent(o,s)
            elif src==('inside_cover' if axle=='front' else 'rear_inside_cover'):reparent(o,p)
        if axle=='front':wheel_pivots.append(p)
        spin_pivots.append(s)
flap=next(o for o in meshes if o.get('sourceObject')=='rear_wing_drs')
hinge=bpy.data.objects.new('Abertura_DRS',None);car.objects.link(hinge);hinge.parent=root;hinge.location=center(flap);hinge.location.z+=flap.dimensions.z*.4;hinge.location.y+=flap.dimensions.y*.35;reparent(flap,hinge)
base_positions={o:o.location.copy() for o in meshes}
initial={o.name:list(sum((list(row) for row in o.matrix_world),[])) for o in meshes}
seen={}
for o in meshes:
    c=center(o);x,y,z=c.x,c.z,-c.y;src=o.get('sourceObject','');cat=o.get('category','details');sign=lambda v:1 if v>0 else -1 if v<0 else 0
    idx=seen.get((src,sign(x)),0);seen[(src,sign(x))]=idx+1
    if cat=='wheels':d=Vector((sign(x)*(1.35+(0 if 'tire' in src else .45)+idx*.22),.18,sign(z)*.18))
    elif cat=='suspension':d=Vector((sign(x or 1)*1.25,.45,sign(z)*.3))
    elif 'front_wing' in src:d=Vector((x*.5,.1,1.85))
    elif 'rear_wing' in src or 'drs' in src:d=Vector((x*.6,.75,-1.55))
    elif 'floor' in src:d=Vector((x*.25,.05,-.15))
    elif src=='main_body':d=Vector((0,1.65,0))
    elif cat=='cockpit':d=Vector((x*.6,1.1,.35))
    else:d=Vector((x*.75,.9,z*.55))
    d.y+=min(idx*.06,.35);delta=Vector((d.x,-d.z,d.y))
    for frame,t in [(1,0),(90,1),(120,1),(210,0),(300,0)]:
        o.location=base_positions[o]+delta*t;o.keyframe_insert(data_path='location',frame=frame,group='Montagem')
for p in spin_pivots:
    for frame,angle in [(1,0),(210,0),(300,math.tau*2)]:p.rotation_euler.x=angle;p.keyframe_insert(data_path='rotation_euler',frame=frame,group='Giro das rodas')
for p in wheel_pivots:
    for frame,a in [(1,0),(210,0),(240,22),(270,-22),(300,0)]:p.rotation_euler.z=math.radians(a);p.keyframe_insert(data_path='rotation_euler',frame=frame,group='Direcao')
for frame,a in [(1,0),(210,0),(255,-32),(300,0)]:hinge.rotation_euler.x=math.radians(a);hinge.keyframe_insert(data_path='rotation_euler',frame=frame,group='DRS')
scene.frame_start=1;scene.frame_end=300
for frame,name in [(1,'MONTADO'),(90,'DESMONTADO'),(120,'REMONTAR'),(210,'RODAS DIRECAO DRS'),(300,'FIM')]:scene.timeline_markers.new(name,frame=frame)
scene.frame_set(1);bpy.context.view_layer.update()
error=max(abs(o.matrix_world[r][c]-source_matrices[o.name][r][c]) for o in meshes for r in range(4) for c in range(4))
assert error<.00001, f'Assembly drift: {error}'
def select_car():
    bpy.ops.object.select_all(action='DESELECT')
    for o in car.objects:o.select_set(True)
    bpy.context.view_layer.objects.active=root
select_car()
bpy.ops.export_scene.gltf(filepath=OUT+'/modelos/INTEIA_F1_estatico.glb',use_selection=True,export_animations=False,export_extras=True)
bpy.ops.export_scene.gltf(filepath=OUT+'/modelos/INTEIA_F1_animado.glb',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_force_sampling=True,export_extras=True)
# Studio stays separate and is excluded from model exports.
studio=bpy.data.collections.new('INTEIA | Estudio (nao exportar para jogos)');scene.collection.children.link(studio)
def to_studio(o):
    for c in list(o.users_collection):c.objects.unlink(o)
    studio.objects.link(o)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.009));floor=bpy.context.object;floor.name='Piso do estudio';to_studio(floor)
m=bpy.data.materials.new('INTEIA_Piso');base(m,'#c9c8c5',.06,.7);floor.data.materials.append(m)
for name,loc,power,size in [('Principal',(-4.5,-2,7),500,5),('Preenchimento',(5,5,3),300,4),('Topo',(0,1,9),400,5),('Recorte',(0,9,4),300,4)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
    o=bpy.data.objects.new(name,data);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
world=bpy.data.worlds.new('INTEIA_Ambiente');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.3,.3,.3,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
data=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',data);studio.objects.link(cam);cam.location=(7,-9,4.4);cam.rotation_euler=(Vector((0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler();data.lens=48;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=960;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene['INTEIA_notas']='Materiais adaptados para Blender/glTF. Trama de carbono UV planar portavel; reflexos diferem do shader Three.js. 97 componentes exteriores; sem LOD, colisores ou interiores novos.'
text=bpy.data.texts.new('LEIA-ME INTEIA');text.write(scene['INTEIA_notas']+'\nTimeline: 1 montado; 90-120 explodido; 210 remontado; 210-300 rodas/direcao/DRS.\nReutilize a colecao INTEIA | Carro reutilizavel via File > Append. Materiais e colecao marcados como assets.\nOrigem: arquivo de tutorial fornecido pelo usuario. Conferir licenca original antes de distribuir/comercializar.')
select_car();bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=OUT+'/INTEIA_F1_Master.blend',compress=True)
scene.render.filepath=OUT+'/Previa-Blender.png';bpy.ops.render.render(write_still=True)
report={'mesh_components':len(meshes),'triangles':sum(len(o.data.polygons) for o in meshes),'frames':[1,300],'fps':30,'packed_images':[i.name for i in bpy.data.images if i.packed_file],'blend':'INTEIA_F1_Master.blend'}
open(OUT+'/validacao-criacao.json','w').write(json.dumps(report,indent=2))
print('INTEIA_PACKAGE_OK',json.dumps(report))
