# Continuar em outro PC

## Primeira instalação

Instale Git e Node.js 24 (com npm). Para editar os arquivos `.blend`, instale também Blender 4.5. No PowerShell, entre na pasta onde deseja guardar o projeto e execute:

```powershell
git clone https://github.com/igormorais123/INTEIA-laboratorio-3d.git
cd INTEIA-laboratorio-3d
npm --prefix web ci
npm --prefix web run build
npm --prefix web test
npm --prefix web run dev
```

Abra http://127.0.0.1:5186 no navegador. Mantenha o terminal do servidor aberto; use Ctrl+C para encerrar. Se a porta estiver ocupada, use `$env:PORT='5190'` antes de iniciar e abra http://127.0.0.1:5190.

O clone inclui código-fonte, documentação, identidade visual, texturas, modelos GLB e projetos Blender. As dependências são instaladas com `npm ci`; caches, arquivos temporários e backups automáticos do Blender ficam fora do Git.

## Alternar entre computadores

Antes de começar, confira se não há alterações locais pendentes:

```powershell
git status
git pull --ff-only
npm --prefix web ci
```

Se houver trabalho local pendente, salve-o em um commit antes de sincronizar. Se o pull indicar históricos divergentes, preserve os commits e resolva a integração antes de continuar; não use push forçado para alternar de computador.

Depois de editar, execute os testes e o build quando houver mudanças no site, confira o resultado no navegador e envie:

```powershell
git status
git diff
git add .
git diff --cached --stat
git commit -m "Descreve a alteração realizada"
git push origin main
```

Revise os arquivos preparados antes do commit para não incluir dados privados. O push exige autenticação no GitHub com acesso ao repositório. No outro computador, repita o pull antes de editar. Mudanças ainda não enviadas ficam somente no computador em que foram feitas.

## Documentação

- [Índice geral e arquivos do projeto](../README.md)
- [Desenvolvimento e reconstrução dos modelos](DESENVOLVIMENTO.md)
- [Arquitetura](ARQUITETURA.md)
- [Guia Blender](BLENDER.md)
- [Publicação do site](PUBLICACAO.md)
- [Atlas do código e assets](mapas/README.md)
- [Mapeamento detalhado](mapeamento-detalhado/README.md)

O envio ao GitHub sincroniza os arquivos; o servidor local é iniciado separadamente em cada computador.
