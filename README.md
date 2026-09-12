# Laboratório 3D INTEIA

Um laboratório interativo para explorar e personalizar um carro de fórmula: 97 componentes, cores independentes, materiais, iluminação e movimentos ilustrativos. Inclui projeto Blender editável e modelos GLB para reutilização.

![Prévia do projeto Blender](Previa-Blender.png)

## Comece aqui

| Quero… | Abra / leia |
| --- | --- |
| Explorar e trocar cores | [web/index.html](web/index.html) — baixe o repositório e abra no navegador |
| Editar o modelo | [INTEIA_F1_Master.blend](INTEIA_F1_Master.blend) no Blender 4.5 |
| Importar apenas o carro | [GLB estático](modelos/INTEIA_F1_estatico.glb) |
| Reproduzir a demonstração | [GLB animado](modelos/INTEIA_F1_animado.glb) |
| Desenvolver o site | [Desenvolvimento](docs/DESENVOLVIMENTO.md) |
| Usar partes em outro Blender | [Guia Blender](docs/BLENDER.md) |
| Integrar em sites ou jogos | [Integração](docs/INTEGRACAO.md) |
| Entender os arquivos e materiais | [Arquitetura](docs/ARQUITETURA.md) |
| Fazer ensaios por coeficientes | [Túnel de vento](docs/AERODINAMICA.md) |
| Conferir testes e limitações | [Validação](docs/VALIDACAO.md) |

## Download e execução

Clone ou use Code > Download ZIP. O HTML já está pronto e contém o modelo; não requer conta nem chave de API.

```sh
git clone https://github.com/igormorais123/INTEIA-laboratorio-3d.git
cd INTEIA-laboratorio-3d/web
npm ci
npm run build
npm run dev
```

Abra http://127.0.0.1:5186. Também é possível abrir web/index.html diretamente, sem instalar dependências. O link de um HTML dentro do GitHub mostra o código: ele não é um site publicado por si só.

## O que está incluído

- 97 componentes exteriores, separados e nomeados, com metadados de origem.
- Montagem/desmontagem, seleção, isolamento e deslocamento de peças.
- Giro das rodas, direção dianteira e DRS ilustrativos.
- Cores para carroceria, asas, rodas e carbono; quatro acabamentos de pintura.
- Estúdio claro/escuro, luz, piso, fundo e exportação de imagem.
- Túnel de vento didático com vento relativo, forças por coeficientes, gráfico e CSV. Não é CFD da geometria.
- Blender com texturas incorporadas, coleção reutilizável e estúdio separado.
- GLBs estático e animado, fontes web, scripts de conversão e evidências de validação.

As escolhas de personalização ficam na sessão do navegador. Use Salvar imagem para guardar uma imagem do design. O .blend distribuído contém o visual vermelho padrão, não escolhas posteriores feitas no navegador.

## Limites e direitos

É uma representação das peças externas fornecidas, com cerca de 753 mil triângulos. Não contém motor/câmbio completos, rig físico, colisores ou LODs. Os movimentos são ilustrativos; o projeto não foi certificado como réplica técnica nem como indistinguível de uma fotografia.

A origem geométrica é o arquivo de tutorial F1 2026 parte 7 fornecido pelo usuário. A licença desse conteúdo não foi disponibilizada/verificada. Publicidade do repositório não equivale a licença de redistribuição comercial. Consulte [Direitos e procedência](docs/DIREITOS-E-PROCEDENCIA.md). A licença da biblioteca Three.js é preservada em [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
