# Grafos verificáveis

[Índice](README.md) · [Explorar no navegador](index.html) · [Dados e evidências](dependencias.json)

Setas de dependência vão do importador ao módulo importado. Setas de produção vão da entrada à ferramenta ou entrega. Cada aresta abaixo tem evidência; a análise semântica complementar está em [graphify](../../graphify-out/GRAPH_REPORT.md).

## Arquitetura dos módulos web

```mermaid
flowchart LR
  n0["aero-physics.mjs"]
  n1["app-v2.js"]
  n2["branding.js"]
  n3["customize.js"]
  n4["flow-detail.js"]
  n5["garage.js"]
  n6["identity.js"]
  n7["mechanics.js"]
  n8["studio.js"]
  n9["tunnel-visual.js"]
  n10["wind-tunnel.js"]
  n1 -->|"importa"| n2
  n1 -->|"importa"| n6
  n1 -->|"importa"| n5
  n1 -->|"importa"| n10
  n1 -->|"importa"| n3
  n1 -->|"importa"| n8
  n1 -->|"importa"| n7
  n2 -->|"importa"| n6
  n5 -->|"importa"| n6
  n9 -->|"importa"| n4
  n10 -->|"importa"| n9
  n10 -->|"importa"| n0
```

`branding.js` integra a árvore de imports de `app-v2.js`. Dependências externas constam nos dados e na busca.

## Produção do carro

```mermaid
flowchart LR
  n0["INTEIA_F1_Master.blend"]
  n1["Previa-Blender.png"]
  n2["ferramentas/merge-animation.cjs"]
  n3["ferramentas/package_blender.py"]
  n4["modelos/INTEIA_F1_animado.glb"]
  n5["modelos/INTEIA_F1_estatico.glb"]
  n6["texturas/INTEIA_Carbono_BaseColor.png"]
  n7["validacao-criacao.json"]
  n8["web/assets/carro-movable.glb"]
  n9["web/index.html"]
  n10["app-v2.js"]
  n11["template-v2.html"]
  n10 -->|"empacota"| n9
  n11 -->|"incorpora"| n9
  n8 -->|"incorpora"| n9
  n8 -->|"entrada"| n3
  n3 -->|"gera / sobrescreve"| n0
  n3 -->|"gera / sobrescreve"| n5
  n3 -->|"gera / sobrescreve"| n4
  n3 -->|"gera / sobrescreve"| n6
  n3 -->|"gera / sobrescreve"| n1
  n3 -->|"gera / sobrescreve"| n7
  n2 -->|"reescreve clipe"| n4
```

## Produção do box

```mermaid
flowchart LR
  n0["ambientes/INTEIA-box-laboratorio.glb"]
  n1["ambientes/INTEIA_Box_com_carro.blend"]
  n2["ambientes/Previa-Box.png"]
  n3["ambientes/validacao-box.json"]
  n4["ferramentas/package_garage.py"]
  n5["ferramentas/render_garage_preview.py"]
  n6["modelos/INTEIA_F1_estatico.glb"]
  n7["garage.js"]
  n7 -->|"download; cópia manual ao repo"| n0
  n0 -->|"entrada"| n4
  n6 -->|"entrada"| n4
  n4 -->|"gera / sobrescreve"| n1
  n4 -->|"gera / sobrescreve"| n3
  n1 -->|"entrada"| n5
  n5 -->|"renderiza"| n2
```

O download do box é uma etapa humana: o grafo descreve o produtor, sem certificar que o GLB salvo foi exportado do código atual. O original `F1_2026_tutorial_part7_textures.blend` e a etapa inicial de separação não estão disponíveis no repositório.

## Evidências das relações

| Origem | Relação | Destino | Evidência |
| --- | --- | --- | --- |
| `ferramentas/manifest.cjs` | importa | `external:fs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ferramentas/manifest.cjs` | importa | `external:path` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ferramentas/manifest.cjs` | importa | `external:crypto` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ferramentas/merge-animation.cjs` | importa | `external:fs` | [ferramentas/merge-animation.cjs:1](../../ferramentas/merge-animation.cjs#L1) |
| `ferramentas/merge-animation.cjs` | importa | `external:path` | [ferramentas/merge-animation.cjs:1](../../ferramentas/merge-animation.cjs#L1) |
| `web/build.cjs` | importa | `external:fs` | [web/build.cjs:1](../../web/build.cjs#L1) |
| `web/build.cjs` | importa | `external:esbuild` | [web/build.cjs:1](../../web/build.cjs#L1) |
| `web/server.cjs` | importa | `external:http` | [web/server.cjs:1](../../web/server.cjs#L1) |
| `web/server.cjs` | importa | `external:fs` | [web/server.cjs:1](../../web/server.cjs#L1) |
| `web/server.cjs` | importa | `external:path` | [web/server.cjs:1](../../web/server.cjs#L1) |
| `web/src/app-v2.js` | importa | `web/src/branding.js` | [web/src/app-v2.js:1](../../web/src/app-v2.js#L1) |
| `web/src/app-v2.js` | importa | `web/src/identity.js` | [web/src/app-v2.js:2](../../web/src/app-v2.js#L2) |
| `web/src/app-v2.js` | importa | `external:three/addons/exporters/GLTFExporter.js` | [web/src/app-v2.js:3](../../web/src/app-v2.js#L3) |
| `web/src/app-v2.js` | importa | `web/src/garage.js` | [web/src/app-v2.js:4](../../web/src/app-v2.js#L4) |
| `web/src/app-v2.js` | importa | `web/src/wind-tunnel.js` | [web/src/app-v2.js:5](../../web/src/app-v2.js#L5) |
| `web/src/app-v2.js` | importa | `web/src/customize.js` | [web/src/app-v2.js:6](../../web/src/app-v2.js#L6) |
| `web/src/app-v2.js` | importa | `external:three` | [web/src/app-v2.js:7](../../web/src/app-v2.js#L7) |
| `web/src/app-v2.js` | importa | `external:three/addons/controls/OrbitControls.js` | [web/src/app-v2.js:8](../../web/src/app-v2.js#L8) |
| `web/src/app-v2.js` | importa | `external:three/addons/controls/TransformControls.js` | [web/src/app-v2.js:9](../../web/src/app-v2.js#L9) |
| `web/src/app-v2.js` | importa | `external:three/addons/postprocessing/EffectComposer.js` | [web/src/app-v2.js:10](../../web/src/app-v2.js#L10) |
| `web/src/app-v2.js` | importa | `external:three/addons/postprocessing/RenderPass.js` | [web/src/app-v2.js:11](../../web/src/app-v2.js#L11) |
| `web/src/app-v2.js` | importa | `external:three/addons/postprocessing/SSAOPass.js` | [web/src/app-v2.js:12](../../web/src/app-v2.js#L12) |
| `web/src/app-v2.js` | importa | `external:three/addons/postprocessing/OutputPass.js` | [web/src/app-v2.js:13](../../web/src/app-v2.js#L13) |
| `web/src/app-v2.js` | importa | `external:three/addons/postprocessing/SMAAPass.js` | [web/src/app-v2.js:14](../../web/src/app-v2.js#L14) |
| `web/src/app-v2.js` | importa | `external:three/addons/loaders/GLTFLoader.js` | [web/src/app-v2.js:15](../../web/src/app-v2.js#L15) |
| `web/src/app-v2.js` | importa | `web/src/studio.js` | [web/src/app-v2.js:16](../../web/src/app-v2.js#L16) |
| `web/src/app-v2.js` | importa | `web/src/mechanics.js` | [web/src/app-v2.js:17](../../web/src/app-v2.js#L17) |
| `web/src/branding.js` | importa | `web/src/identity.js` | [web/src/branding.js:1](../../web/src/branding.js#L1) |
| `web/src/branding.js` | importa | `external:three` | [web/src/branding.js:2](../../web/src/branding.js#L2) |
| `web/src/branding.js` | importa | `external:three/addons/geometries/DecalGeometry.js` | [web/src/branding.js:3](../../web/src/branding.js#L3) |
| `web/src/flow-detail.js` | importa | `external:three` | [web/src/flow-detail.js:1](../../web/src/flow-detail.js#L1) |
| `web/src/garage.js` | importa | `external:three/addons/lights/RectAreaLightUniformsLib.js` | [web/src/garage.js:1](../../web/src/garage.js#L1) |
| `web/src/garage.js` | importa | `web/src/identity.js` | [web/src/garage.js:2](../../web/src/garage.js#L2) |
| `web/src/garage.js` | importa | `external:three` | [web/src/garage.js:3](../../web/src/garage.js#L3) |
| `web/src/garage.js` | importa | `external:three/addons/geometries/RoundedBoxGeometry.js` | [web/src/garage.js:4](../../web/src/garage.js#L4) |
| `web/src/mechanics.js` | importa | `external:three` | [web/src/mechanics.js:1](../../web/src/mechanics.js#L1) |
| `web/src/tunnel-visual.js` | importa | `web/src/flow-detail.js` | [web/src/tunnel-visual.js:1](../../web/src/tunnel-visual.js#L1) |
| `web/src/tunnel-visual.js` | importa | `external:three` | [web/src/tunnel-visual.js:2](../../web/src/tunnel-visual.js#L2) |
| `web/src/wind-tunnel.js` | importa | `web/src/tunnel-visual.js` | [web/src/wind-tunnel.js:1](../../web/src/wind-tunnel.js#L1) |
| `web/src/wind-tunnel.js` | importa | `external:three` | [web/src/wind-tunnel.js:2](../../web/src/wind-tunnel.js#L2) |
| `web/src/wind-tunnel.js` | importa | `web/src/aero-physics.mjs` | [web/src/wind-tunnel.js:3](../../web/src/wind-tunnel.js#L3) |
| `web/test-aerodynamics.mjs` | importa | `external:node:assert/strict` | [web/test-aerodynamics.mjs:1](../../web/test-aerodynamics.mjs#L1) |
| `web/test-aerodynamics.mjs` | importa | `web/src/aero-physics.mjs` | [web/test-aerodynamics.mjs:2](../../web/test-aerodynamics.mjs#L2) |
| `web/test-mechanics.mjs` | importa | `external:node:fs` | [web/test-mechanics.mjs:1](../../web/test-mechanics.mjs#L1) |
| `web/test-mechanics.mjs` | importa | `external:three` | [web/test-mechanics.mjs:2](../../web/test-mechanics.mjs#L2) |
| `web/test-mechanics.mjs` | importa | `external:three/addons/loaders/GLTFLoader.js` | [web/test-mechanics.mjs:3](../../web/test-mechanics.mjs#L3) |
| `web/test-mechanics.mjs` | importa | `web/src/mechanics.js` | [web/test-mechanics.mjs:4](../../web/test-mechanics.mjs#L4) |
| `web/src/app-v2.js` | empacota | `web/index.html` | [web/build.cjs:2](../../web/build.cjs#L2) |
| `web/src/template-v2.html` | incorpora | `web/index.html` | [web/build.cjs:3](../../web/build.cjs#L3) |
| `web/assets/carro-movable.glb` | incorpora | `web/index.html` | [web/build.cjs:3](../../web/build.cjs#L3) |
| `web/assets/carro-movable.glb` | entrada | `ferramentas/package_blender.py` | [ferramentas/package_blender.py:9](../../ferramentas/package_blender.py#L9) |
| `ferramentas/package_blender.py` | gera / sobrescreve | `INTEIA_F1_Master.blend` | [ferramentas/package_blender.py:145](../../ferramentas/package_blender.py#L145) |
| `ferramentas/package_blender.py` | gera / sobrescreve | `modelos/INTEIA_F1_estatico.glb` | [ferramentas/package_blender.py:126](../../ferramentas/package_blender.py#L126) |
| `ferramentas/package_blender.py` | gera / sobrescreve | `modelos/INTEIA_F1_animado.glb` | [ferramentas/package_blender.py:127](../../ferramentas/package_blender.py#L127) |
| `ferramentas/package_blender.py` | gera / sobrescreve | `texturas/INTEIA_Carbono_BaseColor.png` | [ferramentas/package_blender.py:44](../../ferramentas/package_blender.py#L44) |
| `ferramentas/package_blender.py` | gera / sobrescreve | `Previa-Blender.png` | [ferramentas/package_blender.py:146](../../ferramentas/package_blender.py#L146) |
| `ferramentas/package_blender.py` | gera / sobrescreve | `validacao-criacao.json` | [ferramentas/package_blender.py:148](../../ferramentas/package_blender.py#L148) |
| `ferramentas/merge-animation.cjs` | reescreve clipe | `modelos/INTEIA_F1_animado.glb` | [ferramentas/merge-animation.cjs:4](../../ferramentas/merge-animation.cjs#L4) |
| `web/src/garage.js` | download; cópia manual ao repo | `ambientes/INTEIA-box-laboratorio.glb` | [web/src/app-v2.js:56](../../web/src/app-v2.js#L56) |
| `ambientes/INTEIA-box-laboratorio.glb` | entrada | `ferramentas/package_garage.py` | [ferramentas/package_garage.py:6](../../ferramentas/package_garage.py#L6) |
| `modelos/INTEIA_F1_estatico.glb` | entrada | `ferramentas/package_garage.py` | [ferramentas/package_garage.py:12](../../ferramentas/package_garage.py#L12) |
| `ferramentas/package_garage.py` | gera / sobrescreve | `ambientes/INTEIA_Box_com_carro.blend` | [ferramentas/package_garage.py:72](../../ferramentas/package_garage.py#L72) |
| `ferramentas/package_garage.py` | gera / sobrescreve | `ambientes/validacao-box.json` | [ferramentas/package_garage.py:75](../../ferramentas/package_garage.py#L75) |
| `ambientes/INTEIA_Box_com_carro.blend` | entrada | `ferramentas/render_garage_preview.py` | [ferramentas/render_garage_preview.py:4](../../ferramentas/render_garage_preview.py#L4) |
| `ferramentas/render_garage_preview.py` | renderiza | `ambientes/Previa-Box.png` | [ferramentas/render_garage_preview.py:5](../../ferramentas/render_garage_preview.py#L5) |
| `INTEIA_F1_Master.blend` | reabre / verifica | `ferramentas/validate-kit.py` | [ferramentas/validate-kit.py:5](../../ferramentas/validate-kit.py#L5) |
| `modelos/INTEIA_F1_estatico.glb` | reabre / verifica | `ferramentas/validate-kit.py` | [ferramentas/validate-kit.py:15](../../ferramentas/validate-kit.py#L15) |
| `modelos/INTEIA_F1_animado.glb` | reabre / verifica | `ferramentas/validate-kit.py` | [ferramentas/validate-kit.py:15](../../ferramentas/validate-kit.py#L15) |
| `ferramentas/validate-kit.py` | escreve evidência | `validacao-reabertura.json` | [ferramentas/validate-kit.py:25](../../ferramentas/validate-kit.py#L25) |
| `web/test-mechanics.mjs` | escreve evidência | `validacao-mecanica-web.json` | [web/test-mechanics.mjs:23](../../web/test-mechanics.mjs#L23) |
| `INTEIA_F1_Master.blend` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `modelos/INTEIA_F1_estatico.glb` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `modelos/INTEIA_F1_animado.glb` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `texturas/INTEIA_Carbono_BaseColor.png` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `web/assets/carro-movable.glb` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `web/index.html` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `Previa-Blender.png` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ambientes/INTEIA-box-laboratorio.glb` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ambientes/INTEIA_Box_com_carro.blend` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ambientes/Previa-Box.png` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `identidade/INTEIA-principal.svg` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `identidade/INTEIA-negativo.svg` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `identidade/INTEIA-monocromatico.svg` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `identidade/INTEIA-simbolo.svg` | mede hash | `ferramentas/manifest.cjs` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
| `ferramentas/manifest.cjs` | escreve hashes | `manifesto-sha256.json` | [ferramentas/manifest.cjs:1](../../ferramentas/manifest.cjs#L1) |
