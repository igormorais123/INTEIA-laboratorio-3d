"""Valida a entrega sem executar app nem escrever fora deste diretório."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import collections,datetime,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/mapeamento-detalhado'
def read(p):return p.read_text(encoding='utf-8-sig')
def hashfile(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def load(name):return json.loads(read(OUT/name))
def slug(s):
    s=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',s)
    s=re.sub(r'<[^>]*>','',s).replace('`','').replace('*','').lower()
    return re.sub(r'[^\w\- ]','',s).replace(' ','-')
def anchors(p):
    t=re.sub(r'```[\s\S]*?```','',read(p));seen=collections.Counter();a=set(re.findall(r'<a\s+(?:id|name)="([^"]+)"',t))
    for m in re.finditer(r'^#{1,6}\s+(.+?)\s*#*$',t,re.M):
        s=slug(m.group(1));a.add(s+('-'+str(seen[s]) if seen[s] else ''));seen[s]+=1
    return a
errors=[];warnings=[];links=0
for p in OUT.rglob('*.md'):
    if 'graphify-out' in p.parts:continue
    text=re.sub(r'```[\s\S]*?```','',read(p))
    for m in re.finditer(r'!?\[[^]]*\]\(([^)]+)\)',text):
        u=m.group(1).strip('<>');v=urlparse(u)
        if v.scheme or u.startswith('//'):continue
        target=(p.parent/unquote(v.path)).resolve() if v.path else p
        links+=1
        if not target.is_relative_to(ROOT) or not target.exists():errors.append(f'Link ausente/fora do escopo: {p.relative_to(OUT)} -> {u}');continue
        frag=unquote(v.fragment)
        if frag and not re.fullmatch(r'L\d+(?:-L\d+)?',frag) and target.suffix=='.md' and frag not in anchors(target):errors.append(f'Âncora ausente: {p.relative_to(OUT)} -> {u}')
for u in re.findall(r'(?:href|src)="([^"]+)"',read(OUT/'index.html').split('<script id="atlas-data"')[0]):
    if u.startswith('#') or urlparse(u).scheme:continue
    links+=1
    if not (OUT/unquote(u)).exists():errors.append('Link HTML ausente: '+u)
cat=load('dados/catalogo.json');g=load('dados/grafo.json');syms=load('dados/simbolos.json');ids=[n['id'] for n in g['nodes']]
if len(ids)!=len(set(ids)):errors.append('IDs de nós duplicados')
ids=set(ids)
for e in g['edges']:
    if e['source'] not in ids or e['target'] not in ids:errors.append('Extremidade ausente: '+str(e))
    if e['confidence'] not in ('EXTRACTED','INFERRED','AMBIGUOUS'):errors.append('Confiança inválida')
    if e['confidence']=='EXTRACTED' and e.get('confidence_score')!=1:errors.append('Confiança EXTRACTED sem score 1')
    ev=e.get('evidence',{});p=ROOT/ev.get('path','')
    if not p.is_file():errors.append('Fonte de relação ausente: '+str(ev))
    elif ev.get('line') and not 0<ev['line']<=len(read(p).splitlines()):errors.append('Linha de evidência inexistente: '+str(ev))
stale=[]
for f in cat['files']:
    p=ROOT/f['path']
    if not p.is_file() or hashfile(p)!=f['sha256']:stale.append(f['path'])
if stale:errors.append('Snapshot desatualizado: '+', '.join(stale))
if cat['metadata']['baseline_missing']:errors.append('Arquivos do inventário inicial ausentes')
if cat['metadata']['unclassified']:errors.append('Arquivos sem finalidade revisada')
if syms['parse_errors']:errors.append('Erros de parse de símbolos')
if cat['metadata']['unresolved_local_imports']:errors.append('Imports locais não resolvidos')
for e in load('dados/relacoes-curadas.json'):
    ev=e['evidence'];p=ROOT/ev['path']
    if p.is_file() and ev['text'].strip()!=read(p).splitlines()[ev['line']-1].strip():errors.append('Evidência curada mudou: '+ev['path']+':'+str(ev['line']))
for s in syms['symbols']:
    p=ROOT/s['path']
    if not p.is_file() or not 0<s['line']<=s['end_line']<=len(read(p).splitlines()):errors.append('Símbolo sem linha válida: '+str(s))
parts=load('dados/componentes.json')
if not parts['all_documented_fields_match_glb'] or len(set(p['partId'] for p in parts['parts']))!=len(parts['parts']):errors.append('Metadados das peças divergentes/duplicados')
for p in OUT.rglob('*.json'):
    if 'graphify-out' in p.parts:continue
    try:json.loads(read(p))
    except Exception as e:errors.append('JSON inválido: '+str(p)+' '+str(e))
for m in load('dados/manifesto-conferencia.json'):
    if not m['matches']:warnings.append('Manifesto do aplicativo não corresponde aos bytes atuais: '+m['arquivo'])
raw=load('dados/graphify-execucao.json')
if raw['diagnostics']['dangling_endpoint_edges']:warnings.append('AST bruto graphify contém '+str(raw['diagnostics']['dangling_endpoint_edges'])+' relações sem extremidade; não confundir com grafo validado desta documentação')
app=OUT/'dados/verificacao-app.json'
if app.exists():
    a=json.loads(read(app))
    for p,h in a['source_hashes'].items():
        if hashfile(ROOT/p)!=h:errors.append('Testes anteriores a mudança do fonte: '+p)
    if not a['build']['equals_checked_in_html']:warnings.append('HTML do app difere do build em memória; arquivo original foi preservado')
report={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':not errors,'links_checked':links,'catalog_files':len(cat['files']),'symbols':len(syms['symbols']),'nodes':len(ids),'edges':len(g['edges']),'parts':len(parts['parts']),'errors':errors,'warnings':warnings,'scope':'Links locais e âncoras Markdown, JSON, linhas de fonte, hashes, imports, extremos de grafo e metadados GLB. Não valida destinos HTTP nem a física do carro.'}
(OUT/'dados/validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
delivery=[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':hashfile(p)} for p in sorted(OUT.rglob('*')) if p.is_file() and 'graphify-out' not in p.parts and '__pycache__' not in p.parts and p.name not in ('entrega.json','servidor.pid') and p.suffix!='.log']
(OUT/'dados/entrega.json').write_text(json.dumps({'note':'Manifesto da documentação; exclui a si mesmo para evitar hash recursivo e caches/logs. Não substitui manifesto-sha256.json do aplicativo.','files':delivery},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False));sys.exit(1 if errors else 0)
