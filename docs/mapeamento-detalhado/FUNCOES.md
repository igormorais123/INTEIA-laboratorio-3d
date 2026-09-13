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
| $ | 18 | module | `$` |
| setFlowXray | 30 | module | `setFlowXray(on)` |
| clone | 31 | 30:setFlowXray | `clone` |
| moveCamera | 37 | module | `moveCamera(to,target,animate=true)` |
| view | 38 | module | `view(name,animate=true)` |
| resize | 40 | module | `resize()` |
| refreshSelection | 42 | module | `refreshSelection()` |
| select | 43 | module | `select(id)` |
| focusPart | 44 | module | `focusPart()` |
| assemblyTo | 45 | module | `assemblyTo(v)` |
| onBeforeToggle | 49 | module | `onBeforeToggle` |
| onRegion | 49 | module | `onRegion` |
| onToggle | 49 | module | `onToggle` |

## web/src/branding.js

[Fonte](../../web/src/branding.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| applyInteiaBranding | 6 | module | `applyInteiaBranding(model, mechanics)` |
| project | 16 | 6:applyInteiaBranding | `project(source,origin,direction,rotation,width,depth)` |
| dispose | 29 | 6:applyInteiaBranding | `dispose()` |

## web/src/customize.js

[Fonte](../../web/src/customize.js)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| setupCustomization | 1 | module | `setupCustomization(materials, studio, renderer, scene)` |
| $ | 2 | 1:setupCustomization | `$` |
| applyLight | 32 | 1:setupCustomization | `applyLight()` |

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

## web/test-aerodynamics.mjs

[Fonte](../../web/test-aerodynamics.mjs)

| Nome | Linha | Escopo | Assinatura |
|---|---:|---|---|
| near | 5 | module | `near(v,w)` |
