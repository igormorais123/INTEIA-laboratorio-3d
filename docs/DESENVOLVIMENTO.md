# Desenvolvimento

## Requisitos

- Node.js 24, usado na validação local; npm para instalar dependências.
- Blender 4.5 para editar/reconstruir o master distribuído; Blender 5.2 para reproduzir o gerador procedural de sistemas conforme `ferramentas/gerar_sistemas.py`.
- Navegador com WebGL e aceleração gráfica.

## Site

Na pasta web, execute npm ci, npm run build e npm run dev. O servidor escuta somente 127.0.0.1 e usa a porta 5186 por padrão. Se a porta estiver ocupada, preserve o processo existente e defina outra porta livre em PORT antes de executar. No PowerShell, use `$env:PORT='5190'` e depois `npm --prefix web run dev` a partir da raiz. Confirme que o endereço aberto serve este clone: durante o mapeamento, 5186 servia uma pasta de outputs externa. Ele não publica o projeto na internet.

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

### Gerar os sistemas internos

`ferramentas/gerar_sistemas.py` descobre os módulos `ferramentas/sistemas/sNN_<id>.py`. Cada módulo expõe `SYSTEM=(id, rótulo)` e `build(ctx)`. Execute o Blender a partir da raiz:

```powershell
blender -b --python ferramentas/gerar_sistemas.py
$env:SISTEMAS='brakes,power'; blender -b --python ferramentas/gerar_sistemas.py
$env:PREVIEW='1'; blender -b --python ferramentas/gerar_sistemas.py
```

O primeiro comando gera todos os módulos disponíveis; `SISTEMAS` restringe a geração; `PREVIEW=1` também produz imagens em `ferramentas/sistemas/previews/`. As saídas usam o prefixo `web/assets/sistemas-v1` e incluem manifesto. Trate GLBs, manifestos e prévias como derivados: revise tamanho, lista de sistemas e contagem de peças antes de substituir uma entrega. A geração não conecta automaticamente o asset ao aplicativo web.

## Antes de enviar mudanças

1. Execute `npm --prefix web ci` e `npm --prefix web run build`.
2. Execute `npm --prefix web test` para verificar o modelo e ciclos mecânicos.
3. Abrir a versão construída no navegador; conferir cores, restaurar, montar/desmontar, temas e tela estreita.
4. Para mudanças Blender, executar validate-kit.py e inspecionar a prévia.
5. Atualizar documentação/manifesto, revisar git diff e criar commit.

O teste automatizado não substitui a inspeção visual. Não inclua node_modules, tokens, .env, logs de sessão, arquivos temporários ou backups .blend1.

## Atualizar o mapa do projeto

Após alterar fontes ou documentação, execute `python ferramentas/mapear.py` e `python ferramentas/mapear.py --check` na raiz. O [guia dos mapas](mapas/MANUTENCAO.md) explica cobertura, vínculos e atualização semântica do graphify. Esses comandos não refazem modelos ou exports.
