# Integração em sites e jogos

## Qual arquivo escolher

| Arquivo | Uso |
| --- | --- |
| modelos/INTEIA_F1_estatico.glb | Montado, sem ações; ponto de partida para um controlador próprio |
| modelos/INTEIA_F1_animado.glb | Um clipe de demonstração com 104 canais |
| web/assets/carro-movable.glb | Base do site; recebe acabamento e movimentação pelos módulos JavaScript |
| INTEIA_F1_Master.blend | Edição e fonte organizada com estúdio |

GLB usa Y para cima. Blender usa Z para cima. Evite aplicar conversão de eixo duas vezes. Confira escala, orientação e pivôs ao importar no seu motor.

## Three.js

Carregue o GLB com GLTFLoader. Adicione gltf.scene à sua cena. Para a demonstração animada, crie AnimationMixer(gltf.scene), reproduza gltf.animations[0] e atualize o mixer com o delta de tempo em segundos. Configure renderer, câmera, iluminação e redimensionamento no projeto de destino.

O clipe se chama INTEIA_Demonstracao_Montagem_Rodas_DRS. Não aplique simultaneamente esse clipe e mechanics.js às mesmas peças. O site entregue usa seu próprio controlador, não esse clipe.

setupStudio, applyCarMaterials, createMechanics e setupCustomization são exportações dos módulos em web/src. customize.js depende dos IDs do template; não é um widget independente. A interface HTML não vira interface de um motor de jogos ao importar GLB.

## Motores de jogos

Importe o GLB com o importador compatível do motor/versão escolhidos. A entrega foi reimportada no Blender; **não foi testada em Unity, Unreal ou Godot**. Alguns motores precisam de extensão/conversor para glTF: verifique a instalação de destino antes de escolher o fluxo.

O modelo detalhado tem 752.823 triângulos na conversão Blender e 97 meshes. Para jogo, planeje LODs, materiais/draw calls, colisores simples, retopologia e orçamento de texturas conforme a plataforma. Não use cada detalhe visual como colisor físico por padrão. Não há versão low-poly pronta neste repositório.

As articulações ilustram movimentos; não implementam dinâmica de pneus, suspensão, aerodinâmica ou dirigibilidade. A carroceria principal é uma casca conectada, não um conjunto de painéis internos completos.

## Materiais

GLBs contêm materiais PBR e imagens incorporadas. O export pode usar extensões de verniz/transparência; um importador pode apresentar diferenças. Carbono portátil é uma textura com UVs planares; o site usa projeção local em três planos. Para identidade visual entre destinos, calibre iluminação, exposição e materiais em cada motor.
