# Publicação oficial do laboratório

- [Laboratório 3D INTEIA](https://laboratorio-3d-inteia.igor47306.chatgpt.site)
- [Repositório do código](https://github.com/igormorais123/INTEIA-laboratorio-3d)
- [Atlas detalhado local](mapeamento-detalhado/index.html)
- [Atlas de arquivos e peças local](mapas/index.html)

O ambiente oficial de produção é o **ChatGPT Sites**, e é o **único** destino de deploy. O GitHub permanece apenas como repositório e histórico do código: GitHub Pages está desativado e não há GitHub Actions (a conta exige pagamento para executá-las). Build, testes e verificação de mapas rodam localmente antes de cada publicação.

## Identidade imutável do Site

Passe este bloco para outra IA encarregada da publicação:

```text
Site: Laboratório 3D INTEIA
URL oficial: https://laboratorio-3d-inteia.igor47306.chatgpt.site
Provedor: ChatGPT Sites
project_id: appgprj_6aaac720c8b88191be26c74716d13f4d
slug: laboratorio-3d-inteia
manifesto: .openai/hosting.json no checkout de deploy
static.directory: dist
fonte local: C:\Users\IgorPC\.claude\projects\Site aula mota\INTEIA-laboratorio-3d
checkout de deploy: C:\Users\IgorPC\.claude\projects\Site aula mota\INTEIA-laboratorio-3d-site
audiência atual: pública; qualquer pessoa com o link pode acessar
```

O `project_id` identifica o Site existente. Uma IA deve reutilizá-lo e **não chamar `create_site`**. Tokens de envio são temporários e não ficam em arquivos, URLs, configuração Git ou documentação.

## Atualizar a produção

1. Preserve alterações locais e confira `git status` nos dois checkouts.
2. Dentro de `INTEIA-laboratorio-3d/web`, execute:

```powershell
npm ci
npm test
npm run build
npm test
```

`npm ci` pode ser omitido quando as dependências travadas já estiverem instaladas. O build atualiza `web/index.html`.

3. No checkout `INTEIA-laboratorio-3d-site`, sincronize somente os artefatos de runtime:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\sync-from-source.ps1
```

O sincronizador publica oito arquivos: HTML compilado, licença do Three.js, duas marcas SVG, a marca Inteligência Mil Grau e os GLBs de motor, sistemas e peças sobressalentes. O carro principal está incorporado no HTML. Arquivos de geração e o GLB-fonte de 26,45 MB permanecem no repositório-fonte; eles não são carregados pela aplicação e excederiam o limite de 25 MiB por arquivo do Sites.

4. Revise e faça commit apenas no checkout de deploy. Envie o `HEAD` ao remoto `origin` usando uma credencial temporária criada pelas ferramentas do Sites.

   As ferramentas do Sites pertencem ao agente ChatGPT/Codex. Quando quem publica é o Claude Code, delegue esta etapa e as seguintes ao Codex CLI rodando direto no checkout de deploy, sem sandbox:

```powershell
codex exec -s danger-full-access -C "C:\Users\IgorPC\.claude\projects\Site aula mota\INTEIA-laboratorio-3d-site" --skip-git-repo-check "<instruções com project_id, SHA do HEAD e os passos 4 a 6>"
```

   O subagente com sandbox falha no Windows (erro de ACL) e o conector do Sites não repassa tokens; a chamada direta acima é a que funciona.
5. Leia `.openai/hosting.json`, salve uma versão para o SHA completo enviado e publique preservando a audiência pública existente. No Windows, use o build remoto de `save_site_version` quando o empacotador local depender de Bash.
6. Aguarde `get_deployment_status` retornar `succeeded`. Confirme `current_live_url` e a audiência com `get_site` antes de declarar a publicação concluída.

## Critérios de conclusão

- Os testes passam antes e depois do build.
- `sync-from-source.ps1` termina sem arquivo acima de 25 MiB.
- O checkout de deploy está limpo e o commit está no remoto do Sites.
- A nova versão chega a `succeeded` e mantém a URL oficial.
- O Site continua público; não restrinja a audiência sem autorização explícita do usuário.

## Estado da migração

Em 16 de setembro de 2026, o ChatGPT Sites publicou o laboratório em produção e confirmou a URL oficial acima. A audiência foi alterada para pública, permitindo acesso por qualquer pessoa com o link. O GitHub Pages anterior foi desativado; links de produção devem apontar somente para `chatgpt.site`. Em 17 de setembro de 2026, o fluxo de verificação no GitHub Actions foi removido do repositório, porque a conta do GitHub passou a exigir pagamento para executá-lo; desde então todo deploy acontece exclusivamente no ChatGPT Sites.
