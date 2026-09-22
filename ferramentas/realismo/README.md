# Acabamento F1 — 22/09/2026

Aplicado ao laboratório e à aula em `inteia-f1-sites`. O carro mantém suas 97 peças, geometria, nomes e mecânica. O Blender produz iluminação e mapas; o navegador continua renderizando o carro em tempo real com Three.js.

## Produção

`gerar_acabamento.py` roda em Blender 5.2 isolado, com Cycles/OptiX na NVIDIA RTX 3060 Ti. Gera um box original com luminárias largas, preenchimento lateral, anteparos escuros e rebotes de luz. Não usa assets de terceiros nem serviços pagos.

- `pitlane-lighting.blend`: cena editável da iluminação; não substitui o modelo mestre do carro.
- `pitlane-cycles.hdr`: panorama linear de 2048 × 1024, 96 amostras.
- `pitlane-cycles-mobile.hdr`: versão 1024 × 512 para telas pequenas.
- `lacquer-cycles-normal.png` e `lacquer-cycles-roughness.png`: mapas de dados 512 × 512, gerados por bake de ruído 4D periódico.
- `generation.json`: dispositivo e parâmetros efetivamente usados.
- `assets-manifest.json`: hashes das quatro cópias de runtime verificadas.

Execute da raiz do laboratório:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --factory-startup --python ferramentas/realismo/gerar_acabamento.py
```

O script exige OptiX e falha se não houver GPU compatível. Não altera configurações do sistema. Após regenerar, copie os quatro assets para `inteia-f1-sites/public/assets`, reconstrua ambos os projetos e rode o sincronizador do checkout de publicação do laboratório.

## Integração

`web/src/cycles-finish.js` e a cópia `src/fx/cycles-finish.js` na aula carregam os arquivos, ajustam a radiância do HDR em 0,32 para a exposição web e criam o ambiente pré-filtrado. Os mapas do verniz afetam a camada transparente; a tinta permanece pigmento sólido. Carbono usa relevo derivado da projeção local, acompanhando as peças ao desmontar.

Na aula, a luz do box ficou mais neutra; ACES substitui AgX, com menos bloom e granulação. Túnel e pista continuam usando seus ambientes próprios. O preset brilhante do laboratório acompanha os novos parâmetros.

## Verificação e limites

Builds e testes dos dois projetos passaram: 76 testes na aula e as 14 suítes do laboratório, incluindo 20 ciclos mecânicos sem deriva. Inspeção visual feita no navegador em desktop e viewport móvel; montagem, box/estúdio e navegação entre capítulos exercitados. Assets HDR/PBR carregaram em ambas as experiências; o navegador identificou a RTX 3060 Ti via ANGLE/D3D11. Capturas em `validacao/`.

O pacote local de publicação inclui os quatro assets adicionais e foi conferido por SHA-256. A publicação usa os sites públicos existentes e mantém os ambientes e recursos já publicados. O resultado é uma melhoria de materiais e iluminação de um modelo didático existente; não é uma certificação de fotorrealismo. Não foi realizado benchmark comparativo de FPS; o modo móvel foi testado por emulação no PC, não em aparelho físico.
