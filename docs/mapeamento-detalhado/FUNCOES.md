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
| measure_glb | 158 | module | `def measure_glb(path):` |
| write_manifest | 185 | module | `def write_manifest(path_glb, optimized):` |
| light | 230 | module | `def light(name, kind, loc, energy, size=2.0):` |
| frame | 248 | module | `def frame(objs, direction, pad=1.25):` |

## ferramentas/gerar_sobressalentes.py

[Fonte](../../ferramentas/gerar_sobressalentes.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| surface_y | 55 | module | `def surface_y(x, z, r=.035):` |
| spare | 62 | module | `def spare(obj, slot, variant, target, label, mode='geometry', **extra):` |
| tyre_profile | 94 | module | `def tyre_profile(width, R):` |
| tyre_texture | 99 | module | `def tyre_texture(kind, band, size=(1024, 512)):` |
| build_tyre | 139 | module | `def build_tyre(name, center, width, R, mat):` |
| wing_section | 174 | module | `def wing_section(le, chord, angle_deg, thick=.10, camber=-.05, n=16):` |
| span_loft | 188 | module | `def span_loft(name, xs, section_at, mat):` |
| fw_at | 214 | module | `def fw_at(ax, d_angle, k_chord):` |
| sec | 225 | module | `def sec(x, da=da, kc=kc):` |
| bbox_web | 266 | module | `def bbox_web(o):` |

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
| W | 16 | module | `def W(x, y=None, z=None):` |
| to_web | 22 | module | `def to_web(v):` |
| _encode_normal | 32 | module | `def _encode_normal(height, strength=1.0):` |
| image_from_array | 39 | module | `def image_from_array(name, rgba, srgb=True):` |
| tex_twill | 51 | module | `def tex_twill(size=256, tow=16, base=(.028, .032, .038), lift=.055):` |
| tex_kevlar | 62 | module | `def tex_kevlar(size=256, tow=12):` |
| tex_brushed | 71 | module | `def tex_brushed(size=256):` |
| tex_cast | 78 | module | `def tex_cast(size=256):` |
| tex_heat | 87 | module | `def tex_heat(size=256):` |
| tex_brake_disc | 100 | module | `def tex_brake_disc(size=512, rings=14, holes_per_ring=64, inner=.42):` |
| tex_fins | 122 | module | `def tex_fins(size=256, pitch=6):` |
| tex_honeycomb | 129 | module | `def tex_honeycomb(size=256, cell=18):` |
| tex_kapton | 139 | module | `def tex_kapton(size=256):` |
| tex_braid | 145 | module | `def tex_braid(size=128, tow=8):` |
| _seg7 | 152 | module | `def _seg7(img, ch, x0, y0, w, h, t, col):` |
| rect | 156 | 152:_seg7 | `def rect(xa, ya, xb, yb):` |
| _text7 | 174 | module | `def _text7(img, text, x, y, w, h, t, col, gap=None):` |
| tex_display | 181 | module | `def tex_display(size=(512, 256)):` |
| box | 187 | 181:tex_display | `def box(xa, ya, xb, yb, col):` |
| material | 217 | module | `def material(name, color, metallic=0.0, roughness=0.45, *, emissive=None, emissive_strength=1.0, alpha=1.0,` |
| tex_node | 249 | 217:material | `def tex_node(img):` |
| Materials | 276 | module | `class Materials:` |
| __init__ | 278 | 276:Materials | `def __init__(self):` |
| Context | 366 | module | `class Context:` |
| __init__ | 367 | 366:Context | `def __init__(self, scene, mats):` |
| system | 375 | 366:Context | `def system(self, sid, label):` |
| register | 385 | 366:Context | `def register(self, obj, part, *, spin=None, spin_axis='y', flow=None, era=None, explode=None, hide_group=None, tag=None, carrier=False, parent=None):` |
| _link | 412 | module | `def _link(obj):` |
| shade_smooth | 416 | module | `def shade_smooth(obj, angle=math.radians(38)):` |
| bevel | 430 | module | `def bevel(obj, width=.002, segments=2, angle=math.radians(40)):` |
| box_uv | 438 | module | `def box_uv(obj, scale=1.0, offset=(0.0, 0.0)):` |
| mesh_object | 458 | module | `def mesh_object(name, verts, faces, edges=(), uvs=None):` |
| bm_to_object | 470 | module | `def bm_to_object(name, bm, smooth=True):` |
| set_material | 479 | module | `def set_material(obj, mat):` |
| orient | 485 | module | `def orient(obj, axis):` |
| cube | 493 | module | `def cube(ctx, part, center, size, mat, *, bev=.002, segments=2, rot=None, uv=None, **extras):` |
| W_rot | 507 | module | `def W_rot(rot):` |
| cyl | 513 | module | `def cyl(ctx, part, center, radius, length, mat, *, axis=UP, verts=32, bev=.0012, segments=2, radius2=None, **extras):` |
| tube_cyl | 522 | module | `def tube_cyl(ctx, part, center, radius, wall, length, mat, *, axis=UP, verts=32, **extras):` |
| sphere | 543 | module | `def sphere(ctx, part, center, radius, mat, *, segments=24, rings=16, scale=None, **extras):` |
| torus | 551 | module | `def torus(ctx, part, center, major, minor, mat, *, axis=UP, seg=40, mseg=12, **extras):` |
| catmull | 558 | module | `def catmull(points, per_segment=8, closed=False):` |
| _frames | 576 | module | `def _frames(pts, closed=False):` |
| sweep | 601 | module | `def sweep(ctx, part, points, mat, *, radius=.01, radii=None, sides=14, smooth_path=True, per_segment=8,` |
| airfoil | 658 | module | `def airfoil(chord, thick, camber=0.0, n=18):` |
| loft | 675 | module | `def loft(ctx, part, sections, mat, *, cap=True, open_ring=False, **extras):` |
| lathe | 700 | module | `def lathe(ctx, part, profile, mat, *, center=(0, 0, 0), axis=UP, segments=40, **extras):` |
| helix | 714 | module | `def helix(ctx, part, center, radius, pitch, turns, wire, mat, *, axis=UP, per_turn=28, **extras):` |
| gear | 724 | module | `def gear(ctx, part, center, teeth, module, width, mat, *, axis=UP, bore=None, helix_deg=0, hub_r=None, hub_w=None, spokes=0, **extras):` |
| ring | 740 | 724:gear | `def ring(z, pts):` |
| bolt_ring | 776 | module | `def bolt_ring(ctx, part, center, radius, count, axis, mat_head, *, size=.006, head=.004, start=0.0, **extras):` |
| join | 799 | module | `def join(ctx, objects, part=None, **extras):` |
| mirror_x | 825 | module | `def mirror_x(ctx, obj, part=None):` |
| mirror_system | 848 | module | `def mirror_system(ctx, sid):` |
| both_sides | 880 | module | `def both_sides(fn):` |
| hexagon | 884 | module | `def hexagon(r):` |
| rounded_rect | 887 | module | `def rounded_rect(w, h, r, n=4):` |
| super_ellipse | 895 | module | `def super_ellipse(w, h, n=2.6, seg=32, exp=None):` |
| shell | 904 | module | `def shell(ctx, part, sections, mat, *, thickness=.004, open_ring=False, **extras):` |
| flow_ribbon | 910 | module | `def flow_ribbon(ctx, part, points, kind, *, radius=.006, **extras):` |
| text_plate | 914 | module | `def text_plate(ctx, part, text, center, size, mat, *, normal=FWD, up=UP, depth=.0006, **extras):` |
| centroid | 930 | module | `def centroid(objs):` |
| auto_explode | 941 | module | `def auto_explode(ctx, sid, scale=1.0, min_len=.06):` |
| car_components | 959 | module | `def car_components(source='main_body__01'):` |
| car_part | 997 | module | `def car_part(ctx, part, mat, *, source='main_body__01', box=None, select=None, smooth_angle=math.radians(45), uv=8, **extras):` |
| plate | 1017 | module | `def plate(ctx, part, outline, center, thickness, mat, *, normal=FWD, up=UP, bev=.0015, uv=8, **extras):` |
| P | 1024 | 1017:plate | `def P(u, v, w):` |
| lado | 1037 | module | `def lado(side, fem=False):` |
| arc2d | 1043 | module | `def arc2d(cx, cy, r, a0, a1, n=6):` |
| face_uv_fit | 1047 | module | `def face_uv_fit(obj, normal=FWD, tol=.9):` |

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
| build | 20 | module | `def build(ctx):` |

## ferramentas/sistemas/s12_cockpit.py

[Fonte](../../ferramentas/sistemas/s12_cockpit.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| strap | 19 | module | `def strap(ctx, name, pts, width=.075):` |
| build | 22 | module | `def build(ctx):` |
| seat_section | 26 | 22:build | `def seat_section(t):` |

## ferramentas/sistemas/s13_wheel.py

[Fonte](../../ferramentas/sistemas/s13_wheel.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| build | 21 | module | `def build(ctx):` |
| Q | 25 | 21:build | `def Q(u, v, w=0.0):` |
| E | 28 | 21:build | `def E(u, v, w):` |

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
| $ | 27 | module | `$` |
| closeEngine | 38 | module | `closeEngine()` |
| setFlowXray | 40 | module | `setFlowXray(on)` |
| clone | 41 | 40:setFlowXray | `clone` |
| moveCamera | 48 | module | `moveCamera(to,target,animate=true)` |
| setCarSelectionEnabled | 49 | module | `setCarSelectionEnabled(enabled)` |
| syncSystemMode | 50 | module | `syncSystemMode()` |
| view | 52 | module | `view(name,animate=true)` |
| resize | 57 | module | `resize()` |
| refreshSelection | 59 | module | `refreshSelection()` |
| setupSparesUI | 62 | module | `setupSparesUI()` |
| setSpareStatus | 68 | module | `setSpareStatus(text)` |
| showSpareInfo | 69 | module | `showSpareInfo(slotId,variant)` |
| renderInto | 70 | module | `renderInto(box,info)` |
| syncSpares | 71 | module | `syncSpares(setup,state)` |
| renderSelectedInfo | 72 | module | `renderSelectedInfo(info)` |
| select | 73 | module | `select(id)` |
| focusPart | 74 | module | `focusPart()` |
| assemblyTo | 75 | module | `assemblyTo(v)` |
| target | 86 | module | `target()` |
| showCar | 87 | module | `showCar()` |
| onClose | 87 | module | `onClose()` |
| onBeforeToggle | 87 | module | `onBeforeToggle` |
| onRegion | 87 | module | `onRegion` |
| onToggle | 87 | module | `onToggle` |
| showCar | 88 | module | `showCar()` |
| systemsSpreadTo | 104 | module | `systemsSpreadTo(v)` |

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

## web/src/parts-info.js

[Fonte](../../web/src/parts-info.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| R | 6 | module | `R(pattern, funcao, curiosidade)` |
| describePart | 361 | module | `describePart(part, systemId)` |
| describeCarPart | 442 | module | `describeCarPart(label, category)` |

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

## web/src/spares.js

[Fonte](../../web/src/spares.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| createSpares | 48 | module | `createSpares({model,mechanics,assetUrl=SPARES_ASSET,onChange=()=>{}}={})` |
| targetObject | 55 | 48:createSpares | `targetObject` |
| load | 57 | 48:createSpares | `load()` |
| remember | 64 | 48:createSpares | `remember(target)` |
| revert | 66 | 48:createSpares | `revert(slot)` |
| applySlot | 71 | 48:createSpares | `applySlot(slot,variant)` |
| set | 83 | 48:createSpares | `set(slot,variant)` |
| preset | 92 | 48:createSpares | `preset(id)` |
| presetMatching | 94 | 48:createSpares | `presetMatching()` |
| describe | 98 | 48:createSpares | `describe(slot,variant)` |
| setup | 99 | 48:createSpares | `setup()` |
| state | 99 | 48:createSpares | `state()` |
| ready | 99 | 48:createSpares | `ready()` |
| reset | 100 | 48:createSpares | `reset()` |
| dispose | 101 | 48:createSpares | `dispose()` |

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
| advanceLocalSpin | 32 | module | `advanceLocalSpin(quaternion,axis='y',angle=0)` |
| flowTexture | 35 | module | `flowTexture()` |
| createSystems | 43 | module | `createSystems({scene,model,mechanics,engine,driver,garage,camera,canvas,moveCamera,showCar=()=>{},onClose=showCar,mobile=false,assetUrl=SYSTEMS_ASSET})` |
| onVisibilityChange | 51 | 43:createSystems | `onVisibilityChange()` |
| meta | 53 | 43:createSystems | `meta` |
| flowMaterial | 58 | 43:createSystems | `flowMaterial` |
| cardFor | 67 | 43:createSystems | `cardFor` |
| logicalPartCount | 68 | 43:createSystems | `logicalPartCount` |
| syncView | 69 | 43:createSystems | `syncView` |
| setStatus | 70 | 43:createSystems | `setStatus` |
| attachPart | 73 | 43:createSystems | `attachPart(mesh,systemId,logicalOwner=mesh.uuid)` |
| prepareMaterials | 85 | 43:createSystems | `prepareMaterials(sceneRoot)` |
| distribute | 94 | 43:createSystems | `distribute(gltf)` |
| ownerId | 96 | 94:distribute | `ownerId` |
| load | 111 | 43:createSystems | `load()` |
| applyEra | 126 | 43:createSystems | `applyEra()` |
| applyCovers | 127 | 43:createSystems | `applyCovers()` |
| applyExplode | 130 | 43:createSystems | `applyExplode()` |
| translucentOf | 138 | 43:createSystems | `translucentOf` |
| materialFor | 139 | 43:createSystems | `materialFor(entry)` |
| applyFlows | 140 | 43:createSystems | `applyFlows()` |
| applySchematic | 141 | 43:createSystems | `applySchematic()` |
| highlight | 143 | 43:createSystems | `highlight(entry,on)` |
| setPicked | 150 | 43:createSystems | `setPicked(entry)` |
| setERSContext | 164 | 43:createSystems | `setERSContext(mode)` |
| updateUI | 165 | 43:createSystems | `updateUI(id=active)` |
| objectFor | 170 | 43:createSystems | `objectFor(id)` |
| geometryBounds | 171 | 43:createSystems | `geometryBounds(object)` |
| viewportAspect | 172 | 43:createSystems | `viewportAspect()` |
| dirFor | 175 | 43:createSystems | `dirFor(id,name)` |
| frame | 176 | 43:createSystems | `frame(id,direction=dirFor(id,currentView),animate=true)` |
| show | 177 | 43:createSystems | `show(id='overview',animate=true)` |
| view | 178 | 43:createSystems | `view(name)` |
| captureGhost | 179 | 43:createSystems | `captureGhost()` |
| cloneMaterial | 179 | 179:captureGhost | `cloneMaterial` |
| setGhost | 180 | 43:createSystems | `setGhost(on)` |
| setEnabled | 181 | 43:createSystems | `setEnabled(on)` |
| onPointerDown | 185 | 43:createSystems | `onPointerDown` |
| pickFromEvent | 186 | 43:createSystems | `pickFromEvent(event)` |
| onPointerUp | 187 | 43:createSystems | `onPointerUp` |
| onSystemClick | 189 | 43:createSystems | `onSystemClick` |
| onSystemKey | 190 | 43:createSystems | `onSystemKey` |
| onOverviewClick | 191 | 43:createSystems | `onOverviewClick()` |
| onBackClick | 192 | 43:createSystems | `onBackClick()` |
| onContextToggle | 193 | 43:createSystems | `onContextToggle()` |
| onFlows | 194 | 43:createSystems | `onFlows()` |
| onCovers | 195 | 43:createSystems | `onCovers()` |
| onSchematic | 196 | 43:createSystems | `onSchematic()` |
| onGhost | 197 | 43:createSystems | `onGhost()` |
| onExplode | 198 | 43:createSystems | `onExplode()` |
| deactivate | 207 | 43:createSystems | `deactivate()` |
| setPaused | 207 | 43:createSystems | `setPaused(value)` |
| reset | 207 | 43:createSystems | `reset()` |
| clearPick | 207 | 43:createSystems | `clearPick()` |
| systemLabel | 207 | 43:createSystems | `systemLabel(id)` |
| setSpread | 207 | 43:createSystems | `setSpread(value)` |
| spread | 207 | 43:createSystems | `spread()` |
| setRevealInExplode | 208 | 43:createSystems | `setRevealInExplode(value)` |
| active | 209 | 43:createSystems | `active()` |
| enabled | 209 | 43:createSystems | `enabled()` |
| state | 209 | 43:createSystems | `state()` |
| ready | 209 | 43:createSystems | `ready()` |
| revealing | 209 | 43:createSystems | `revealing()` |
| context | 209 | 43:createSystems | `context()` |
| parts | 209 | 43:createSystems | `parts()` |
| paused | 209 | 43:createSystems | `paused()` |
| update | 210 | 43:createSystems | `update(dt,now=performance.now()/1000)` |
| dispose | 225 | 43:createSystems | `dispose()` |

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

## web/test-spares.mjs

[Fonte](../../web/test-spares.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| read | 6 | module | `read(path)` |
| near | 41 | module | `near(entry, box, tol = .06)` |

## web/test-systems.mjs

[Fonte](../../web/test-systems.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| nodesOf | 89 | module | `nodesOf(id)` |
| find | 90 | module | `find(id, pattern)` |
| center | 91 | module | `center(node)` |
