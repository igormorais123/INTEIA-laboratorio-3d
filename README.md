# Laboratório 3D INTEIA

Um laboratório interativo para explorar e personalizar um carro de fórmula: 97 componentes exteriores, motor V6 ilustrativo integrado, patrocínios do F1 Loop, cores independentes, materiais, iluminação e movimentos ilustrativos. Inclui projeto Blender editável e modelos GLB para reutilização.

**[Abrir o laboratório online](https://igormorais123.github.io/INTEIA-laboratorio-3d/)** · **[Atlas detalhado online](https://igormorais123.github.io/INTEIA-laboratorio-3d/docs/mapeamento-detalhado/index.html)** · [Publicação e atualização](docs/PUBLICACAO.md)

![Prévia do projeto Blender](Previa-Blender.png)

## Comece aqui

**[Atlas do código, documentos e assets](docs/mapas/README.md)** — índice navegável, busca de arquivos e peças, grafos com evidências e [guia de reaproveitamento](docs/mapas/REUSO.md). Para a busca offline, baixe o repositório e abra [docs/mapas/index.html](docs/mapas/index.html).

| Quero… | Abra / leia |
| --- | --- |
| Explorar e trocar cores | [Laboratório publicado](https://igormorais123.github.io/INTEIA-laboratorio-3d/) ou [HTML para uso local](web/index.html) |
| Editar o modelo | [INTEIA_F1_Master.blend](INTEIA_F1_Master.blend) no Blender 4.5 |
| Usar a identidade visual | [Marca e variantes SVG](identidade/LEIA-ME.md) |
| Explorar o box-laboratório | [Guia do ambiente](docs/BOX-LABORATORIO.md) · [Box GLB](ambientes/INTEIA-box-laboratorio.glb) · [Blender com carro](ambientes/INTEIA_Box_com_carro.blend) |
| Importar apenas o carro | [GLB estático](modelos/INTEIA_F1_estatico.glb) |
| Reproduzir a demonstração | [GLB animado](modelos/INTEIA_F1_animado.glb) |
| Desenvolver o site | [Desenvolvimento](docs/DESENVOLVIMENTO.md) |
| Usar partes em outro Blender | [Guia Blender](docs/BLENDER.md) |
| Integrar em sites ou jogos | [Integração](docs/INTEGRACAO.md) |
| Entender os arquivos e materiais | [Arquitetura](docs/ARQUITETURA.md) |
| Fazer ensaios por coeficientes | [Túnel de vento](docs/AERODINAMICA.md) |
| Conferir testes e limitações | [Validação](docs/VALIDACAO.md) |

## Download e execução

Para continuar o trabalho em outra máquina, siga o [guia de instalação e sincronização entre PCs](docs/OUTRO-PC.md).

Clone ou use Code > Download ZIP. O HTML já está pronto e contém o carro final v2; o motor e as marcas são carregados de web/assets. Não requer conta nem chave de API.

```sh
git clone https://github.com/igormorais123/INTEIA-laboratorio-3d.git
cd INTEIA-laboratorio-3d/web
npm ci
npm run build
npm run dev
```

Abra http://127.0.0.1:5186 se essa for a porta livre usada por este servidor. Se já estiver ocupada, preserve o processo existente e escolha outra porta com `PORT`; veja [Desenvolvimento](docs/DESENVOLVIMENTO.md). Use o laboratório publicado ou o servidor local para carregar também o motor e os patrocínios. O link de um HTML dentro do GitHub mostra o código: ele não é um site publicado por si só.

## Atualização do carro e motor

O laboratório usa o mesmo carro v2, pintura final, rodas, piloto e patrocínios do F1 Loop: assinatura e brasão INTEIA, número 1 e Inteligência Mil Grau. Abra **MOTOR / V6 TURBO** para levantar a tampa, cortar a vista para mostrar os pistões e pausar/retomar. **Desmontar** mantém o motor visível dentro do conjunto. O túnel fecha a tampa automaticamente.

[Detalhes da integração](docs/INTEGRACAO-MOTOR.md).

## Bancadas de modelagem

As abas **Carro, Motor, Capacete, Piloto e Ambientes** organizam a oficina. O capacete detalhado de 1991 é compartilhado entre o carro e a bancada. O piloto tem corpo completo em postura reclinada, luvas com dedos, botas, costuras e cintos. As bancadas de capacete e piloto permitem alternar entre inspeção isolada e encaixe no cockpit e baixar GLB. Ajustes de altura, avanço e inclinação do capacete ficam na sessão e são incluídos ao exportar o piloto.

[Referências e limites do estudo](docs/PILOTO-E-CAPACETE.md).

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

É uma representação das peças externas fornecidas, com cerca de 260 mil triângulos no carro v2, além do motor e dos detalhes adicionais. Inclui o motor V6 didático do F1 Loop; não contém câmbio completo, rig físico ou colisores. Os arquivos Blender e GLB da pasta modelos continuam sendo a entrega original; esta atualização refere-se ao laboratório web. Os movimentos são ilustrativos; o projeto não foi certificado como réplica técnica nem como indistinguível de uma fotografia.

**© 2026 INTEIA — todos os direitos reservados.** O Laboratório 3D INTEIA é um projeto de titularidade da INTEIA, sob [licença proprietária](LICENSE). Estar público não concede uma licença de código aberto. A procedência dos assets e as licenças de terceiros estão registradas separadamente em [Direitos e procedência](docs/DIREITOS-E-PROCEDENCIA.md) e [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
