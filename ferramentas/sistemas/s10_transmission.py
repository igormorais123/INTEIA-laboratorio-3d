"""10 · Câmbio e diferencial: carcaça estrutural com janela de corte, embreagem multidisco,
oito pares de engrenagens em tomada constante mais ré, anéis de engate, tambor seletor com
garfos, pinhão e coroa, diferencial, semieixos com juntas tripoide e homocinética.
"""
import math
from lib import *

SYSTEM = ('transmission', 'Câmbio e diferencial')

Z_BELL = -1.345      # face traseira do motor
Z_CASE = -1.50       # início da carcaça principal
Z_END = -1.985       # tampa traseira
AXLE = (0.0, 0.342, -1.838)
INPUT_Y, LAY_Y = 0.415, 0.325          # eixos primário (superior) e secundário (inferior)
MODULE = .0034
PAIRS = [(13, 31), (15, 29), (17, 27), (19, 25), (21, 23), (23, 21), (25, 19), (27, 17)]   # soma constante: 44 dentes
ENGAGED = 3                             # 4ª marcha engatada no repouso didático
INPUT_RATE = 2.4                        # rad/s do eixo primário na animação do site
SHOTS = {
    'lateral-corte': ((0.0, 0.40, -1.72), 0.42, (1, .55, .35)),
    'engrenagens': ((0.0, 0.37, -1.68), 0.20, (.7, .9, .5)),
    'diferencial': ((0.1, 0.34, -1.84), 0.30, (.4, .5, -1)),
    'embreagem': ((0.0, 0.42, -1.43), 0.16, (1, .35, .6)),
}

def rr_section(w, h, r=.02):
    return rounded_rect(w, h, r)

def build(ctx):
    m = ctx.m
    # Carcaça: campânula do motor à caixa principal e à tampa traseira (carbono com insertos de titânio)
    sections = []
    for z, w, h, yc in ((Z_BELL, .60, .44, .43), (Z_CASE, .38, .40, .40), (-1.62, .34, .38, .385), (-1.78, .30, .34, .37), (Z_END, .26, .30, .36)):
        sections.append([(px, yc + py, z) for px, py in rr_section(w, h, .04)])
    case = shell(ctx, 'Carcaça do câmbio · estrutural', sections, m.carbon_matte, thickness=.006, hide_group='gearbox_case')
    # janela de corte no lado direito superior (para estudo das relações)
    bpy.ops.mesh.primitive_cube_add(size=1, location=W((.16, .50, -1.72)))
    cutter = bpy.context.object; cutter.scale = (.22, .40, .22); bpy.ops.object.transform_apply(scale=True)
    mod = case.modifiers.new('Janela de inspeção', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cutter; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = case
    for md in list(case.modifiers):
        bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.data.objects.remove(cutter)
    box_uv(case, 12)
    cube(ctx, 'Tampa traseira da carcaça', (0, .36, Z_END - .006), (.26, .30, .012), m.titanium, bev=.003, hide_group='gearbox_case')
    bolt_ring(ctx, 'Parafusos da tampa traseira', (0, .36, Z_END - .012), .12, 10, (0, 0, -1), m.steel, size=.005, head=.003)
    bolt_ring(ctx, 'Prisioneiros da campânula ao motor', (0, .43, Z_BELL + .004), .26, 12, (0, 0, 1), m.steel, size=.006, head=.004)
    # pontos de ancoragem da suspensão traseira sobre a carcaça (insertos de titânio)
    for side in (-1, 1):
        for p in ((side * .175, .505, -1.61), (side * .175, .495, -2.01), (side * .16, .205, -1.59), (side * .16, .195, -2.03)):
            cube(ctx, 'Inserto de ancoragem da suspensão', p, (.03, .03, .04), m.titanium, bev=.003)
    # Embreagem multidisco em carbono na campânula
    zc = -1.42
    lathe(ctx, 'Cesto da embreagem', [(.030, -.028), (.078, -.028), (.082, -.020), (.082, .026), (.070, .026), (.070, -.018), (.030, -.018), (.030, -.028)], m.titanium, center=(0, INPUT_Y, zc), axis=FWD, segments=40, spin=INPUT_RATE)
    for i in range(6):
        cyl(ctx, f'Disco de embreagem {i + 1}', (0, INPUT_Y, zc - .015 + i * .0065), .066, .004, m.brake_pad if i % 2 else m.steel, axis=FWD, verts=40, spin=INPUT_RATE)
    cyl(ctx, 'Placa de pressão da embreagem', (0, INPUT_Y, zc + .028), .070, .008, m.alu, axis=FWD, verts=40, spin=INPUT_RATE)
    cyl(ctx, 'Rolamento de acionamento da embreagem', (0, INPUT_Y, zc + .045), .030, .018, m.steel, axis=FWD, verts=32)
    cyl(ctx, 'Cilindro escravo hidráulico da embreagem', (0, INPUT_Y, zc + .062), .040, .022, m.anod_black, axis=FWD, verts=32)
    # Eixos primário e secundário
    cyl(ctx, 'Eixo primário', (0, INPUT_Y, -1.72), .015, .58, m.steel, axis=FWD, verts=24, spin=INPUT_RATE, carrier=True)
    lay_rate = -INPUT_RATE * PAIRS[ENGAGED][0] / PAIRS[ENGAGED][1]
    cyl(ctx, 'Eixo secundário', (0, LAY_Y, -1.72), .017, .52, m.steel, axis=FWD, verts=24, spin=lay_rate, carrier=True)
    # Oito pares em tomada constante; as engrenagens do secundário giram livres na relação de cada par
    z0 = -1.545
    for i, (n1, n2) in enumerate(PAIRS):
        z = z0 - i * .0345
        gear(ctx, f'Engrenagem {i + 1}ª · primário ({n1} dentes)', (0, INPUT_Y, z), n1, MODULE, .013, m.gear, axis=FWD, bore=.015, spin=INPUT_RATE)
        gear(ctx, f'Engrenagem {i + 1}ª · secundário ({n2} dentes)', (0, LAY_Y, z), n2, MODULE, .013, m.gear, axis=FWD, bore=.020, spin=-INPUT_RATE * n1 / n2)
    # Anéis de engate (dog rings) entre pares, no eixo secundário; o da 4ª está engatado
    for k in range(4):
        z = z0 - (2 * k + .5) * .0345
        ring = lathe(ctx, f'Anel de engate {2 * k + 1}ª/{2 * k + 2}ª', [(.020, -.006), (.036, -.006), (.036, .006), (.020, .006), (.020, -.006)], m.steel_dark, center=(0, LAY_Y, z), axis=FWD, segments=32, spin=lay_rate)
        for d in range(6):
            a = 2 * math.pi * d / 6
            cube(ctx, f'Dente de engate {2 * k + 1}ª/{2 * k + 2}ª', (.030 * math.cos(a), LAY_Y + .030 * math.sin(a), z + (.010 if k == 1 else -.010)), (.006, .006, .008), m.steel_dark, bev=.0006, spin=lay_rate)
    # Ré: engrenagem intermediária deslocada
    gear(ctx, 'Engrenagem intermediária da ré', (.075, .37, -1.515), 14, MODULE, .012, m.gear, axis=FWD, bore=.008, spin=-INPUT_RATE * 13 / 14)
    cyl(ctx, 'Eixo da intermediária da ré', (.075, .37, -1.515), .006, .05, m.steel, axis=FWD, verts=12)
    # Tambor seletor com pistas helicoidais, garfos e atuador hidráulico
    barrel = (-.085, .37, -1.67)
    cyl(ctx, 'Tambor seletor', barrel, .024, .30, m.alu, axis=FWD, verts=32)
    for k in range(4):
        helix(ctx, f'Pista {k + 1} do tambor seletor', (barrel[0], barrel[1], barrel[2] + .105 - k * .07), .0245, .012, 1.0, .0025, m.steel_dark, axis=FWD, per_turn=24)
        zf = z0 - (2 * k + .5) * .0345
        fork = sweep(ctx, f'Garfo seletor {2 * k + 1}ª/{2 * k + 2}ª', [(barrel[0], barrel[1], zf), (barrel[0] + .03, barrel[1] - .01, zf), (-.03, LAY_Y + .03, zf), (0, LAY_Y + .038, zf), (.03, LAY_Y + .03, zf)], m.alu,
                     section=lambda t: rounded_rect(.008, .012, .002), smooth_path=True)
    cyl(ctx, 'Atuador hidráulico de troca de marcha', (barrel[0], barrel[1], barrel[2] + .19), .028, .06, m.anod_black, axis=FWD, verts=28)
    cyl(ctx, 'Sensor de posição do tambor', (barrel[0], barrel[1], barrel[2] - .17), .012, .025, m.plastic_black, axis=FWD, verts=16)
    # Pinhão de saída e coroa do diferencial
    gear(ctx, 'Pinhão da transmissão final', (0, LAY_Y, -1.875), 11, .0045, .020, m.gear, axis=FWD, bore=.017, spin=lay_rate)
    crown = gear(ctx, 'Coroa do diferencial', (.045, AXLE[1], AXLE[2]), 40, .0045, .016, m.gear, axis=RIGHT, bore=.060, spin=lay_rate * 11 / 40)
    # Diferencial autoblocante: carcaça, flanges de saída, controle hidráulico
    diff_rate = lay_rate * 11 / 40
    lathe(ctx, 'Carcaça do diferencial', [(.030, -.085), (.062, -.085), (.075, -.060), (.075, .030), (.062, .040), (.030, .040), (.030, -.085)], m.alu_cast, center=AXLE, axis=RIGHT, segments=40, spin=diff_rate)
    bolt_ring(ctx, 'Parafusos da coroa', (.054, AXLE[1], AXLE[2]), .068, 12, (1, 0, 0), m.steel, size=.005, head=.003)
    for side in (-1, 1):
        lab = 'esquerdo' if side < 0 else 'direito'
        cyl(ctx, f'Flange de saída {lab}', (side * .11, AXLE[1], AXLE[2]), .036, .026, m.steel, axis=RIGHT, verts=28, spin=diff_rate)
        # tripoide interna: copo, aranha de três roletes
        lathe(ctx, f'Copo da junta tripoide {lab}', [(.0, -.03), (.046, -.03), (.046, .04), (.040, .04), (.040, -.024), (.0, -.024)], m.steel, center=(side * .165, AXLE[1], AXLE[2]), axis=(side, 0, 0), segments=32, spin=diff_rate)
        for r_i in range(3):
            a = 2 * math.pi * r_i / 3
            cyl(ctx, f'Rolete da tripoide {r_i + 1} {lab}', (side * .18, AXLE[1] + .026 * math.sin(a), AXLE[2] + .026 * math.cos(a)), .010, .014, m.steel_dark, axis=(0, math.sin(a), math.cos(a)), verts=14, spin=diff_rate)
        helix(ctx, f'Coifa da junta tripoide {lab}', (side * .215, AXLE[1], AXLE[2]), .040, .010, 3, .004, m.rubber, axis=RIGHT, per_turn=20)
        # semieixo oco em aço, junta homocinética externa e flange do cubo
        cyl(ctx, f'Semieixo {lab}', (side * .40, AXLE[1], AXLE[2]), .017, .36, m.steel, axis=RIGHT, verts=24, spin=diff_rate, carrier=True)
        sphere(ctx, f'Junta homocinética externa {lab}', (side * .585, AXLE[1], AXLE[2]), .040, m.steel, spin=diff_rate)
        helix(ctx, f'Coifa da homocinética {lab}', (side * .555, AXLE[1], AXLE[2]), .036, .009, 3, .0035, m.rubber, axis=RIGHT, per_turn=20)
        cyl(ctx, f'Flange de acionamento do cubo {lab}', (side * .625, AXLE[1], AXLE[2]), .034, .020, m.steel, axis=RIGHT, verts=28, spin=diff_rate)
    cyl(ctx, 'Atuador hidráulico do diferencial', (-.10, AXLE[1] + .05, AXLE[2] - .11), .024, .06, m.anod_black, axis=RIGHT, verts=28)
    # Bomba de óleo do câmbio e conexões do arrefecedor
    cyl(ctx, 'Bomba de óleo do câmbio', (.13, .27, -1.56), .028, .05, m.alu_cast, axis=FWD, verts=28)
    for dz, lab in ((-.02, 'saída'), (.02, 'retorno')):
        cyl(ctx, f'Conexão do óleo do câmbio · {lab}', (.155, .27 + dz, -1.56), .007, .02, m.anod_blue, axis=RIGHT, verts=10)
    flow_ribbon(ctx, 'Torque · motor → embreagem → primário', [(0, INPUT_Y, -1.35), (0, INPUT_Y, -1.75)], 'hyd', radius=.004)
    flow_ribbon(ctx, 'Torque · secundário → coroa → semieixos', [(0, LAY_Y, -1.55), (0, LAY_Y, -1.87), (.04, AXLE[1], AXLE[2]), (.45, AXLE[1], AXLE[2])], 'hyd', radius=.004)
    flow_ribbon(ctx, 'Torque · coroa → semieixo esquerdo', [(-.02, AXLE[1], AXLE[2]), (-.45, AXLE[1], AXLE[2])], 'hyd', radius=.004)
