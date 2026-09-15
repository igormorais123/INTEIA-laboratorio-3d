# Índice de funções e métodos

[Índice](README.md) · [Busca interativa](index.html) · [JSON](dados/simbolos.json)

tree-sitter-javascript: declarações nomeadas, arrow functions atribuídas e métodos; Python ast: funções/classes. Callbacks anônimos e resolução dinâmica não são indexados integralmente.

Chamadas são referências sintáticas conservadoras, não rastreamento de execução. Funções anônimas e métodos dinâmicos exigem a leitura dos módulos.

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

## ferramentas/validate-kit.py

[Fonte](../../ferramentas/validate-kit.py)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| matrices | 7 | module | `def matrices():` |

## web/src/aero-physics.mjs

[Fonte](../../web/src/aero-physics.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| aerodynamicTest | 2 | module | `aerodynamicTest({speedKmh=0,headwindKmh=0,crosswindKmh=0,temperatureC=15,pressureKPa=101.325,area=null,cd=null,clDown=null,length=5.5})` |

## web/src/app-v2.js

[Fonte](../../web/src/app-v2.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| $ | 24 | module | `$` |
| closeEngine | 35 | module | `closeEngine()` |
| setFlowXray | 37 | module | `setFlowXray(on)` |
| clone | 38 | 37:setFlowXray | `clone` |
| moveCamera | 45 | module | `moveCamera(to,target,animate=true)` |
| view | 46 | module | `view(name,animate=true)` |
| resize | 48 | module | `resize()` |
| refreshSelection | 50 | module | `refreshSelection()` |
| select | 51 | module | `select(id)` |
| focusPart | 52 | module | `focusPart()` |
| assemblyTo | 53 | module | `assemblyTo(v)` |
| target | 64 | module | `target()` |
| onBeforeToggle | 65 | module | `onBeforeToggle` |
| onRegion | 65 | module | `onRegion` |
| onToggle | 65 | module | `onToggle` |
| showCar | 66 | module | `showCar()` |

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
| createWorkbench | 4 | module | `createWorkbench({scene,model,driver,engine,garage,controls,camera,moveCamera,closeEngine,showCar})` |
| $ | 5 | 4:createWorkbench | `$` |
| frame | 11 | 4:createWorkbench | `frame(object)` |
| view | 12 | 4:createWorkbench | `view(name)` |
| rebuild | 20 | 4:createWorkbench | `rebuild()` |
| refreshPanels | 28 | 4:createWorkbench | `refreshPanels()` |
| setTab | 29 | 4:createWorkbench | `setTab(next)` |
| cockpit | 38 | 4:createWorkbench | `cockpit()` |
| downloadModel | 44 | 4:createWorkbench | `downloadModel(kind)` |
| inspecting | 53 | 4:createWorkbench | `inspecting()` |
| update | 54 | 4:createWorkbench | `update()` |
| reset | 55 | 4:createWorkbench | `reset()` |

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
