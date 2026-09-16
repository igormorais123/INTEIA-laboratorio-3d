"""Inventário e mapas reproduzíveis. Python 3.10+, stdlib, nenhum export 3D.

Uso na raiz: python ferramentas/mapear.py [--check]
O check é somente leitura e falha se os mapas estiverem desatualizados.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import struct
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/mapas'
GENERATED = {
    'docs/mapas/inventario.json', 'docs/mapas/INVENTARIO.md',
    'docs/mapas/dependencias.json', 'docs/mapas/GRAFOS.md',
    'docs/mapas/controles.json', 'docs/mapas/componentes.json',
    'docs/mapas/index.html', 'docs/mapas/cobertura.json',
}
BINARY = {'.glb', '.blend', '.png'}

# O atlas detalhado cataloga os nossos derivados. Não criar hashes circulares:
# suas saídas continuam no inventário, e o validador próprio confere seu conteúdo.
DETAILED_GENERATED = {'docs/mapeamento-detalhado/' + p for p in {
    'ARVORE.md', 'CATALOGO.md', 'FUNCOES.md', 'index.html',
    'dados/catalogo.csv', 'dados/catalogo.json', 'dados/cobertura.json',
    'dados/componentes.json', 'dados/entrega.json', 'dados/grafo.json',
    'dados/manifesto-conferencia.json', 'dados/simbolos.json',
    'dados/teste-mecanica.json', 'dados/validacao.json', 'dados/verificacao-app.json',
    'grafos/arquitetura.json', 'grafos/arquitetura.mmd',
    'grafos/assets.json', 'grafos/assets.mmd',
    'grafos/dados.json', 'grafos/dados.mmd',
}}


def is_generated(path):
    return path in GENERATED or path in DETAILED_GENERATED or path.startswith('graphify-out/')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def line_of(path, needle):
    text = read(path)
    pos = text.find(needle)
    if pos < 0:
        raise ValueError(f'Evidência ausente: {path}: {needle}')
    return text.count('\n', 0, pos) + 1


def href(path, line=None):
    return '../../' + quote(path, safe='/.-_') + (f'#L{line}' if line else '')


def file_list():
    raw = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT)
    files = {p for p in raw.decode('utf-8').split('\0') if p and (ROOT / p).is_file()}
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0'))
    # Trabalho paralelo não versionado não pertence a esta entrega. Se for
    # incorporado futuramente ao Git, será incluído automaticamente no inventário.
    files = {p for p in files if not p.startswith('docs/mapeamento-detalhado/') or p in tracked}
    # Graphify tem um snapshot independente. Incluímos entregas finais, nunca caches.
    files = {p for p in files if not p.startswith('graphify-out/') or p in {
        'graphify-out/graph.json', 'graphify-out/graph.html', 'graphify-out/GRAPH_REPORT.md'}}
    return sorted(files | GENERATED)


def category(path):
    p = Path(path)
    if is_generated(path):
        return 'mapa gerado'
    if path == 'web/index.html':
        return 'aplicação gerada'
    if p.suffix == '.blend':
        return 'entrega editável Blender'
    if path == 'web/assets/carro-movable.glb':
        return 'base geométrica derivada'
    if p.suffix == '.glb':
        return 'entrega GLB'
    if 'validacao' in p.name or path == 'manifesto-sha256.json':
        return 'evidência gerada'
    if path.startswith('texturas/'):
        return 'textura gerada'
    if p.suffix == '.png':
        return 'prévia histórica'
    if p.suffix == '.svg' or path.startswith('identidade/'):
        return 'identidade editável'
    if path == 'documentacao/componentes-origem.json':
        return 'metadados de procedência'
    if 'LICENSE' in p.name or 'NOTICES' in p.name or 'DIREITOS' in p.name:
        return 'licença ou procedência'
    if p.suffix in {'.md', '.html'} and not path.startswith('web/src/'):
        return 'documentação'
    if 'test-' in p.name:
        return 'teste'
    if path.startswith('ferramentas/'):
        return 'ferramenta editável'
    if path.startswith('web/src/'):
        return 'fonte web editável'
    return 'configuração ou infraestrutura'


def glb_info(path):
    data = (ROOT / path).read_bytes()
    magic, version, length = struct.unpack_from('<III', data)
    assert magic == 0x46546C67 and version == 2 and length == len(data), path
    size, kind = struct.unpack_from('<II', data, 12)
    assert kind == 0x4E4F534A, path
    doc = json.loads(data[20:20 + size])
    triangles = 0
    for mesh in doc.get('meshes', []):
        for prim in mesh['primitives']:
            assert prim.get('mode', 4) == 4, f'Modo não triangular: {path}'
            accessor = prim.get('indices', prim['attributes']['POSITION'])
            triangles += doc['accessors'][accessor]['count'] // 3
    return {
        'nodes': len(doc.get('nodes', [])), 'meshes': len(doc.get('meshes', [])),
        'triangles': triangles, 'materials': len(doc.get('materials', [])),
        'images': len(doc.get('images', [])), 'extensionsUsed': doc.get('extensionsUsed', []),
        'animations': [{'name': a.get('name'), 'channels': len(a['channels'])} for a in doc.get('animations', [])],
        'components': [{'nodeIndex': i, 'name': n.get('name'), 'extras': n['extras']}
                       for i, n in enumerate(doc.get('nodes', [])) if n.get('extras', {}).get('assemblyComponent')],
    }


def extract(files):
    records, edges, symbols = [], [], []
    for path in files:
        rec = {'path': path, 'category': category(path), 'href': href(path)}
        generated = is_generated(path)
        if not generated:
            data = (ROOT / path).read_bytes()
            if Path(path).suffix not in BINARY:
                data = data.replace(b'\r\n', b'\n')
            rec.update(bytesCanonical=len(data), sha256=hashlib.sha256(data).hexdigest())
            if Path(path).suffix == '.glb':
                rec['glb'] = glb_info(path)
        if Path(path).suffix in {'.js', '.mjs', '.cjs', '.py'} and not generated:
            text = read(path)
            # Índice lexical, não resolução de chamadas ou tipos.
            pattern = r'(?:\b(?:async\s+)?function\s+|\bclass\s+|^\s*def\s+)([\w$]+)|\bexport\s+const\s+([\w$]+)'
            for m in re.finditer(pattern, text, re.M):
                name = m.group(1) or m.group(2)
                line = text.count('\n', 0, m.start()) + 1
                symbols.append({'name': name, 'path': path, 'line': line, 'href': href(path, line), 'extraction': 'declaração lexical'})
            if Path(path).suffix != '.py':
                pattern = r'''\bimport\s+(?:[^;\n]*?\sfrom\s*)?["']([^"']+)["']|\brequire\(\s*["']([^"']+)["']\s*\)'''
                for m in re.finditer(pattern, text):
                    spec = m.group(1) or m.group(2)
                    line = text.count('\n', 0, m.start()) + 1
                    target = (ROOT / path).parent / spec
                    target = target.resolve().relative_to(ROOT).as_posix() if spec.startswith('.') else 'external:' + spec
                    if not target.startswith('external:') and not (ROOT / target).is_file():
                        raise ValueError(f'Import não resolvido: {path}:{line} → {spec}')
                    edges.append({'source': path, 'target': target, 'relation': 'importa', 'confidence': 'EXTRACTED',
                                  'evidence': {'path': path, 'line': line, 'text': m.group(0)}, 'href': href(path, line)})
        records.append(rec)
    active = set()

    def visit(path):
        if path in active:
            return
        active.add(path)
        for e in edges:
            if e['source'] == path and not e['target'].startswith('external:'):
                visit(e['target'])
    visit('web/src/app-v2.js')
    for rec in records:
        if rec['path'].startswith('web/src/') and rec['path'].endswith(('.js', '.mjs')):
            rec['reachableFromApp'] = rec['path'] in active
    return records, edges, symbols


def production_edges():
    edges = []

    def add(source, target, relation, path, needle):
        edges.append({'source': source, 'target': target, 'relation': relation, 'confidence': 'EXTRACTED',
                      'evidence': {'path': path, 'line': line_of(path, needle), 'text': needle},
                      'href': href(path, line_of(path, needle))})
    add('web/src/app-v2.js', 'web/index.html', 'empacota', 'web/build.cjs', "entryPoints: [source('src', 'app-v2.js')]")
    for source, needle in [('web/src/template-v2.html', "source('src', 'template-v2.html')"), ('web/assets/carro-aula-v2.glb', "source('assets', 'carro-aula-v2.glb')")]:
        add(source, 'web/index.html', 'incorpora', 'web/build.cjs', needle)
    add('ferramentas/gerar_sistemas.py', 'web/assets/sistemas-v1.glb', 'gera', 'ferramentas/gerar_sistemas.py', "glb = (OUT if not wanted else PREVIEW_DIR) / f'sistemas-v1{suffix}.glb'")
    add('ferramentas/otimizar_sistemas.mjs', 'web/assets/sistemas-v1.glb', 'otimiza', 'ferramentas/otimizar_sistemas.mjs', 'fs.writeFileSync(file, output)')
    add('ferramentas/gerar_sistemas.py', 'web/assets/sistemas-v1.manifest.json', 'escreve manifesto', 'ferramentas/gerar_sistemas.py', "f'sistemas-v1{suffix}.manifest.json'")
    add('web/assets/sistemas-v1.glb', 'web/src/systems.js', 'carrega em runtime', 'web/src/systems.js', "export const SYSTEMS_ASSET='./assets/sistemas-v1.glb'")
    add('web/assets/carro-movable.glb', 'ferramentas/package_blender.py', 'entrada', 'ferramentas/package_blender.py', "ROOT+'/web/assets/carro-movable.glb'")
    for target in ['INTEIA_F1_Master.blend', 'modelos/INTEIA_F1_estatico.glb', 'modelos/INTEIA_F1_animado.glb', 'texturas/INTEIA_Carbono_BaseColor.png', 'Previa-Blender.png', 'validacao-criacao.json']:
        add('ferramentas/package_blender.py', target, 'gera / sobrescreve', 'ferramentas/package_blender.py', "'/" + target + "'")
    add('ferramentas/merge-animation.cjs', 'modelos/INTEIA_F1_animado.glb', 'reescreve clipe', 'ferramentas/merge-animation.cjs', 'fs.writeFileSync(file,out)')
    add('web/src/garage.js', 'ambientes/INTEIA-box-laboratorio.glb', 'download; cópia manual ao repo', 'web/src/app-v2.js', "garage.getExportScene()")
    for source in ['ambientes/INTEIA-box-laboratorio.glb', 'modelos/INTEIA_F1_estatico.glb']:
        add(source, 'ferramentas/package_garage.py', 'entrada', 'ferramentas/package_garage.py', "repo/'" + source + "'")
    for target in ['ambientes/INTEIA_Box_com_carro.blend', 'ambientes/validacao-box.json']:
        add('ferramentas/package_garage.py', target, 'gera / sobrescreve', 'ferramentas/package_garage.py', "repo/'" + target + "'")
    add('ambientes/INTEIA_Box_com_carro.blend', 'ferramentas/render_garage_preview.py', 'entrada', 'ferramentas/render_garage_preview.py', "repo/'ambientes/INTEIA_Box_com_carro.blend'")
    add('ferramentas/render_garage_preview.py', 'ambientes/Previa-Box.png', 'renderiza', 'ferramentas/render_garage_preview.py', "repo/'ambientes/Previa-Box.png'")
    for source in ['INTEIA_F1_Master.blend', 'modelos/INTEIA_F1_estatico.glb', 'modelos/INTEIA_F1_animado.glb']:
        add(source, 'ferramentas/validate-kit.py', 'reabre / verifica', 'ferramentas/validate-kit.py', Path(source).name)
    add('ferramentas/validate-kit.py', 'validacao-reabertura.json', 'escreve evidência', 'ferramentas/validate-kit.py', "'/validacao-reabertura.json'")
    add('web/test-mechanics.mjs', 'validacao-mecanica-web.json', 'escreve evidência', 'web/test-mechanics.mjs', "'../validacao-mecanica-web.json'")
    for source in [r['arquivo'] for r in json.loads(read('manifesto-sha256.json'))]:
        add(source, 'ferramentas/manifest.cjs', 'mede hash', 'ferramentas/manifest.cjs', "'" + source + "'")
    add('ferramentas/manifest.cjs', 'manifesto-sha256.json', 'escreve hashes', 'ferramentas/manifest.cjs', "'manifesto-sha256.json'")
    return edges


def controls(files):
    path = 'web/src/template-v2.html'
    text = read(path)
    rows = []
    for m in re.finditer(r'<([a-z]+)\b[^>]*\bid="([^"]+)"[^>]*>', text):
        tag, id_ = m.group(1, 2)
        refs = []
        for source in files:
            if not source.startswith('web/src/') or not source.endswith(('.js', '.mjs')):
                continue
            for hit in re.finditer(r'''["']#?''' + re.escape(id_) + r'''["']''', read(source)):
                line = read(source).count('\n', 0, hit.start()) + 1
                if not any(r['path'] == source and r['line'] == line for r in refs):
                    refs.append({'path': source, 'line': line, 'href': href(source, line)})
        rows.append({'id': id_, 'tag': tag, 'line': text.count('\n', 0, m.start()) + 1,
                     'href': href(path, text.count('\n', 0, m.start()) + 1), 'literalReferences': refs})
    return rows


def mermaid(edges):
    paths = sorted({e[k] for e in edges for k in ['source', 'target']})
    ids = {p: 'n' + str(i) for i, p in enumerate(paths)}
    rows = ['```mermaid', 'flowchart LR']
    for p in paths:
        rows.append(f'  {ids[p]}["{p.removeprefix("web/src/")}"]')
    for e in edges:
        rows.append(f'  {ids[e["source"]]} -->|"{e["relation"]}"| {ids[e["target"]]}')
    rows.append('```')
    return '\n'.join(rows)


def check_links(path, text, virtual):
    errors, count = [], 0
    # Links Markdown; URLs externas são inventariadas, não requisitadas.
    for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', text):
        target = m.group(1).strip('<>')
        if re.match(r'^[a-z]+:', target) or target.startswith('#'):
            continue
        name, _, anchor = target.partition('#')
        dest = ((ROOT / path).parent / unquote(name)).resolve()
        try:
            rel = dest.relative_to(ROOT).as_posix()
        except ValueError:
            errors.append(f'{path}: link fora do repo: {target}')
            continue
        count += 1
        if rel not in virtual and not dest.exists():
            errors.append(f'{path}: destino ausente: {target}')
        elif anchor and dest.is_file():
            content = virtual.get(rel) if rel in virtual else dest.read_text(encoding='utf-8-sig')
            if re.fullmatch(r'L\d+', anchor):
                if int(anchor[1:]) > len(content.splitlines()):
                    errors.append(f'{path}: linha inexistente: {target}')
            elif dest.suffix == '.md':
                headings = [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-')
                            for h in re.findall(r'^#+\s+(.+)$', content, re.M)]
                explicit = re.findall(r'<a\s+(?:id|name)=[\"\x27]([^\"\x27]+)[\"\x27]', content)
                if unquote(anchor) not in headings + explicit:
                    errors.append(f'{path}: âncora inexistente: {target}')
    return errors, count


def make():
    files = file_list()
    records, imports, symbols = extract(files)
    pipeline = production_edges()
    dom = controls(files)
    base = next(r['glb'] for r in records if r['path'] == 'web/assets/carro-aula-v2.glb')
    origin = json.loads(read('documentacao/componentes-origem.json'))['parts']
    actual = {r['extras']['partId']: r for r in base['components']}
    assert len(actual) == len(base['components']), 'partId duplicado no GLB'
    assert {r['partId'] for r in origin} == set(actual), 'Procedência diverge do GLB'
    parts = [{'partId': r['partId'], 'label': r['label'], 'category': r['category'],
              'sourceObject': r['sourceObject'], 'trianglesRecorded': r['triangles'],
              'originPointer': '/parts/' + str(i), 'nodePointer': '/nodes/' + str(actual[r['partId']]['nodeIndex']),
              'originHref': href('documentacao/componentes-origem.json', line_of('documentacao/componentes-origem.json', '"partId": "' + r['partId'] + '"'))}
             for i, r in enumerate(origin)]
    fingerprint = hashlib.sha256('\n'.join(r['path'] + ':' + r.get('sha256', '') for r in records).encode()).hexdigest()
    data = {'schemaVersion': 1, 'fingerprint': fingerprint,
            'scope': 'arquivos Git e novos não ignorados; caches, dependências instaladas e backups ignorados excluídos',
            'hashPolicy': 'SHA256 e bytes de texto com LF; binários exatos; mapas gerados sem auto-hash',
            'files': records, 'symbols': symbols}
    graph = {'schemaVersion': 1, 'imports': imports, 'production': pipeline,
             'limits': 'imports literais JS/CJS; declarações lexicais; produção curada com evidência. Não é call graph completo.'}
    result = {}

    def put(name, value):
        result['docs/mapas/' + name] = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'

    put('inventario.json', data)
    put('dependencias.json', graph)
    put('controles.json', {'limits': 'IDs do HTML e referências literais; IDs concatenados, delegação e CSS exigem revisão humana.', 'controls': dom})
    put('componentes.json', {'source': 'documentacao/componentes-origem.json', 'comparedTo': 'web/assets/carro-aula-v2.glb', 'parts': parts})
    rows = ['# Inventário completo', '', '[Índice dos mapas](README.md) · [Busca interativa](index.html)', '',
            'Gerado por `python ferramentas/mapear.py`. Todos os arquivos do escopo estão listados, inclusive entregas e documentos. Binários Blender são inventariados por hash; não são interpretados.', '',
            '| Arquivo | Papel | Tamanho canônico |', '| --- | --- | --- |']
    for r in records:
        rows.append(f'| [{r["path"]}]({r["href"]}) | {r["category"]} | {r.get("bytesCanonical", "—")} |')
    rows += ['', '## Símbolos declarados', '', 'Índice lexical de funções, classes e constantes exportadas. Não resolve callbacks anônimos nem chamadas dinâmicas.', '', '| Símbolo | Origem |', '| --- | --- |']
    for s in symbols:
        rows.append(f'| `{s["name"]}` | [{s["path"]}:{s["line"]}]({s["href"]}) |')
    put('INVENTARIO.md', '\n'.join(rows) + '\n')
    local = [e for e in imports if e['source'].startswith('web/src/') and not e['target'].startswith('external:')]
    rows = ['# Grafos verificáveis', '', '[Índice](README.md) · [Explorar no navegador](index.html) · [Dados e evidências](dependencias.json)', '',
            'Setas de dependência vão do importador ao módulo importado. Setas de produção vão da entrada à ferramenta ou entrega. Cada aresta abaixo tem evidência; a análise semântica complementar está em [graphify](../../graphify-out/GRAPH_REPORT.md).', '',
            '## Arquitetura dos módulos web', '', mermaid(local), '',
            ('`branding.js` integra a árvore de imports de `app-v2.js`.' if any(r['path'] == 'web/src/branding.js' and r.get('reachableFromApp') for r in records)
             else '`branding.js` está fora da árvore de imports de `app-v2.js`.') + ' Dependências externas constam nos dados e na busca.', '',
            '## Produção do carro', '', mermaid([e for e in pipeline if ('package_blender' in e['source'] or 'package_blender' in e['target'] or 'merge-animation' in e['source'] or e['target'] == 'web/index.html')]), '',
            '## Produção do box', '', mermaid([e for e in pipeline if any(x in e['source'] + e['target'] for x in ['package_garage', 'render_garage', 'web/src/garage.js'])]), '',
            'O download do box é uma etapa humana: o grafo descreve o produtor, sem certificar que o GLB salvo foi exportado do código atual. O original `F1_2026_tutorial_part7_textures.blend` e a etapa inicial de separação não estão disponíveis no repositório.', '',
            '## Evidências das relações', '', '| Origem | Relação | Destino | Evidência |', '| --- | --- | --- | --- |']
    for e in imports + pipeline:
        ev = e['evidence']
        rows.append(f'| `{e["source"]}` | {e["relation"]} | `{e["target"]}` | [{ev["path"]}:{ev["line"]}]({e["href"]}) |')
    put('GRAFOS.md', '\n'.join(rows) + '\n')
    template = read('ferramentas/mapa-template.html')
    payload = json.dumps({'inventory': data, 'graph': graph, 'controls': dom, 'parts': parts}, ensure_ascii=False).replace('<', '\\u003c')
    put('index.html', template.replace('__MAP_DATA__', payload))
    errors, links = [], 0
    for path in files:
        if path.endswith('.md') and not path.startswith('graphify-out/'):
            errs, n = check_links(path, result.get(path, '') if path in GENERATED else read(path),
                                  {**{p: '' for p in GENERATED}, **result})
            errors.extend(errs)
            links += n
    assert not errors, '\n'.join(errors)
    coverage = {'files': len(records), 'categories': dict(sorted(Counter(r['category'] for r in records).items())),
                'declaredSymbols': len(symbols), 'literalImports': len(imports), 'productionEdges': len(pipeline),
                'templateIds': len(dom), 'componentsMatchedByPartId': len(parts), 'localMarkdownLinksChecked': links,
                'brokenLocalLinks': 0, 'fingerprint': fingerprint,
                'limits': ['Não abre Blender nem refaz exports.', 'Não verifica URLs externas.',
                           'IDs DOM dinâmicos e callbacks não são resolvidos.',
                           'Graphify é snapshot separado; este check não reextrai sua semântica.',
                           'Cobertura de arquivos não significa cobertura de testes ou de todas as relações.']}
    put('cobertura.json', coverage)
    return result, coverage


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--check', action='store_true')
    options = args.parse_args()
    outputs, coverage = make()
    stale = []
    for path, content in outputs.items():
        dest = ROOT / path
        if options.check:
            if not dest.exists() or dest.read_text(encoding='utf-8') != content:
                stale.append(path)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding='utf-8', newline='\n')
    if stale:
        raise SystemExit('Mapas desatualizados: ' + ', '.join(stale) + '\nExecute python ferramentas/mapear.py')
    print(json.dumps(coverage, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
