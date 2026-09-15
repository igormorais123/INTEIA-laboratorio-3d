"""Gera catálogo/grafos sem alterar aplicativo, dependências ou mapeamento paralelo.
Executar na raiz do repositório: python docs/mapeamento-detalhado/scripts/gerar.py
Tree-sitter JS é opcional; sem ele, preserva-se a coleta de símbolos anterior
somente quando os hashes de TODAS as fontes desse índice conferem.
"""
from pathlib import Path
import ast, collections, csv, datetime, hashlib, html, json, os, re, struct, subprocess
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/mapeamento-detalhado'
assert ROOT.name == 'INTEIA-laboratorio-3d', 'Escopo inesperado'
PREFIX = 'docs/mapeamento-detalhado/'
EXCLUDES = {'.git': 'Metadados e objetos internos Git; revisão registrada via Git',
            'node_modules': 'Dependências instaladas; versões em package-lock.json',
            '__pycache__': 'Cache Python regenerável',
            'graphify-out': 'Extração/cache da conversa paralela ou cache isolado desta análise'}

def write(name, data):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def link(path): return '../../'+quote(path, safe='/')

def inventory():
    found=[]; skipped=[]
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        parent=Path(base)
        for name in list(dirs):
            p=parent/name; rel=p.relative_to(ROOT).as_posix()
            reason=EXCLUDES.get(name)
            if (p/'.git').exists(): reason='Checkout/worktree Git aninhado: cópia operacional do mesmo projeto, não é fonte adicional'
            if rel == PREFIX.rstrip('/'): reason='Esta entrega: inventário próprio em dados/entrega.json; evita autorreferência recursiva'
            if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()): reason='Link/junção não seguido para preservar escopo'
            if reason:
                skipped.append({'path':rel, 'reason':reason}); dirs.remove(name)
        for name in files:
            p=parent/name; rel=p.relative_to(ROOT).as_posix()
            if p.is_symlink(): skipped.append({'path':rel,'reason':'Link não seguido'}); continue
            if re.search(r'(^\.env($|\.)|\.log$|\.blend[12]$|\.zip$)',name):
                skipped.append({'path':rel,'reason':'Ambiente local, log, backup ou pacote duplicado; conteúdo não lido'}); continue
            found.append(rel)
    return sorted(found),skipped

def glb_info(path):
    with path.open('rb') as f:
        header=f.read(20); magic,version,total,n,kind=struct.unpack('<4sIIII',header)
        assert magic==b'glTF' and version==2 and kind==0x4e4f534a and total==path.stat().st_size
        g=json.loads(f.read(n))
        binary=None
        if g.get('animations'):
            nbin,kbin=struct.unpack('<II',f.read(8)); binary=f.read(nbin)
    primitives=[p for m in g.get('meshes',[]) for p in m.get('primitives',[])]
    triangle_count=sum(g['accessors'][p.get('indices',p.get('attributes',{}).get('POSITION'))]['count']//3 for p in primitives if p.get('mode',4)==4)
    clips=[]
    for a in g.get('animations',[]):
        times=[]
        for s in a['samplers']:
            acc=g['accessors'][s['input']]; bv=g['bufferViews'][acc['bufferView']]
            if 'EXT_meshopt_compression' in bv.get('extensions',{}):
                # Compressed offsets address decoded data, not the binary chunk.
                times.extend(acc.get('min',[])+acc.get('max',[]))
            elif binary is not None and acc['componentType']==5126:
                offset=bv.get('byteOffset',0)+acc.get('byteOffset',0)
                stride=bv.get('byteStride',4)
                times.extend(struct.unpack_from('<f',binary,offset+i*stride)[0] for i in range(acc['count']))
        clips.append({'name':a.get('name'),'channels':len(a['channels']),'samplers':len(a['samplers']),'time_min':min(times) if times else None,'time_max':max(times) if times else None,'paths':dict(collections.Counter(c['target']['path'] for c in a['channels']))})
    return {'asset':g.get('asset'),'nodes':len(g.get('nodes',[])),'meshes':len(g.get('meshes',[])),'primitives':len(primitives),'triangles':triangle_count,'triangle_note':'Contagem de primitivas TRIANGLES por indices ou POSITION; não equivale a fidelidade topológica ou física','materials':len(g.get('materials',[])),'images':len(g.get('images',[])),'external_uris':[x['uri'] for k in ('images','buffers') for x in g.get(k,[]) if 'uri' in x and not x['uri'].startswith('data:')],'animations':clips,'extensions_used':g.get('extensionsUsed',[]),'material_names':[m.get('name') for m in g.get('materials',[])],'parts':[{'name':n.get('name'),'extras':n['extras']} for n in g.get('nodes',[]) if n.get('extras',{}).get('assemblyComponent')]}

def gather_symbols(paths):
    code=[p for p in paths if Path(p).suffix in ('.js','.mjs','.cjs','.py') and not p.startswith('docs/') and p!='ferramentas/mapear.py']
    hashes={p:sha(ROOT/p) for p in code}
    try:
        import tree_sitter, tree_sitter_javascript
        parser=tree_sitter.Parser(tree_sitter.Language(tree_sitter_javascript.language()))
    except ImportError:
        old=OUT/'dados/simbolos.json'
        if old.exists():
            data=json.loads(old.read_text(encoding='utf-8'))
            if data['source_hashes']==hashes:return data
        raise SystemExit('Fontes mudaram ou índice inexistente. Use Python com tree-sitter/tree-sitter-javascript (ver ATUALIZAR.md).')
    symbols=[]; calls=[]; errors=[]
    for path in code:
        b=(ROOT/path).read_bytes()
        if path.endswith('.py'):
            tree=ast.parse(b, filename=path)
            def walk_py(n, scope='module'):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    sid=path+'#'+str(n.lineno)+':'+n.name
                    symbols.append({'id':sid,'path':path,'name':n.name,'kind':type(n).__name__,'line':n.lineno,'end_line':n.end_lineno,'scope':scope,'signature':b.decode('utf-8').splitlines()[n.lineno-1].strip()})
                    scope=sid
                for child in ast.iter_child_nodes(n):walk_py(child,scope)
            walk_py(tree);continue
        tree=parser.parse(b)
        if tree.root_node.has_error: errors.append(path)
        def txt(n):return b[n.start_byte:n.end_byte].decode('utf-8') if n else ''
        def walk(n,scope='module'):
            name=None; value=None
            if n.type in ('function_declaration','generator_function_declaration','method_definition'):
                name=txt(n.child_by_field_name('name'));value=n
            elif n.type=='variable_declarator':
                value=n.child_by_field_name('value')
                if value and value.type in ('arrow_function','function_expression'): name=txt(n.child_by_field_name('name'))
            elif n.type=='pair':
                value=n.child_by_field_name('value')
                if value and value.type in ('arrow_function','function_expression'):name=txt(n.child_by_field_name('key'))
            if name:
                sid=path+'#'+str(n.start_point.row+1)+':'+name
                symbols.append({'id':sid,'path':path,'name':name,'kind':n.type,'line':n.start_point.row+1,'end_line':n.end_point.row+1,'scope':scope,'signature':(name+txt(value.child_by_field_name('parameters')))[:220]})
                scope=sid
            if n.type=='call_expression':
                f=n.child_by_field_name('function')
                if f and f.type=='identifier':calls.append({'path':path,'source':scope,'callee':txt(f),'line':n.start_point.row+1,'expression':txt(n)[:180]})
            for child in n.named_children:walk(child,scope)
        walk(tree.root_node)
    return {'method':'tree-sitter-javascript: declarações nomeadas, arrow functions atribuídas e métodos; Python ast: funções/classes. Callbacks anônimos e resolução dinâmica não são indexados integralmente.','source_hashes':hashes,'parse_errors':errors,'symbols':symbols,'direct_calls':calls}

def main():
    paths,skipped=inventory();tracked=set(git('ls-files').splitlines())
    purpose=json.loads((OUT/'scripts/finalidades.json').read_text(encoding='utf-8'))
    rows=[]; nodes=[]; edges=[]; ids=set(); imports=[]; refs_unresolved=[]
    def node(i,label,kind,path=None):
        if i not in ids:nodes.append({'id':i,'label':label,'kind':kind,'path':path});ids.add(i)
    def edge(source,target,relation,path,line,text='',confidence='EXTRACTED',score=1):
        edges.append({'source':source,'target':target,'relation':relation,'confidence':confidence,'confidence_score':score,'evidence':{'path':path,'line':line,'text':text}})
    for p in paths:node(p,p,'file',p)
    for p in paths:
        full=ROOT/p; ext=full.suffix.lower(); meta=purpose.get(p)
        parallel=p.startswith('docs/mapeamento/') or p.startswith('docs/mapa') or p in ('ferramentas/mapear.py','ferramentas/mapa-template.html')
        if meta is None:
            if parallel:meta=['Mapeamento produzido pela conversa paralela; catalogado como artefato complementar','documentação/código de mapeamento paralelo','Consultar entrada da outra documentação; não editado nesta tarefa']
            else:meta=['Arquivo adicional: finalidade ainda requer revisão humana','não classificado','Revisar scripts/finalidades.json antes de reutilizar']
        row={'path':p,'type':ext.lstrip('.') or 'sem extensão','purpose':meta[0],'nature':meta[1],'usage':meta[2],'classification_reviewed':p in purpose or parallel,'tracked':p in tracked,'bytes':full.stat().st_size,'sha256':sha(full),'dependencies':[],'used_by':[]}
        if ext=='.png':
            b=full.read_bytes()
            if b.startswith(b'\x89PNG\r\n\x1a\n'):
                row['image_size']=list(struct.unpack('>II',b[16:24]));row['actual_format']='PNG'
            elif b.startswith(b'\xff\xd8'):
                row['actual_format']='JPEG (extensão .png divergente)';offset=2
                while offset<len(b):
                    if b[offset]!=255:offset+=1;continue
                    while b[offset]==255:offset+=1
                    marker=b[offset];offset+=1
                    if marker in (0xd8,0xd9):continue
                    size=struct.unpack_from('>H',b,offset)[0]
                    if marker in (0xc0,0xc1,0xc2,0xc3):
                        height,width=struct.unpack_from('>HH',b,offset+3);row['image_size']=[width,height];break
                    offset+=size
            else:row['actual_format']='Assinatura não identificada'
        if ext=='.glb':row['glb']=glb_info(full)
        if ext in ('.js','.mjs','.cjs','.py','.md','.json','.yml','.svg','.txt') or p in ('LICENSE','.gitattributes','.gitignore'):
            row['lines']=len(full.read_text(encoding='utf-8-sig').splitlines())
        rows.append(row)
        if ext in ('.js','.mjs','.cjs') and not parallel:
            text=full.read_text(encoding='utf-8')
            pat=r"\bimport\s+(?:[^;\n]*?\s+from\s*)?['\"]([^'\"]+)['\"]|\brequire\(\s*['\"]([^'\"]+)['\"]\s*\)"
            for m in re.finditer(pat,text):
                spec=m.group(1) or m.group(2); line=text.count('\n',0,m.start())+1
                if spec.startswith('.'):
                    resolved=(full.parent/spec).resolve(); target=resolved.relative_to(ROOT).as_posix()
                    if target not in paths:refs_unresolved.append({'path':p,'line':line,'specifier':spec});continue
                else:
                    target='external:'+spec;node(target,spec,'external')
                edge(p,target,'importa',p,line,m.group());imports.append({'source':p,'target':target,'line':line,'specifier':spec,'statement':m.group()})
        if ext=='.md' and not parallel:
            text=full.read_text(encoding='utf-8'); text=re.sub(r'```[\s\S]*?```','',text)
            for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
                url=m.group(1).strip('<>');parsed=urlparse(url)
                if parsed.scheme or not parsed.path:continue
                dest=(full.parent/unquote(parsed.path)).resolve()
                if dest.is_relative_to(ROOT) and dest.is_file():
                    target=dest.relative_to(ROOT).as_posix()
                    if target in paths:edge(p,target,'documenta',p,None,url)
    bypath={r['path']:r for r in rows}
    symbols=gather_symbols(paths);write('dados/simbolos.json',symbols)
    for s in symbols['symbols']:
        node(s['id'],s['name'],'symbol',s['path']);edge(s['path'],s['id'],'define',s['path'],s['line'],s['signature'])
    # Resolução conservadora: só nomes unívocos no mesmo arquivo ou imports nomeados unívocos.
    for call in symbols['direct_calls']:
        matches=[s for s in symbols['symbols'] if s['path']==call['path'] and s['name']==call['callee']]
        if not matches:
            for imp in imports:
                if imp['source']!=call['path'] or imp['target'].startswith('external:'):continue
                m=re.search(r'\{([^}]+)\}',imp['statement'])
                if not m:continue
                for binding in m.group(1).split(','):
                    parts=re.split(r'\s+as\s+',binding.strip())
                    if parts[-1]==call['callee']:matches.extend(s for s in symbols['symbols'] if s['path']==imp['target'] and s['name']==parts[0] and s['scope']=='module')
        if len(matches)==1:
            source=call['source'] if call['source']!='module' else call['path']
            edge(source,matches[0]['id'],'chama_sintaticamente',call['path'],call['line'],call['expression'])
    curated=OUT/'dados/relacoes-curadas.json'
    if curated.exists():
        data=json.loads(curated.read_text(encoding='utf-8'))
        for e in data if isinstance(data,list) else data.get('edges',data.get('relations',[])):
            assert e['source'] in ids and e['target'] in ids, e
            edges.append(e)
    output_relations={'gera_ou_sobrescreve','sobrescreve_html_gerado','escreve_relatorio','escreve_relatorio_de_teste','salva_blend_conjunto','renderiza_previa','sobrescreve_manifesto_de_artefatos','le_e_reescreve_com_clipe_unico'}
    for e in edges:
        if e['source'] in bypath:
            row=bypath[e['source']];ref={'target':e['target'],'relation':e['relation'],'line':e.get('evidence',{}).get('line')}
            row.setdefault('relations_out',[]).append(ref)
            if e['relation'] in output_relations:row.setdefault('outputs',[]).append(ref)
            if (e['target'] in bypath or e['target'].startswith('external:')) and not e['relation'].startswith(('documenta','declara_licenca','identifica_licenca','registra_fonte')) and (e['relation'] not in output_relations or e['relation']=='le_e_reescreve_com_clipe_unico'):row['dependencies'].append(ref)
        if e['target'] in bypath:bypath[e['target']]['used_by'].append({'source':e['source'],'relation':e['relation']})
    parts=json.loads((ROOT/'documentacao/componentes-origem.json').read_text(encoding='utf-8'))
    web_parts=bypath['web/assets/carro-aula-v2.glb']['glb']['parts']
    provenance_check=all(any(w['name']==p['name'] and w['extras']=={k:v for k,v in p.items() if k!='name'} for w in web_parts) for p in parts['parts'])
    # Extras podem incluir o campo name: compare campos presentes no documento sem inferir autoria.
    if not provenance_check:
        provenance_check=all(any(w['name']==p['name'] and all(w['extras'].get(k)==v for k,v in p.items() if k!='name') for w in web_parts) for p in parts['parts'])
    write('dados/componentes.json',{'source':'documentacao/componentes-origem.json','web_glb':'web/assets/carro-aula-v2.glb','documented_parts':len(parts['parts']),'glb_parts':len(web_parts),'all_documented_fields_match_glb':provenance_check,**parts})
    manifest=[]
    for m in json.loads((ROOT/'manifesto-sha256.json').read_text(encoding='utf-8')):
        actual=bypath.get(m['arquivo']);manifest.append({**m,'matches':bool(actual and actual['sha256']==m['sha256'] and actual['bytes']==m['bytes'])})
    write('dados/manifesto-conferencia.json',manifest)
    base=json.loads((OUT/'dados/estado-inicial.json').read_text(encoding='utf-8'))
    meta={'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revision':git('rev-parse','HEAD'),'initial_revision':base['revision'],'branch':git('branch','--show-current'),'status':git('status','--porcelain=v1'),'catalog_count':len(rows),'bytes':sum(r['bytes'] for r in rows),'baseline_files':len(base['tracked']),'baseline_missing':sorted(set(base['tracked'])-set(paths)),'unclassified':[r['path'] for r in rows if not r['classification_reviewed']],'excluded':skipped,'scope':'Somente '+str(ROOT),'own_delivery':'dados/entrega.json','parallel_thread':base['parallel_thread'],'symbols':len(symbols['symbols']),'symbol_parse_errors':symbols['parse_errors'],'unresolved_local_imports':refs_unresolved,'edges':len(edges),'nodes':len(nodes),'confidence_counts':dict(collections.Counter(e['confidence'] for e in edges))}
    write('dados/cobertura.json',meta);write('dados/catalogo.json',{'metadata':meta,'files':rows});write('dados/grafo.json',{'metadata':meta,'directed':True,'multigraph':True,'nodes':nodes,'edges':edges,'note':'Uma relação EXTRACTED confirma referência/declaracao no fonte, não execução de todos os ramos. Chamadas dinâmicas podem estar ausentes.'})
    with (OUT/'dados/catalogo.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['caminho','tipo','natureza','finalidade','uso','bytes','sha256','dependencias','saidas','usado_por'])
        for r in rows:w.writerow([r['path'],r['type'],r['nature'],r['purpose'],r['usage'],r['bytes'],r['sha256'],'; '.join(d['target'] for d in r['dependencies']),'; '.join(d['target'] for d in r.get('outputs',[])),'; '.join(d['source'] for d in r['used_by'])])
    cat=['# Catálogo completo de arquivos','', '[Índice](README.md) · [Busca interativa](index.html) · [CSV](dados/catalogo.csv) · [JSON](dados/catalogo.json)','',f"{len(rows)} arquivos catalogados. Hashes de bytes locais em dados/catalogo.json; fontes e derivados têm naturezas distintas. Dependências externas são identificadas como external: e não inventariadas como código do projeto.",'']
    for r in rows:
        cat.extend([f"## {r['path']}",'',f"[Abrir arquivo]({link(r['path'])}) · {r['type']} · {r['bytes']:,} bytes",'',r['purpose']+'.', '',f"**Natureza:** {r['nature']}. **Uso:** {r['usage']}."])
        deps=[d for d in r.get('relations_out',[]) if d['relation']!='define']
        cat.append('**Relações de saída:** '+('; '.join(f"{d['relation']} → `{d['target']}`" for d in deps) or 'Nenhuma relação estrutural encontrada; ausência não prova desuso.')+'.')
        cat.append('**Referenciado por:** '+('; '.join('`'+d['source']+'` ('+d['relation']+')' for d in r['used_by']) or 'Nenhuma referência catalogada.')+'.')
        if r.get('glb'):cat.append(f"**GLB:** {r['glb']['nodes']} nós, {r['glb']['meshes']} meshes, {r['glb']['triangles']:,} triângulos, {r['glb']['materials']} materiais, {r['glb']['images']} imagens, {len(r['glb']['animations'])} clipes.")
        cat.append('')
    write('CATALOGO.md','\n'.join(cat))
    folders={'.':'Entradas, direitos, projeto Blender mestre e evidências históricas','.github':'Automação de verificação remota','.github/workflows':'CI de build/test','web':'Aplicação autocontida e ferramentas Node','web/src':'Fontes editáveis da cena e interface','web/assets':'Base GLB operacional e wordmark avulso','ferramentas':'Conversão, embalagem, validação e manifesto','docs':'Guias técnicos e documentação','documentacao':'Metadados de peças e histórico visual','identidade':'SVGs e guia de identidade','modelos':'GLBs convertidos para distribuição','texturas':'Texturas portáveis de entrega','ambientes':'Box GLB e cena Blender com carro'}
    tree=['# Árvore comentada','', '[Índice](README.md) · [Catálogo](CATALOGO.md)','', 'Diretórios de dependências, caches e Git são listados nas exclusões; não são expandidos. Esta documentação tem inventário próprio para evitar autorreferência.','', '```text','INTEIA-laboratorio-3d/']
    seen=set()
    for r in rows:
        pp=Path(r['path']); current=''
        for depth,part in enumerate(pp.parts[:-1]):
            current=part if not current else current+'/'+part
            if current not in seen:
                tree.append('  '*(depth+1)+part+'/  # '+folders.get(current,'Documentação complementar da conversa paralela'));seen.add(current)
        tree.append('  '*len(pp.parts)+pp.name+'  # '+r['purpose'])
    tree.extend(['  docs/mapeamento-detalhado/  # Esta entrega: índice, HTML, catálogos, grafos e scripts','```','', '## Exclusões observadas',''])
    tree.extend('- `'+s['path']+'`: '+s['reason']+'.' for s in skipped);write('ARVORE.md','\n'.join(tree)+'\n')
    fun=['# Índice de funções e métodos','', '[Índice](README.md) · [Busca interativa](index.html) · [JSON](dados/simbolos.json)','',symbols['method'],'','Chamadas são referências sintáticas conservadoras, não rastreamento de execução. Funções anônimas e métodos dinâmicos exigem a leitura dos módulos.','']
    for p in code_paths(symbols):
        fun.extend(['## '+p,'',f'[Fonte]({link(p)})','', '| Nome | Linha | Escopo | Assinatura |','|---|---:|---|---|'])
        for s in symbols['symbols']:
            if s['path']==p:fun.append('| '+s['name']+' | '+str(s['line'])+' | '+s['scope'].split('#')[-1]+' | `'+s['signature'].replace('|','\\|')+'` |')
        fun.append('')
    write('FUNCOES.md','\n'.join(fun))
    # Grafos sem dependência externa; mesmo conjunto de arestas em Mermaid e JSON.
    for name,select in [('arquitetura',lambda e:e['relation']=='importa' and e['source'].startswith('web/')),('assets',lambda e:e['source'].startswith('ferramentas/') or any(x in str(e['target']) for x in ('.glb','.blend','.png','manifesto'))),('dados',lambda e:e['relation'] not in ('importa','define','documenta','chama_sintaticamente'))]:
        selected=[e for e in edges if select(e) and e['source'] in bypath and e['target'] in ids]
        selected_ids=set(v for e in selected for v in (e['source'],e['target']));subnodes=[n for n in nodes if n['id'] in selected_ids]
        write('grafos/'+name+'.json',{'nodes':subnodes,'edges':selected,'directed':True,'multigraph':True})
        ix={n['id']:'n'+str(i) for i,n in enumerate(subnodes)}
        lines=['flowchart LR']+[f'  {ix[n["id"]]}["{n["label"].replace(chr(34),chr(39))}"]' for n in subnodes]
        for e in selected:lines.append(f'  {ix[e["source"]]} -->|"{e["relation"]} · {e["confidence"]}"| {ix[e["target"]]}')
        write('grafos/'+name+'.mmd','\n'.join(lines)+'\n')
    template=(OUT/'scripts/interface.html').read_text(encoding='utf-8')
    payload={'meta':meta,'files':rows,'nodes':nodes,'edges':edges,'symbols':symbols['symbols'],'parts':parts['parts']}
    write('index.html',template.replace('/*__DATA__*/',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')))
    print(json.dumps({k:meta[k] for k in ('catalog_count','baseline_files','unclassified','symbols','nodes','edges','unresolved_local_imports')},ensure_ascii=False))

def code_paths(symbols):return sorted(set(s['path'] for s in symbols['symbols']))

if __name__=='__main__':main()
