# Índice de funções e métodos

[Índice](README.md) · [Busca interativa](index.html) · [JSON](dados/simbolos.json)

tree-sitter-javascript: declarações nomeadas, arrow functions atribuídas e métodos; Python ast: funções/classes. Callbacks anônimos e resolução dinâmica não são indexados integralmente.

Chamadas são referências sintáticas conservadoras, não rastreamento de execução. Funções anônimas e métodos dinâmicos exigem a leitura dos módulos.

## ferramentas/gerar_sistemas.py

[Fonte](../../ferramentas/gerar_sistemas.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| _import_glb | 40 | module | `def _import_glb(path):` |
| _bbox | 45 | module | `def _bbox(objs):` |
| import_car_reference | 58 | module | `def import_car_reference(alpha=.045):` |
| power_unit_reference | 76 | module | `def power_unit_reference():` |
| measure_glb | 154 | module | `def measure_glb(path):` |
| write_manifest | 181 | module | `def write_manifest(path_glb, optimized):` |
| light | 226 | module | `def light(name, kind, loc, energy, size=2.0):` |
| frame | 244 | module | `def frame(objs, direction, pad=1.25):` |

## ferramentas/otimizar_sistemas.mjs

[Fonte](../../ferramentas/otimizar_sistemas.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| load | 14 | module | `load(name)` |
| systemNames | 33 | module | `systemNames(docRoot)` |
| partCount | 34 | module | `partCount(docRoot)` |

## ferramentas/package_blender.py

[Fonte](../../ferramentas/package_blender.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| linear | 27 | module | `def linear(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4` |
| col | 28 | module | `def col(h):return tuple(linear(int(h[i:i+2],16)/255) for i in (1,3,5))+(1,)` |
| base | 29 | module | `def base(m,h,metal,rough,coat=0,cr=.1):` |
| center | 74 | module | `def center(o):return sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8` |
| reparent | 75 | module | `def reparent(o,p):` |
| select_car | 121 | module | `def select_car():` |
| to_studio | 130 | module | `def to_studio(o):` |

## ferramentas/sistemas/lib.py

[Fonte](../../ferramentas/sistemas/lib.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| W | 15 | module | `def W(x, y=None, z=None):` |
| to_web | 21 | module | `def to_web(v):` |
| _encode_normal | 31 | module | `def _encode_normal(height, strength=1.0):` |
| image_from_array | 38 | module | `def image_from_array(name, rgba, srgb=True):` |
| tex_twill | 50 | module | `def tex_twill(size=256, tow=16, base=(.028, .032, .038), lift=.055):` |
| tex_kevlar | 61 | module | `def tex_kevlar(size=256, tow=12):` |
| tex_brushed | 70 | module | `def tex_brushed(size=256):` |
| tex_cast | 77 | module | `def tex_cast(size=256):` |
| tex_heat | 86 | module | `def tex_heat(size=256):` |
| tex_brake_disc | 99 | module | `def tex_brake_disc(size=512, rings=14, holes_per_ring=64, inner=.42):` |
| tex_fins | 121 | module | `def tex_fins(size=256, pitch=6):` |
| tex_honeycomb | 128 | module | `def tex_honeycomb(size=256, cell=18):` |
| tex_kapton | 138 | module | `def tex_kapton(size=256):` |
| tex_braid | 144 | module | `def tex_braid(size=128, tow=8):` |
| tex_display | 151 | module | `def tex_display(size=(512, 256)):` |
| material | 180 | module | `def material(name, color, metallic=0.0, roughness=0.45, *, emissive=None, emissive_strength=1.0, alpha=1.0,` |
| tex_node | 212 | 180:material | `def tex_node(img):` |
| Materials | 239 | module | `class Materials:` |
| __init__ | 241 | 239:Materials | `def __init__(self):` |
| Context | 320 | module | `class Context:` |
| __init__ | 321 | 320:Context | `def __init__(self, scene, mats):` |
| system | 329 | 320:Context | `def system(self, sid, label):` |
| register | 339 | 320:Context | `def register(self, obj, part, *, spin=None, spin_axis='y', flow=None, era=None, explode=None, hide_group=None, tag=None, carrier=False, parent=None):` |
| _link | 366 | module | `def _link(obj):` |
| shade_smooth | 370 | module | `def shade_smooth(obj, angle=math.radians(38)):` |
| bevel | 384 | module | `def bevel(obj, width=.002, segments=2, angle=math.radians(40)):` |
| box_uv | 392 | module | `def box_uv(obj, scale=1.0, offset=(0.0, 0.0)):` |
| mesh_object | 412 | module | `def mesh_object(name, verts, faces, edges=(), uvs=None):` |
| bm_to_object | 424 | module | `def bm_to_object(name, bm, smooth=True):` |
| set_material | 433 | module | `def set_material(obj, mat):` |
| orient | 439 | module | `def orient(obj, axis):` |
| cube | 447 | module | `def cube(ctx, part, center, size, mat, *, bev=.002, segments=2, rot=None, uv=None, **extras):` |
| W_rot | 461 | module | `def W_rot(rot):` |
| cyl | 467 | module | `def cyl(ctx, part, center, radius, length, mat, *, axis=UP, verts=32, bev=.0012, segments=2, radius2=None, **extras):` |
| tube_cyl | 476 | module | `def tube_cyl(ctx, part, center, radius, wall, length, mat, *, axis=UP, verts=32, **extras):` |
| sphere | 497 | module | `def sphere(ctx, part, center, radius, mat, *, segments=24, rings=16, scale=None, **extras):` |
| torus | 505 | module | `def torus(ctx, part, center, major, minor, mat, *, axis=UP, seg=40, mseg=12, **extras):` |
| catmull | 512 | module | `def catmull(points, per_segment=8, closed=False):` |
| _frames | 530 | module | `def _frames(pts, closed=False):` |
| sweep | 555 | module | `def sweep(ctx, part, points, mat, *, radius=.01, radii=None, sides=14, smooth_path=True, per_segment=8,` |
| airfoil | 612 | module | `def airfoil(chord, thick, camber=0.0, n=18):` |
| loft | 629 | module | `def loft(ctx, part, sections, mat, *, cap=True, open_ring=False, **extras):` |
| lathe | 654 | module | `def lathe(ctx, part, profile, mat, *, center=(0, 0, 0), axis=UP, segments=40, **extras):` |
| helix | 668 | module | `def helix(ctx, part, center, radius, pitch, turns, wire, mat, *, axis=UP, per_turn=28, **extras):` |
| gear | 678 | module | `def gear(ctx, part, center, teeth, module, width, mat, *, axis=UP, bore=None, helix_deg=0, hub_r=None, hub_w=None, spokes=0, **extras):` |
| ring | 694 | 678:gear | `def ring(z, pts):` |
| bolt_ring | 730 | module | `def bolt_ring(ctx, part, center, radius, count, axis, mat_head, *, size=.006, head=.004, start=0.0, **extras):` |
| join | 753 | module | `def join(ctx, objects, part=None, **extras):` |
| mirror_x | 779 | module | `def mirror_x(ctx, obj, part=None):` |
| both_sides | 802 | module | `def both_sides(fn):` |
| hexagon | 806 | module | `def hexagon(r):` |
| rounded_rect | 809 | module | `def rounded_rect(w, h, r, n=4):` |
| super_ellipse | 817 | module | `def super_ellipse(w, h, n=2.6, seg=32, exp=None):` |
| shell | 826 | module | `def shell(ctx, part, sections, mat, *, thickness=.004, open_ring=False, **extras):` |
| flow_ribbon | 832 | module | `def flow_ribbon(ctx, part, points, kind, *, radius=.006, **extras):` |
| text_plate | 836 | module | `def text_plate(ctx, part, text, center, size, mat, *, normal=FWD, up=UP, depth=.0006, **extras):` |
| centroid | 852 | module | `def centroid(objs):` |
| auto_explode | 863 | module | `def auto_explode(ctx, sid, scale=1.0, min_len=.06):` |

## ferramentas/sistemas/s01_aero.py

[Fonte](../../ferramentas/sistemas/s01_aero.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 18 | module | `def build(ctx):` |

## ferramentas/sistemas/s02_structure.py

[Fonte](../../ferramentas/sistemas/s02_structure.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| tub_section | 22 | module | `def tub_section(z, w, y0, y1):` |
| build | 28 | module | `def build(ctx):` |

## ferramentas/sistemas/s03_suspension.py

[Fonte](../../ferramentas/sistemas/s03_suspension.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| leg | 38 | module | `def leg(ctx, name, a, b, mat, chord=.048, thick=.26, camber=0.0):` |
| mirror_side | 41 | module | `def mirror_side(v):` |
| rod_end | 44 | module | `def rod_end(ctx, name, p, mat, r=.011):` |
| upright | 48 | module | `def upright(ctx, P, front, label):` |
| corner | 76 | module | `def corner(ctx, P, front, label):` |
| center_elements | 119 | module | `def center_elements(ctx, P, front):` |
| build | 140 | module | `def build(ctx):` |

## ferramentas/sistemas/s04_steering.py

[Fonte](../../ferramentas/sistemas/s04_steering.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 19 | module | `def build(ctx):` |

## ferramentas/sistemas/s05_brakes.py

[Fonte](../../ferramentas/sistemas/s05_brakes.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| arc | 20 | module | `def arc(center, radius, a0, a1, n=12):` |
| corner | 27 | module | `def corner(ctx, wheel, front, label):` |
| build | 74 | module | `def build(ctx):` |

## ferramentas/sistemas/s06_power.py

[Fonte](../../ferramentas/sistemas/s06_power.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| bank_frame | 26 | module | `def bank_frame(side):` |
| add | 32 | module | `def add(a, b, s=1.0):` |
| build | 35 | module | `def build(ctx):` |

## ferramentas/sistemas/s07_ers.py

[Fonte](../../ferramentas/sistemas/s07_ers.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 20 | module | `def build(ctx):` |

## ferramentas/sistemas/s08_cooling.py

[Fonte](../../ferramentas/sistemas/s08_cooling.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| core | 17 | module | `def core(ctx, name, center, size, tilt_deg, mat_tank):` |
| hose | 33 | module | `def hose(ctx, name, pts, kind, r=.016):` |
| build | 40 | module | `def build(ctx):` |

## ferramentas/sistemas/s09_fuel.py

[Fonte](../../ferramentas/sistemas/s09_fuel.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| bladder_sections | 17 | module | `def bladder_sections():` |
| build | 23 | module | `def build(ctx):` |

## ferramentas/sistemas/s10_transmission.py

[Fonte](../../ferramentas/sistemas/s10_transmission.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| rr_section | 26 | module | `def rr_section(w, h, r=.02):` |
| build | 29 | module | `def build(ctx):` |

## ferramentas/sistemas/s11_safety.py

[Fonte](../../ferramentas/sistemas/s11_safety.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 18 | module | `def build(ctx):` |

## ferramentas/sistemas/s12_cockpit.py

[Fonte](../../ferramentas/sistemas/s12_cockpit.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| strap | 18 | module | `def strap(ctx, name, pts, width=.075):` |
| build | 21 | module | `def build(ctx):` |
| seat_section | 25 | 21:build | `def seat_section(t):` |

## ferramentas/sistemas/s13_wheel.py

[Fonte](../../ferramentas/sistemas/s13_wheel.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 17 | module | `def build(ctx):` |

## ferramentas/sistemas/s14_sensors.py

[Fonte](../../ferramentas/sistemas/s14_sensors.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 20 | module | `def build(ctx):` |

## ferramentas/validate-kit.py

[Fonte](../../ferramentas/validate-kit.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| matrices | 7 | module | `def matrices():` |

## web/build.cjs

[Fonte](../../web/build.cjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| source | 6 | module | `source(...parts)` |
| replaceRequired | 8 | module | `replaceRequired(template, marker, value)` |

## web/server.cjs

[Fonte](../../web/server.cjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| reply | 17 | module | `reply(response, status, body = '')` |

## web/src/aero-physics.mjs

[Fonte](../../web/src/aero-physics.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| aerodynamicTest | 2 | module | `aerodynamicTest({speedKmh=0,headwindKmh=0,crosswindKmh=0,temperatureC=15,pressureKPa=101.325,area=null,cd=null,clDown=null,length=5.5})` |

## web/src/app-v2.js

[Fonte](../../web/src/app-v2.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| $ | 25 | module | `$` |
| closeEngine | 36 | module | `closeEngine()` |
| setFlowXray | 38 | module | `setFlowXray(on)` |
| clone | 39 | 38:setFlowXray | `clone` |
| moveCamera | 46 | module | `moveCamera(to,target,animate=true)` |
| setCarSelectionEnabled | 47 | module | `setCarSelectionEnabled(enabled)` |
| syncSystemMode | 48 | module | `syncSystemMode()` |
| view | 50 | module | `view(name,animate=true)` |
| resize | 52 | module | `resize()` |
| refreshSelection | 54 | module | `refreshSelection()` |
| select | 55 | module | `select(id)` |
| focusPart | 56 | module | `focusPart()` |
| assemblyTo | 57 | module | `assemblyTo(v)` |
| target | 68 | module | `target()` |
| showCar | 69 | module | `showCar()` |
| onClose | 69 | module | `onClose()` |
| onBeforeToggle | 69 | module | `onBeforeToggle` |
| onRegion | 69 | module | `onRegion` |
| onToggle | 69 | module | `onToggle` |
| showCar | 70 | module | `showCar()` |

## web/src/branding.js

[Fonte](../../web/src/branding.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| applyInteiaBranding | 5 | module | `applyInteiaBranding(model, mechanics)` |
| project | 25 | 5:applyInteiaBranding | `project(source,origin,direction,rotation,width,depth,decalMaterial=material,decalAspect=aspect)` |
| dispose | 48 | 5:applyInteiaBranding | `dispose()` |

## web/src/car-look.js

[Fonte](../../web/src/car-look.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| rimPatch | 36 | module | `rimPatch(material, uniforms)` |
| paintShader | 49 | module | `paintShader(material)` |
| localVaryings | 62 | module | `localVaryings(shader, tag)` |
| rimShader | 70 | module | `rimShader(material)` |
| tyreShader | 100 | module | `tyreShader(material)` |
| discTexture | 127 | module | `discTexture(width)` |
| random | 132 | 127:discTexture | `random()` |
| heatTexture | 160 | module | `heatTexture()` |
| discGeometry | 174 | module | `discGeometry()` |
| caliperGeometry | 186 | module | `caliperGeometry()` |
| at | 188 | 186:caliperGeometry | `at(r, a)` |
| enhanceCar | 202 | module | `enhanceCar({model, mechanics, mobile})` |
| share | 249 | 202:enhanceCar | `share(source, setup)` |
| rimSetup | 253 | 202:enhanceCar | `rimSetup` |
| tyreSetup | 254 | 202:enhanceCar | `tyreSetup` |
| nutSetup | 257 | 202:enhanceCar | `nutSetup` |
| update | 308 | 202:enhanceCar | `update()` |
| setRim | 314 | 202:enhanceCar | `setRim(color, strength, direction, edge = .72)` |
| race | 322 | 202:enhanceCar | `race(speed, brake, time)` |
| dispose | 340 | 202:enhanceCar | `dispose()` |

## web/src/customize.js

[Fonte](../../web/src/customize.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| setupCustomization | 1 | module | `setupCustomization(materials, studio, renderer, scene)` |
| $ | 2 | 1:setupCustomization | `$` |
| applyLight | 32 | 1:setupCustomization | `applyLight()` |

## web/src/engine/engine-shot.js

[Fonte](../../web/src/engine/engine-shot.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| clamp | 4 | module | `clamp` |
| smooth | 5 | module | `smooth` |
| segment | 48 | module | `segment(keys,p)` |
| tangent | 50 | module | `tangent(keys,i,slot,axis)` |
| spline | 59 | module | `spline(slot,p)` |
| eased | 64 | module | `eased(keys,p)` |
| engineShot | 70 | module | `engineShot(progress,mobile=false)` |

## web/src/engine/in-car.js

[Fonte](../../web/src/engine/in-car.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| smooth | 16 | module | `smooth` |
| nextFrame | 17 | module | `nextFrame()` |
| aborted | 18 | module | `aborted()` |
| createInCarEngine | 25 | module | `createInCarEngine({scene,renderer,camera,model,mechanics,target,mobile=false,signal=null,offstage=()=>[]})` |
| cancel | 48 | 25:createInCarEngine | `cancel()` |
| derive | 54 | 25:createInCarEngine | `derive(material,planes,intersection)` |
| buildSplit | 55 | 25:createInCarEngine | `buildSplit()` |
| twin | 58 | 55:buildSplit | `twin(mesh,material)` |
| setSplit | 68 | 25:createInCarEngine | `setSplit(on)` |
| poseCover | 75 | 25:createInCarEngine | `poseCover(open)` |
| collect | 85 | 25:createInCarEngine | `collect(object)` |
| buildEngine | 88 | 25:createInCarEngine | `buildEngine(gltf)` |
| sectioned | 104 | 88:buildEngine | `sectioned` |
| satin | 107 | 88:buildEngine | `satin` |
| precompile | 115 | 25:createInCarEngine | `precompile()` |
| add | 117 | 115:precompile | `add` |
| upload | 134 | 25:createInCarEngine | `upload()` |
| flush | 139 | 134:upload | `flush()` |
| load | 154 | 25:createInCarEngine | `load()` |
| rehearse | 176 | 25:createInCarEngine | `rehearse()` |
| releaseEngine | 191 | 25:createInCarEngine | `releaseEngine()` |
| state | 199 | 25:createInCarEngine | `state()` |
| ready | 200 | 25:createInCarEngine | `ready()` |
| prepare | 202 | 25:createInCarEngine | `prepare()` |
| update | 212 | 25:createInCarEngine | `update(dt,shot,paused)` |
| dispose | 226 | 25:createInCarEngine | `dispose()` |

## web/src/flow-detail.js

[Fonte](../../web/src/flow-detail.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createFlowDetail | 4 | module | `createFlowDetail({parent,size})` |
| path | 9 | 4:createFlowDetail | `path(points,category)` |
| sample | 45 | 4:createFlowDetail | `sample(p,t)` |
| update | 46 | 4:createFlowDetail | `update(dt,r,invalid,reduced,settings)` |

## web/src/garage.js

[Fonte](../../web/src/garage.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createGarage | 7 | module | `createGarage({scene,renderer,studio,camera,mechanics})` |
| mat | 10 | 7:createGarage | `mat(color,metalness=.0,roughness=.5)` |
| box | 13 | 7:createGarage | `box(w,h,d,x,y,z,m=white,rounded=false,parent=root)` |
| cylinder | 14 | 7:createGarage | `cylinder(r1,r2,h,x,y,z,m=steel,parent=root)` |
| tube | 15 | 7:createGarage | `tube(points,r=.018,m=black,parent=root)` |
| label | 16 | 7:createGarage | `label(text,w,h,x,y,z,rotation=0,bg='#e0e3e4',fg='#26313b',font=50)` |
| grain | 18 | 7:createGarage | `grain(repeatX,repeatY)` |
| cabinet | 40 | 7:createGarage | `cabinet(x,z,w=1.35)` |
| screen | 53 | 7:createGarage | `screen(x,y,z,w,h,kind,rotation=0)` |
| draw | 58 | 53:screen | `draw()` |
| getExportScene | 148 | 7:createGarage | `getExportScene()` |
| enabled | 148 | 7:createGarage | `enabled()` |
| setEnabled | 148 | 7:createGarage | `setEnabled(on)` |
| update | 151 | 7:createGarage | `update(dt)` |

## web/src/helmet-1991.js

[Fonte](../../web/src/helmet-1991.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createHelmet1991 | 5 | module | `createHelmet1991({detail=128}={})` |
| material | 7 | 5:createHelmet1991 | `material` |
| add | 19 | 5:createHelmet1991 | `add(g,m,parent=root)` |
| radius | 22 | 5:createHelmet1991 | `radius(y)` |
| point | 23 | 5:createHelmet1991 | `point(y,a,lift=0)` |
| patch | 33 | 5:createHelmet1991 | `patch(y0,y1,a0,a1,m,lift=0,rows=36,cols=detail,parent=root)` |
| tube | 48 | 5:createHelmet1991 | `tube(points,r,m,parent=root)` |
| label | 54 | 5:createHelmet1991 | `label(y0,y1,a0,a1,draw,parent=root)` |
| text | 55 | 5:createHelmet1991 | `text(x,s,font,color='#f2f0e8')` |
| emblem | 56 | 5:createHelmet1991 | `emblem(x)` |
| national | 57 | 5:createHelmet1991 | `national(x)` |
| screw | 68 | 5:createHelmet1991 | `screw(a,y,r)` |
| dispose | 79 | 5:createHelmet1991 | `dispose()` |

## web/src/identity.js

[Fonte](../../web/src/identity.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| brandSVG | 11 | module | `brandSVG({light=false,compact=false}={})` |
| drawBrand | 16 | module | `drawBrand(ctx,width,height,{light=false}={})` |

## web/src/mechanics.js

[Fonte](../../web/src/mechanics.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createMechanics | 3 | module | `createMechanics(model)` |
| categoryFor | 8 | 3:createMechanics | `categoryFor` |
| apply | 43 | 3:createMechanics | `apply()` |
| amount | 55 | 3:createMechanics | `amount()` |
| target | 55 | 3:createMechanics | `target()` |
| playing | 55 | 3:createMechanics | `playing()` |
| selected | 55 | 3:createMechanics | `selected()` |
| isolated | 55 | 3:createMechanics | `isolated()` |
| motionAvailable | 55 | 3:createMechanics | `motionAvailable()` |
| drag | 56 | 3:createMechanics | `drag(v)` |
| restoreParts | 57 | 3:createMechanics | `restoreParts()` |
| setAmount | 58 | 3:createMechanics | `setAmount(v)` |
| setManual | 59 | 3:createMechanics | `setManual(v)` |
| select | 60 | 3:createMechanics | `select(id)` |
| isolate | 61 | 3:createMechanics | `isolate()` |
| setSpin | 62 | 3:createMechanics | `setSpin(v)` |
| setSteering | 62 | 3:createMechanics | `setSteering(v)` |
| setDRS | 62 | 3:createMechanics | `setDRS(v)` |
| toggleLoop | 63 | 3:createMechanics | `toggleLoop()` |
| reset | 64 | 3:createMechanics | `reset()` |
| update | 65 | 3:createMechanics | `update(dt,now,reduced)` |

## web/src/senna-driver.js

[Fonte](../../web/src/senna-driver.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createSennaDriver | 6 | module | `createSennaDriver(model, mechanics)` |
| mat | 10 | 6:createSennaDriver | `mat(name,options)` |
| mesh | 20 | 6:createSennaDriver | `mesh(name,g,m,parent=body)` |
| V | 21 | 6:createSennaDriver | `V` |
| loft | 23 | 6:createSennaDriver | `loft(name,points,widths,depths,material,fold=.001)` |
| piping | 34 | 6:createSennaDriver | `piping(name,points,r,material=seam)` |
| rounded | 35 | 6:createSennaDriver | `rounded(name,dimensions,position,material)` |
| chest | 39 | 6:createSennaDriver | `chest(t,x)` |
| p | 42 | 6:createSennaDriver | `p` |
| ribbon | 55 | 6:createSennaDriver | `ribbon(name,points,width)` |
| applyFit | 66 | 6:createSennaDriver | `applyFit()` |
| setFit | 69 | 6:createSennaDriver | `setFit(values)` |
| update | 69 | 6:createSennaDriver | `update()` |
| dispose | 69 | 6:createSennaDriver | `dispose()` |

## web/src/studio.js

[Fonte](../../web/src/studio.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| setupStudio | 2 | module | `setupStudio(THREE, renderer, scene)` |
| panel | 14 | 2:setupStudio | `panel(w, h, position, power, color = '#ffffff')` |
| setTheme | 59 | 2:setupStudio | `setTheme` |
| update | 69 | 2:setupStudio | `update()` |
| dispose | 69 | 2:setupStudio | `dispose()` |
| texture | 75 | module | `texture(THREE, mode)` |
| random | 81 | 75:texture | `random()` |
| applyLocalCarbonProjection | 104 | module | `applyLocalCarbonProjection(material)` |
| applyCarMaterials | 146 | module | `applyCarMaterials(THREE, model)` |
| upgrade | 182 | 146:applyCarMaterials | `upgrade` |
| dispose | 251 | 146:applyCarMaterials | `dispose()` |

## web/src/surface-library.js

[Fonte](../../web/src/surface-library.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createSurfaceLibrary | 16 | module | `createSurfaceLibrary(THREE, {renderer, mobile = false} = {})` |
| clamp | 19 | 16:createSurfaceLibrary | `clamp(v,a=0,b=1)` |
| noise | 21 | 16:createSurfaceLibrary | `noise(x,y,seed)` |
| texture | 22 | 16:createSurfaceLibrary | `texture(bytes, color=false)` |
| bake | 28 | 16:createSurfaceLibrary | `bake(kind, tileMeters, pixel, normalStrength)` |
| transformed | 67 | 16:createSurfaceLibrary | `transformed(map,repeat)` |
| applyTo | 68 | 16:createSurfaceLibrary | `applyTo(material,kind,{uvSpanMeters=1}={})` |
| dispose | 98 | 16:createSurfaceLibrary | `dispose()` |

## web/src/systems.js

[Fonte](../../web/src/systems.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| advanceLocalSpin | 31 | module | `advanceLocalSpin(quaternion,axis='y',angle=0)` |
| flowTexture | 34 | module | `flowTexture()` |
| createSystems | 42 | module | `createSystems({scene,model,mechanics,engine,driver,garage,camera,canvas,moveCamera,showCar=()=>{},onClose=showCar,mobile=false,assetUrl=SYSTEMS_ASSET})` |
| onVisibilityChange | 50 | 42:createSystems | `onVisibilityChange()` |
| meta | 52 | 42:createSystems | `meta` |
| flowMaterial | 57 | 42:createSystems | `flowMaterial` |
| cardFor | 66 | 42:createSystems | `cardFor` |
| logicalPartCount | 67 | 42:createSystems | `logicalPartCount` |
| syncView | 68 | 42:createSystems | `syncView` |
| setStatus | 69 | 42:createSystems | `setStatus` |
| attachPart | 72 | 42:createSystems | `attachPart(mesh,systemId,logicalOwner=mesh.uuid)` |
| prepareMaterials | 84 | 42:createSystems | `prepareMaterials(sceneRoot)` |
| distribute | 93 | 42:createSystems | `distribute(gltf)` |
| ownerId | 95 | 93:distribute | `ownerId` |
| load | 110 | 42:createSystems | `load()` |
| applyEra | 125 | 42:createSystems | `applyEra()` |
| applyCovers | 126 | 42:createSystems | `applyCovers()` |
| applyExplode | 127 | 42:createSystems | `applyExplode()` |
| translucentOf | 129 | 42:createSystems | `translucentOf` |
| materialFor | 130 | 42:createSystems | `materialFor(entry)` |
| applyFlows | 131 | 42:createSystems | `applyFlows()` |
| applySchematic | 132 | 42:createSystems | `applySchematic()` |
| highlight | 134 | 42:createSystems | `highlight(entry,on)` |
| setPicked | 141 | 42:createSystems | `setPicked(entry)` |
| setERSContext | 143 | 42:createSystems | `setERSContext(mode)` |
| updateUI | 144 | 42:createSystems | `updateUI(id=active)` |
| objectFor | 149 | 42:createSystems | `objectFor(id)` |
| geometryBounds | 150 | 42:createSystems | `geometryBounds(object)` |
| viewportAspect | 151 | 42:createSystems | `viewportAspect()` |
| frame | 153 | 42:createSystems | `frame(id,direction=directions[currentView],animate=true)` |
| show | 154 | 42:createSystems | `show(id='overview',animate=true)` |
| view | 155 | 42:createSystems | `view(name)` |
| captureGhost | 156 | 42:createSystems | `captureGhost()` |
| cloneMaterial | 156 | 156:captureGhost | `cloneMaterial` |
| setGhost | 157 | 42:createSystems | `setGhost(on)` |
| setEnabled | 158 | 42:createSystems | `setEnabled(on)` |
| onPointerDown | 162 | 42:createSystems | `onPointerDown` |
| onPointerUp | 163 | 42:createSystems | `onPointerUp` |
| onSystemClick | 165 | 42:createSystems | `onSystemClick` |
| onSystemKey | 166 | 42:createSystems | `onSystemKey` |
| onOverviewClick | 167 | 42:createSystems | `onOverviewClick()` |
| onBackClick | 168 | 42:createSystems | `onBackClick()` |
| onContextToggle | 169 | 42:createSystems | `onContextToggle()` |
| onFlows | 170 | 42:createSystems | `onFlows()` |
| onCovers | 171 | 42:createSystems | `onCovers()` |
| onSchematic | 172 | 42:createSystems | `onSchematic()` |
| onGhost | 173 | 42:createSystems | `onGhost()` |
| onExplode | 174 | 42:createSystems | `onExplode()` |
| deactivate | 183 | 42:createSystems | `deactivate()` |
| setPaused | 183 | 42:createSystems | `setPaused(value)` |
| reset | 183 | 42:createSystems | `reset()` |
| setRevealInExplode | 184 | 42:createSystems | `setRevealInExplode(value)` |
| active | 185 | 42:createSystems | `active()` |
| enabled | 185 | 42:createSystems | `enabled()` |
| state | 185 | 42:createSystems | `state()` |
| ready | 185 | 42:createSystems | `ready()` |
| revealing | 185 | 42:createSystems | `revealing()` |
| context | 185 | 42:createSystems | `context()` |
| parts | 185 | 42:createSystems | `parts()` |
| paused | 185 | 42:createSystems | `paused()` |
| update | 186 | 42:createSystems | `update(dt,now=performance.now()/1000)` |
| dispose | 201 | 42:createSystems | `dispose()` |

## web/src/tunnel-visual.js

[Fonte](../../web/src/tunnel-visual.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createTunnelVisual | 4 | module | `createTunnelVisual({scene, size, studio, camera})` |
| box | 9 | 4:createTunnelVisual | `box(w,h,d,x,y,z,mat=metal)` |
| random | 31 | 4:createTunnelVisual | `random()` |
| setEnabled | 67 | 4:createTunnelVisual | `setEnabled(on)` |
| update | 67 | 4:createTunnelVisual | `update(dt,r,invalid,reduced,settings={})` |

## web/src/wind-tunnel.js

[Fonte](../../web/src/wind-tunnel.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createWindTunnel | 4 | module | `createWindTunnel({scene,model,mechanics,reduced,studio,camera,onToggle,onRegion,onBeforeToggle})` |
| $ | 5 | 4:createWindTunnel | `$` |
| number | 18 | 4:createWindTunnel | `number` |
| params | 19 | 4:createWindTunnel | `params()` |
| fmt | 20 | 4:createWindTunnel | `fmt(v,d=0)` |
| calculate | 21 | 4:createWindTunnel | `calculate()` |
| drawChart | 39 | 4:createWindTunnel | `drawChart(p,allowed)` |
| update | 60 | 4:createWindTunnel | `update(dt)` |

## web/src/workbench.js

[Fonte](../../web/src/workbench.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createWorkbench | 4 | module | `createWorkbench({scene,model,driver,engine,garage,systems,controls,camera,moveCamera,closeEngine,showCar})` |
| $ | 5 | 4:createWorkbench | `$` |
| frame | 14 | 4:createWorkbench | `frame(object)` |
| view | 15 | 4:createWorkbench | `view(name)` |
| rebuild | 23 | 4:createWorkbench | `rebuild()` |
| refreshPanels | 31 | 4:createWorkbench | `refreshPanels()` |
| setTab | 32 | 4:createWorkbench | `setTab(next)` |
| cockpit | 42 | 4:createWorkbench | `cockpit()` |
| downloadModel | 48 | 4:createWorkbench | `downloadModel(kind)` |
| inspecting | 57 | 4:createWorkbench | `inspecting()` |
| update | 58 | 4:createWorkbench | `update()` |
| reset | 59 | 4:createWorkbench | `reset()` |
| systemActive | 60 | 4:createWorkbench | `systemActive()` |

## web/test-aerodynamics.mjs

[Fonte](../../web/test-aerodynamics.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| near | 5 | module | `near(v,w)` |

## web/test-driver-model.mjs

[Fonte](../../web/test-driver-model.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createImageData | 5 | module | `createImageData(w,h)` |
| get | 5 | module | `get(o,k)` |
| createElement | 6 | module | `createElement()` |
| getContext | 6 | 6:createElement | `getContext()` |

## web/test-systems.mjs

[Fonte](../../web/test-systems.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| nodesOf | 88 | module | `nodesOf(id)` |
| find | 89 | module | `find(id, pattern)` |
| center | 90 | module | `center(node)` |
