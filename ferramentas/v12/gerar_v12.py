"""Gera web/assets/v12-v1.glb + v12-v1.manifest.json: motor V12 aspirado de 65°, geometria original
INTEIA, ilustrativa e didática (não é CAD de fabricante).

  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --python ferramentas/v12/gerar_v12.py

O movimento NÃO é gravado no GLB. Os nós `v12_virabrequim`, `v12_pistao_01..12`, `v12_biela_01..12` e
`v12_comando_*` carregam extras com a cinemática (cilindro, bancada, defasagem do moente, eixo do cilindro),
e a aba 07 Som os move por código a partir do ângulo θ do reprodutor, em sincronia exata com o áudio.

Referencial do site (glTF): X à direita, Y para cima, Z para a frente do carro, metros.
O eixo do virabrequim é o eixo Z, passando pela origem.
"""
import bpy, math, sys, json, hashlib, time
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'ferramentas' / 'sistemas'))
import lib
from lib import (Materials, Context, W, to_web, UP, FWD, RIGHT, cube, cyl, sphere, torus, lathe,
                 sweep, gear, bolt_ring, join, text_plate, tube_cyl)

started = time.time()

# ----------------------------------------------------------------------------- arquitetura do motor
BANK_DEG = 65.0                  # ângulo em V
BETA = math.radians(BANK_DEG / 2)
BORE = 0.085                     # diâmetro do cilindro
STROKE = 0.0645                  # curso
CRANK_R = STROKE / 2             # raio do moente
ROD = 0.118                      # distância entre centros da biela
SPACING = 0.104                  # distância entre cilindros da mesma bancada
ROD_Z = 0.014                    # meia largura do par de bielas no mesmo moente
DECK = 0.148                     # centro do virabrequim até o plano do cabeçote
CYL = 12
PER_BANK = CYL // 2

# Ordem de ignição do perfil de som (web/src/sound/engine-profiles.mjs), intervalos de 60°.
FIRING_ORDER = [1, 7, 5, 11, 3, 9, 6, 12, 2, 8, 4, 10]
FIRE_AT = {cyl: i * 720 / CYL for i, cyl in enumerate(FIRING_ORDER)}

def bank_of(cyl):
    """'A' = bancada esquerda (cilindros 1–6), 'B' = bancada direita (7–12)."""
    return 'A' if cyl <= PER_BANK else 'B'

def side_of(cyl):
    return -1 if bank_of(cyl) == 'A' else 1

def index_in_bank(cyl):
    return (cyl - 1) % PER_BANK          # 0 = dianteiro

def axis_deg(cyl):
    """Ângulo do eixo do cilindro medido a partir da vertical (+Y), positivo rumo a +X."""
    return side_of(cyl) * BANK_DEG / 2

def axis_vec(cyl):
    a = math.radians(axis_deg(cyl))
    return Vector((math.sin(a), math.cos(a), 0.0))

def z_of(cyl):
    """Posição do cilindro ao longo do eixo do virabrequim (cilindro 1 é o dianteiro)."""
    k = index_in_bank(cyl)
    return (PER_BANK - 1) / 2 * SPACING - k * SPACING + (ROD_Z if bank_of(cyl) == 'A' else -ROD_Z)

def pin_offset_deg(cyl):
    """Defasagem do moente: o cilindro chega ao PMS quando θ + defasagem = ângulo do eixo do cilindro.
    Com V de 65° e ignição uniforme de 60°, cada moente é partido em 5° entre as duas bielas."""
    return (axis_deg(cyl) - FIRE_AT[cyl]) % 360

def pin_pos(cyl, theta_deg):
    """Centro do moente do cilindro para o ângulo θ do virabrequim."""
    psi = math.radians(theta_deg + pin_offset_deg(cyl))
    return Vector((CRANK_R * math.sin(psi), CRANK_R * math.cos(psi), z_of(cyl)))

def piston_distance(cyl, theta_deg):
    """Distância do centro do virabrequim ao pino do pistão, ao longo do eixo do cilindro."""
    gamma = math.radians(theta_deg + pin_offset_deg(cyl) - axis_deg(cyl))
    return CRANK_R * math.cos(gamma) + math.sqrt(ROD ** 2 - (CRANK_R * math.sin(gamma)) ** 2)

def wrist_pos(cyl, theta_deg):
    v = axis_vec(cyl) * piston_distance(cyl, theta_deg)
    return Vector((v.x, v.y, z_of(cyl)))

# Conferência da montagem antes de modelar: ignição uniforme e moentes compartilhados aos pares.
_fire = sorted(FIRE_AT.values())
assert all(abs(_fire[i + 1] - _fire[i] - 60) < 1e-9 for i in range(len(_fire) - 1)), 'ignição não uniforme'
for _c in range(1, PER_BANK + 1):
    _split = abs(pin_offset_deg(_c) - pin_offset_deg(_c + PER_BANK))
    assert abs(_split - 5.0) < 1e-6, f'moente {_c}: separação {_split:.2f}° (esperado 5°)'

# ----------------------------------------------------------------------------- cena
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
m = Materials()
ctx = Context(scene, m)
ctx.system('v12', 'Motor V12 65°')

MOVING = {}          # nome do nó -> extras de cinemática

def renomear(obj, name, **extras):
    obj.name = name
    obj['part'] = obj.get('part', name)
    for k, v in extras.items():
        obj[k] = v
    MOVING[name] = dict(extras)
    return obj

def marcar(obj, **extras):
    """Escreve extras no nó exportado (o registro da biblioteca só aceita um conjunto fixo)."""
    for k, v in extras.items():
        obj[k] = v
    return obj

def corte(obj):
    """Peça fundida ou carenagem: o site pode seccioná-la para mostrar o interior."""
    return marcar(obj, cut=1)

def origem_em(obj, point):
    """Deixa a peça móvel em referencial canônico: rotação identidade, malha nas coordenadas do site e
    origem no ponto dado. Sem isso a malha herda a orientação do primeiro objeto da junção e o site não
    pode simplesmente escrever `rotation.z`."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    scene.cursor.location = W(point)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    return obj

Z_FRONT = (PER_BANK - 1) / 2 * SPACING + 0.085
Z_BACK = -(PER_BANK - 1) / 2 * SPACING - 0.085
BLOCK_LEN = Z_FRONT - Z_BACK

# ----------------------------------------------------------------------------- bloco, cárter e bancadas
corte(cube(ctx, 'Bloco · cárter superior', (0, -0.012, 0), (0.212, 0.176, BLOCK_LEN), m.alu_cast, bev=.008, segments=3, uv=8))
corte(cube(ctx, 'Cárter seco · bandeja rasa', (0, -0.118, 0), (0.238, 0.046, BLOCK_LEN - 0.02), m.alu_cast, bev=.008, uv=8))
mancais = [cube(ctx, 'Mancal principal', (0, -0.052, (PER_BANK - 1) / 2 * SPACING - k * SPACING), (0.150, 0.072, 0.020), m.alu_cast, bev=.003)
           for k in range(PER_BANK + 1)]
corte(join(ctx, mancais, part='Tampas dos mancais principais'))
cube(ctx, 'Flange do cárter', (0, -0.094, 0), (0.246, 0.010, BLOCK_LEN - 0.01), m.alu_cast, bev=.002)

for side in (-1, 1):
    lab = 'esquerda' if side < 0 else 'direita'
    a = math.radians(side * BANK_DEG / 2)
    u = Vector((math.sin(a), math.cos(a), 0))
    rot = (0, 0, -side * BANK_DEG / 2)
    base = u * (DECK * 0.52)
    corte(cube(ctx, f'Bancada de cilindros {lab}', (base.x, base.y, 0), (0.104, DECK * 0.92, BLOCK_LEN - 0.03),
               m.alu_cast, rot=rot, bev=.006, uv=8))
    deck = u * DECK
    corte(cube(ctx, f'Cabeçote {lab}', (deck.x + u.x * 0.036, deck.y + u.y * 0.036, 0), (0.118, 0.072, BLOCK_LEN - 0.04),
               m.alu_cast, rot=rot, bev=.005, uv=8))
    tampa = u * (DECK + 0.094)
    corte(cube(ctx, f'Tampa de comando {lab}', (tampa.x, tampa.y, 0), (0.112, 0.048, BLOCK_LEN - 0.05),
               m.mag_cast, rot=rot, bev=.010, segments=3, uv=10))
    text_plate(ctx, f'Gravação da tampa {lab}', 'INTEIA V12', (tampa.x + u.x * 0.026, tampa.y + u.y * 0.026, 0.12),
               0.020, m.alu_bright, normal=(u.x, u.y, 0), up=FWD)
    # camisas úmidas aparentes no topo da bancada
    camisas = []
    for k in range(PER_BANK):
        z = (PER_BANK - 1) / 2 * SPACING - k * SPACING + (ROD_Z if side < 0 else -ROD_Z)
        c = u * (DECK - 0.030)
        camisas.append(cyl(ctx, f'Camisa do cilindro {lab} {k + 1}', (c.x, c.y, z), BORE / 2 + 0.006, 0.058,
                           m.steel, axis=(u.x, u.y, 0), verts=24, bev=.001))
    corte(join(ctx, camisas, part=f'Camisas úmidas {lab}'))
    # bobinas e injetores
    bobinas, inj = [], []
    for k in range(PER_BANK):
        z = (PER_BANK - 1) / 2 * SPACING - k * SPACING + (ROD_Z if side < 0 else -ROD_Z)
        p = u * (DECK + 0.124)
        bobinas.append(cyl(ctx, f'Bobina de ignição {lab} {k + 1}', (p.x, p.y, z), 0.012, 0.042, m.plastic_black,
                           axis=(u.x, u.y, 0), verts=14))
        q = u * (DECK + 0.020) + Vector((-side * math.cos(a), math.sin(a), 0)) * 0.058
        inj.append(cyl(ctx, f'Injetor {lab} {k + 1}', (q.x, q.y, z), 0.005, 0.040, m.steel, axis=(u.x, u.y, 0), verts=10))
    join(ctx, bobinas, part=f'Bobinas de ignição {lab}')
    join(ctx, inj, part=f'Injetores e galeria {lab}')

# ----------------------------------------------------------------------------- virabrequim
pecas_virab = []
for k in range(PER_BANK):
    cyl_a = k + 1
    zc = (PER_BANK - 1) / 2 * SPACING - k * SPACING
    # munhões principais entre os moentes
    for zz in (zc + SPACING / 2, zc - SPACING / 2):
        pecas_virab.append(cyl(ctx, 'Munhão principal', (0, 0, zz), 0.024, 0.026, m.steel, axis=FWD, verts=28, bev=.0008))
    for cyl_i in (cyl_a, cyl_a + PER_BANK):
        ang = math.radians(pin_offset_deg(cyl_i))
        d = Vector((math.sin(ang), math.cos(ang), 0)) * CRANK_R
        pecas_virab.append(cyl(ctx, f'Moente do cilindro {cyl_i}', (d.x, d.y, z_of(cyl_i)), 0.0165, 0.026,
                               m.steel, axis=FWD, verts=24, bev=.0006))
        # braço e contrapeso opostos ao moente
        pecas_virab.append(cube(ctx, 'Braço do virabrequim', (d.x / 2, d.y / 2, z_of(cyl_i) + (0.019 if cyl_i <= PER_BANK else -0.019)),
                                (0.052, 0.062, 0.011), m.steel, rot=(0, 0, -math.degrees(ang)), bev=.002))
        pecas_virab.append(cyl(ctx, 'Contrapeso', (-d.x * 0.62, -d.y * 0.62, z_of(cyl_i) + (0.019 if cyl_i <= PER_BANK else -0.019)),
                               0.050, 0.011, m.steel, axis=FWD, verts=20, bev=.001))
pecas_virab.append(cyl(ctx, 'Ponta dianteira do virabrequim', (0, 0, Z_FRONT - 0.010), 0.020, 0.060, m.steel, axis=FWD, verts=24))
pecas_virab.append(cyl(ctx, 'Amortecedor de vibrações torcionais', (0, 0, Z_FRONT + 0.028), 0.052, 0.020, m.steel_dark, axis=FWD, verts=36))
pecas_virab.append(cyl(ctx, 'Flange do volante', (0, 0, Z_BACK - 0.012), 0.072, 0.016, m.steel, axis=FWD, verts=40))
virabrequim = join(ctx, pecas_virab, part='Virabrequim de 6 moentes')
origem_em(virabrequim, (0, 0, 0))
renomear(virabrequim, 'v12_virabrequim', kinematics='crank', axisDeg=0.0)

# ----------------------------------------------------------------------------- pistões e bielas
for c in range(1, CYL + 1):
    u = axis_vec(c)
    z = z_of(c)
    wrist = wrist_pos(c, 0.0)
    pin = pin_pos(c, 0.0)
    ax = (u.x, u.y, 0)
    rotz = -axis_deg(c)
    # pistão: coroa, saia, aneis e pino
    corpo = wrist + u * 0.0245
    p1 = cyl(ctx, f'Coroa do pistão {c}', (corpo.x, corpo.y, z), BORE / 2 - 0.0008, 0.015, m.alu_bright, axis=ax, verts=28, bev=.0012)
    saia = wrist + u * 0.0015
    p2 = cyl(ctx, f'Saia do pistão {c}', (saia.x, saia.y, z), BORE / 2 - 0.0035, 0.040, m.alu, axis=ax, verts=28, bev=.001)
    aneis = []
    for j, off in enumerate((0.0290, 0.0255, 0.0220)):
        a = wrist + u * off
        aneis.append(torus(ctx, f'Anel {j + 1} do pistão {c}', (a.x, a.y, z), BORE / 2 - 0.0016, 0.0013, m.steel_dark, axis=ax, seg=28, mseg=6))
    p3 = cyl(ctx, f'Pino do pistão {c}', (wrist.x, wrist.y, z), 0.0095, 0.052, m.titanium, axis=FWD, verts=16, bev=.0004)
    pistao = join(ctx, [p1, p2, p3] + aneis, part=f'Pistão {c}')
    origem_em(pistao, (wrist.x, wrist.y, z))
    renomear(pistao, f'v12_pistao_{c:02d}', kinematics='piston', cylinder=c, bank=bank_of(c),
             pinOffsetDeg=round(pin_offset_deg(c), 4), axisDeg=round(axis_deg(c), 4), z=round(z, 5))

    # biela: modelada na vertical local (pé grande na origem, pé pequeno em +Y), posta na pose de θ=0
    corpo_b = []
    corpo_b.append(cyl(ctx, f'Pé grande da biela {c}', (0, 0, 0), 0.0245, 0.025, m.titanium, axis=FWD, verts=24, bev=.0008))
    corpo_b.append(cyl(ctx, f'Pé pequeno da biela {c}', (0, ROD, 0), 0.0145, 0.023, m.titanium, axis=FWD, verts=20, bev=.0008))
    corpo_b.append(cube(ctx, f'Haste da biela {c}', (0, ROD / 2, 0), (0.017, ROD - 0.030, 0.021), m.titanium, bev=.003, segments=3))
    for flange in (-0.0115, 0.0115):
        corpo_b.append(cube(ctx, f'Mesa da haste da biela {c}', (0, ROD / 2, flange), (0.027, ROD - 0.034, 0.005), m.titanium, bev=.0015))
    corpo_b.append(cube(ctx, f'Transição do pé grande da biela {c}', (0, 0.028, 0), (0.034, 0.030, 0.023), m.titanium, bev=.005, segments=3))
    corpo_b.append(cube(ctx, f'Capa da biela {c}', (0, -0.016, 0), (0.048, 0.016, 0.024), m.titanium, bev=.002))
    biela = join(ctx, corpo_b, part=f'Biela {c}')
    origem_em(biela, (0, 0, 0))
    delta = wrist - pin
    biela.location = W((pin.x, pin.y, z))
    biela.rotation_euler = lib.W_rot((0, 0, -math.degrees(math.atan2(delta.x, delta.y))))
    renomear(biela, f'v12_biela_{c:02d}', kinematics='rod', cylinder=c, bank=bank_of(c),
             pinOffsetDeg=round(pin_offset_deg(c), 4), axisDeg=round(axis_deg(c), 4),
             rodLength=round(ROD, 5), crankRadius=round(CRANK_R, 5), z=round(z, 5))

# ----------------------------------------------------------------------------- comandos e válvulas
VALVE_ANG = 16.0                 # meio ângulo entre admissão e escape
valve_count = {}
for side in (-1, 1):
    lab = 'esquerda' if side < 0 else 'direita'
    bank = 'A' if side < 0 else 'B'
    a = math.radians(side * BANK_DEG / 2)
    u = Vector((math.sin(a), math.cos(a), 0))
    out = Vector((side * math.cos(a), -math.sin(a), 0))       # normal externa da bancada
    for kind, sgn in (('admissão', -1), ('escape', 1)):
        cpos = u * (DECK + 0.068) + out * (sgn * 0.040)
        eixo = cyl(ctx, f'Comando de {kind} {lab}', (cpos.x, cpos.y, 0), 0.014, BLOCK_LEN - 0.08, m.steel,
                   axis=FWD, verts=20, bev=.0006)
        cames = []
        for k in range(PER_BANK * 2):
            z = (PER_BANK - 1) / 2 * SPACING - k * SPACING / 2
            cames.append(cyl(ctx, f'Came {k + 1}', (cpos.x, cpos.y, z), 0.019, 0.011, m.steel, axis=FWD, verts=18, bev=.0005))
        comando = join(ctx, [eixo] + cames, part=f'Comando de {kind} {lab}')
        origem_em(comando, (cpos.x, cpos.y, 0))
        renomear(comando, f'v12_comando_{"adm" if sgn < 0 else "esc"}_{bank.lower()}',
                 kinematics='cam', bank=bank, ratio=0.5, axisDeg=round(side * BANK_DEG / 2, 4))
    # 24 válvulas por cabeçote: 2 de admissão e 2 de escape por cilindro
    valvulas = []
    for k in range(PER_BANK):
        z = (PER_BANK - 1) / 2 * SPACING - k * SPACING + (ROD_Z if side < 0 else -ROD_Z)
        for sgn, nome in ((-1, 'admissão'), (1, 'escape')):
            av = math.radians(side * BANK_DEG / 2 + sgn * VALVE_ANG * side * -1)
            uv = Vector((math.sin(av), math.cos(av), 0))
            for dz in (-0.020, 0.020):
                haste = u * (DECK + 0.028) + out * (sgn * 0.024)
                valvulas.append(cyl(ctx, f'Válvula de {nome} {lab} {k + 1}', (haste.x, haste.y, z + dz), 0.0042, 0.070,
                                    m.steel, axis=(uv.x, uv.y, 0), verts=12, bev=.0004))
                prato = haste - uv * 0.036
                valvulas.append(cyl(ctx, f'Prato da válvula de {nome} {lab} {k + 1}', (prato.x, prato.y, z + dz), 0.0155, 0.006,
                                    m.steel_dark, axis=(uv.x, uv.y, 0), verts=16, bev=.0006, radius2=0.0135))
    valve_count[bank] = PER_BANK * 4
    marcar(join(ctx, valvulas, part=f'Válvulas do cabeçote {lab} (24)'), valves=valve_count[bank], bank=bank)

# ----------------------------------------------------------------------------- cascata de engrenagens
GEAR_Z = Z_BACK - 0.034
gear(ctx, 'Engrenagem do virabrequim', (0, 0, GEAR_Z), 34, 0.0016, 0.012, m.gear, axis=FWD, bore=0.020)
inter = []
for side in (-1, 1):
    a = math.radians(side * BANK_DEG / 2)
    u = Vector((math.sin(a), math.cos(a), 0))
    out = Vector((side * math.cos(a), -math.sin(a), 0))
    meio = u * (DECK * 0.62)
    gear(ctx, f'Engrenagem intermediária {"esquerda" if side < 0 else "direita"}', (meio.x, meio.y, GEAR_Z), 30, 0.0016, 0.012, m.gear, axis=FWD, bore=0.014)
    for kind, sgn in (('admissão', -1), ('escape', 1)):
        cpos = u * (DECK + 0.068) + out * (sgn * 0.040)
        gear(ctx, f'Engrenagem do comando de {kind} {"esquerda" if side < 0 else "direita"}',
             (cpos.x, cpos.y, GEAR_Z), 68, 0.0016, 0.012, m.gear, axis=FWD, bore=0.014)
cube(ctx, 'Carcaça da cascata de engrenagens', (0, DECK * 0.35, GEAR_Z - 0.012), (0.30, 0.34, 0.016), m.mag_cast, bev=.004, uv=8)

# ----------------------------------------------------------------------------- admissão: trompetas e airbox
for c in range(1, CYL + 1):
    side = side_of(c)
    a = math.radians(side * BANK_DEG / 2)
    u = Vector((math.sin(a), math.cos(a), 0))
    out = Vector((side * math.cos(a), -math.sin(a), 0))
    base = u * (DECK + 0.020) + out * (-0.058)
    boca = base + Vector((0, 0.104, 0))
    t = lathe(ctx, f'Trompeta de admissão {c}', [(0.026, 0), (0.026, 0.070), (0.030, 0.082), (0.040, 0.094), (0.036, 0.096), (0.026, 0.084), (0.022, 0.070), (0.022, 0)],
              m.alu_bright, center=(base.x, base.y, z_of(c)), axis=UP, segments=28)
    renomear(t, f'v12_trompeta_{c:02d}', intake=1, cylinder=c, bank=bank_of(c))
AIRBOX_Y = DECK + 0.155
AIRBOX_LEN = BLOCK_LEN - 0.13
corte(cube(ctx, 'Airbox · plenum central', (0, AIRBOX_Y, 0), (0.246, 0.052, AIRBOX_LEN), m.carbon, bev=.016, segments=3, uv=10,
            hide_group='airbox'))
corte(cube(ctx, 'Airbox · flange do plenum', (0, AIRBOX_Y - 0.030, 0), (0.262, 0.008, AIRBOX_LEN + 0.01), m.carbon_matte, bev=.002,
            hide_group='airbox'))
corte(cyl(ctx, 'Airbox · garganta de entrada', (0, AIRBOX_Y, AIRBOX_LEN / 2 + 0.016), 0.040, 0.034, m.carbon,
          axis=FWD, verts=28, radius2=0.034, hide_group='airbox'))
corte(torus(ctx, 'Airbox · aro da garganta', (0, AIRBOX_Y, AIRBOX_LEN / 2 + 0.032), 0.040, 0.0045, m.carbon_matte,
            axis=FWD, seg=28, mseg=8, hide_group='airbox'))

# ----------------------------------------------------------------------------- escape: dois coletores 6-em-1
for side in (-1, 1):
    lab = 'esquerda' if side < 0 else 'direita'
    a = math.radians(side * BANK_DEG / 2)
    u = Vector((math.sin(a), math.cos(a), 0))
    out = Vector((side * math.cos(a), -math.sin(a), 0))
    juncao = u * (DECK * 0.30) + out * 0.190
    tubos = []
    for k in range(PER_BANK):
        c = k + 1 if side < 0 else k + 1 + PER_BANK
        z = z_of(c)
        p0 = u * (DECK + 0.026) + out * 0.058
        p1 = u * (DECK * 0.86) + out * 0.130
        p2 = u * (DECK * 0.52) + out * 0.176
        tubos.append(sweep(ctx, f'Primário de escape {lab} {k + 1}',
                           [(p0.x, p0.y, z), (p1.x, p1.y, z * 0.86), (p2.x, p2.y, z * 0.52),
                            (juncao.x, juncao.y, Z_BACK * 0.34)],
                           m.inconel, radius=0.0175, sides=14, per_segment=7))
    col = sweep(ctx, f'Coletor 6-em-1 {lab} · junção', [(juncao.x, juncao.y, Z_BACK * 0.34), (juncao.x, juncao.y, Z_BACK - 0.03)],
                m.inconel, radius=0.030, sides=18, per_segment=6)
    meg = cyl(ctx, f'Megafone de saída {lab}', (juncao.x, juncao.y, Z_BACK - 0.082), 0.030, 0.104, m.inconel_plain,
              axis=FWD, verts=20, radius2=0.044)
    join(ctx, tubos + [col, meg], part=f'Coletor de escape 6-em-1 {lab}')

# ----------------------------------------------------------------------------- acessórios
cyl(ctx, 'Alternador', (0.128, 0.086, Z_FRONT + 0.010), 0.036, 0.086, m.alu, axis=FWD, verts=24)
cyl(ctx, 'Polia do alternador', (0.128, 0.086, Z_FRONT + 0.058), 0.022, 0.012, m.steel, axis=FWD, verts=20)
cyl(ctx, 'Polia do virabrequim', (0, 0, Z_FRONT + 0.050), 0.034, 0.012, m.steel, axis=FWD, verts=24)
cyl(ctx, 'Bomba de óleo · estágio de pressão', (-0.112, -0.086, 0.150), 0.030, 0.062, m.alu_cast, axis=FWD, verts=20)
cyl(ctx, 'Bomba de óleo · estágios de recuperação', (-0.112, -0.086, 0.040), 0.028, 0.120, m.alu_cast, axis=FWD, verts=20)
cyl(ctx, 'Bomba de água', (0.112, -0.078, 0.170), 0.034, 0.058, m.alu_cast, axis=FWD, verts=20)
sweep(ctx, 'Mangueira de água · saída', [(0.112, -0.078, 0.200), (0.130, -0.030, 0.240), (0.120, 0.040, 0.268)], m.silicone, radius=0.014, sides=12)
cyl(ctx, 'Filtro de óleo', (-0.128, -0.052, -0.130), 0.034, 0.090, m.anod_black, axis=FWD, verts=20)
for side in (-1, 1):
    cube(ctx, f'Suporte do motor {"esquerdo" if side < 0 else "direito"}', (side * 0.118, 0.040, Z_FRONT - 0.030), (0.016, 0.070, 0.056), m.titanium, bev=.003)
cube(ctx, 'Suporte traseiro · flange da caixa', (0, -0.010, Z_BACK - 0.042), (0.190, 0.190, 0.014), m.alu_cast, bev=.004, uv=8)
bolt_ring(ctx, 'Parafusos do flange traseiro', (0, -0.010, Z_BACK - 0.050), 0.082, 10, FWD, m.steel, size=.005, head=.004)

# ----------------------------------------------------------------------------- exportação
bpy.context.view_layer.update()
partes = [o for o in ctx.parts if o.type == 'MESH']
assert 60 <= len(partes) <= 90, f'{len(partes)} peças fora da faixa esperada'
bpy.ops.object.select_all(action='DESELECT')
for o in partes:
    o.parent = None
    o.select_set(True)
bpy.context.view_layer.objects.active = partes[0]
for e in list(ctx.systems.values()):
    bpy.data.objects.remove(e, do_unlink=True)

OUT = ROOT / 'web' / 'assets'
glb = OUT / 'v12-v1.glb'
bpy.ops.export_scene.gltf(filepath=str(glb), use_selection=True, export_format='GLB', export_apply=True,
                          export_yup=True, export_animations=False, export_extras=True, export_image_format='AUTO',
                          export_materials='EXPORT', export_cameras=False, export_lights=False,
                          export_normals=True, export_texcoords=True, export_tangents=False)

def bbox_web(o):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps)
    pts = [to_web(ev.matrix_world @ Vector(c)) for c in ev.bound_box]
    return [round(min(p[i] for p in pts), 4) for i in range(3)], [round(max(p[i] for p in pts), 4) for i in range(3)]

deps = bpy.context.evaluated_depsgraph_get()
nodes, triangles = [], 0
for o in partes:
    ev = o.evaluated_get(deps)
    tris = sum(len(p.vertices) - 2 for p in ev.data.polygons)
    triangles += tris
    mn, mx = bbox_web(o)
    entry = {'node': o.name, 'part': o.get('part', o.name), 'triangles': tris, 'min': mn, 'max': mx}
    if o.get('cut'):
        entry['cut'] = True
    if o.get('hide_group'):
        entry['hideGroup'] = o['hide_group']
    if o.name in MOVING:
        entry['kinematics'] = MOVING[o.name]
    nodes.append(entry)

cilindros = [{'cylinder': c, 'bank': bank_of(c), 'axisDeg': round(axis_deg(c), 4),
              'pinOffsetDeg': round(pin_offset_deg(c), 4), 'firesAtDeg': round(FIRE_AT[c], 4),
              'z': round(z_of(c), 5),
              'piston': f'v12_pistao_{c:02d}', 'rod': f'v12_biela_{c:02d}', 'trumpet': f'v12_trompeta_{c:02d}'}
             for c in range(1, CYL + 1)]

manifest = {
    'asset': glb.name,
    'bytes': glb.stat().st_size,
    'sha256': hashlib.sha256(glb.read_bytes()).hexdigest(),
    'generated_by': 'ferramentas/v12/gerar_v12.py',
    'blender': bpy.app.version_string,
    'license': 'Geometria original INTEIA, ilustrativa e didática; proporções inspiradas em V12 de 3.5 L dos anos 90.',
    'engine': {
        'id': 'v12_90s', 'cylinders': CYL, 'bankAngleDeg': BANK_DEG, 'boreM': BORE, 'strokeM': STROKE,
        'crankRadiusM': round(CRANK_R, 6), 'rodLengthM': ROD, 'cylinderSpacingM': SPACING,
        'deckHeightM': DECK, 'firingOrder': FIRING_ORDER, 'firingIntervalDeg': 720 / CYL,
        'crankNode': 'v12_virabrequim', 'crankAxis': 'z', 'crankSignDeg': -1,
        'camNodes': ['v12_comando_adm_a', 'v12_comando_esc_a', 'v12_comando_adm_b', 'v12_comando_esc_b'],
        'camRatio': 0.5,
    },
    'cylinders': cilindros,
    'counts': {'pistons': CYL, 'rods': CYL, 'trumpets': CYL, 'crankpins': PER_BANK,
               'valves': sum(valve_count.values()), 'valvesPerBank': valve_count,
               'camshafts': 4, 'nodes': len(nodes)},
    'totals': {'nodes': len(nodes), 'triangles': triangles},
    'nodes': nodes,
}
(OUT / 'v12-v1.manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')
print('V12_OK', glb.name, len(nodes), 'nós', triangles, 'triângulos', f'{manifest["bytes"] / 1e6:.2f} MB', f'{time.time() - started:.1f}s')
