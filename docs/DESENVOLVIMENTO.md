# Desenvolvimento

## Requisitos

- Node.js 24, usado na validação local; npm para instalar dependências.
- Blender 4.5 para editar ou reconstruir os modelos.
- Navegador com WebGL e aceleração gráfica.

## Site

Na pasta web, execute npm ci, npm run build e npm run dev. O servidor escuta somente 127.0.0.1:5186. Se a porta estiver ocupada, feche a outra instância ou defina PORT antes de executar. Ele não publica o projeto na internet.

Edite src/app-v2.js (integração), src/mechanics.js (movimentos), src/studio.js (materiais/luz), src/customize.js (personalização) e src/template-v2.html (interface). Execute o build após editar. index.html é gerado e versionado para permitir uso imediato; não o edite manualmente.

O build incorpora assets/carro-movable.glb e gera um único HTML offline. O arquivo tem cerca de 36 MB; para produção considere carregar o GLB separadamente, cache e compressão de transporte. Isso ainda não foi implementado neste kit.

## Reconstruir Blender e GLBs

Execute a partir da raiz do repositório, substituindo blender pelo caminho do executável se necessário:

```sh
blender -b --python ferramentas/package_blender.py
node ferramentas/merge-animation.cjs
blender -b --python ferramentas/validate-kit.py
node ferramentas/manifest.cjs
```

O primeiro comando reconstrói e **sobrescreve** o master, os GLBs e a prévia a partir da base web. Faça cópia/commit de edições manuais antes. O segundo reúne os canais exportados em um clipe. O terceiro reabre os arquivos e valida peças/animação/texturas. O último atualiza hashes de arquivos finais.

Os scripts resolvem caminhos pela própria localização; não dependem do computador original. Para trocar a geometria-base, os metadados esperados pelo script precisam ser preservados/adaptados. Não é um conversor genérico de qualquer carro.

## Antes de enviar mudanças

1. npm ci e npm run build na pasta web.
2. npm test para verificar o modelo e ciclos mecânicos.
3. Abrir a versão construída no navegador; conferir cores, restaurar, montar/desmontar, temas e tela estreita.
4. Para mudanças Blender, executar validate-kit.py e inspecionar a prévia.
5. Atualizar documentação/manifesto, revisar git diff e criar commit.

O teste automatizado não substitui a inspeção visual. Não inclua node_modules, tokens, .env, logs de sessão, arquivos temporários ou backups .blend1.
