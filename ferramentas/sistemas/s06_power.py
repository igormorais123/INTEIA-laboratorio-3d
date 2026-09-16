"""06 · Unidade de potência térmica: V6 de 90° com bloco, cárter seco, cabeçotes e tampas de
comando, turbo dividido (compressor à frente, turbina atrás, eixo comum pelo vale em V) com
MGU-H coaxial (legado 2021), plenums com seis trompetas, snorkel do airbox, dutos de ar
comprimido para o intercooler, coletores de escape em Inconel, wastegates e escapamento.
O V6 detalhado com pistões animados continua na bancada Motor; aqui a arquitetura é a do
carro inteiro, na escala do carro v2.
"""
import math
from lib import *

SYSTEM = ('power', 'Unidade de potência')

C = (0.0, 0.40, -0.92)        # centro do bloco
Z0, Z1 = -1.22, -0.62         # comprimento do bloco
BANK = math.radians(45)
TURBO_Y = 0.60
COMP_Z, TURB_Z = -0.535, -1.36
SHOTS = {
    'tres-quartos': ((0.0, 0.55, -0.95), 0.62, (1, .5, .9)),
    'vale-em-v': ((0.0, 0.70, -0.92), 0.32, (.001, 1, .3)),
    'turbo-dianteiro': ((0.0, 0.60, -0.55), 0.22, (.8, .5, 1)),
    'escape-turbina': ((0.0, 0.52, -1.40), 0.34, (1, .35, -.9)),
    'plenum-trompetas': ((0.0, 0.76, -0.92), 0.26, (.6, .9, .4)),
}

def bank_frame(side):
    """Eixo do cilindro (para cima e para fora) e normal externa da bancada."""
    up = (side * math.sin(BANK), math.cos(BANK), 0)
    out = (side * math.cos(BANK), -math.sin(BANK), 0)
    return up, out

def add(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s, a[2] + b[2] * s)

def build(ctx):
    m = ctx.m
    # Bloco (cárter) e cárter seco raso
    cube(ctx, 'Bloco do motor · cárter superior', (0, .40, -.92), (.40, .20, .60), m.alu_cast, bev=.012, segments=3, uv=8)
    cube(ctx, 'Cárter seco · bandeja rasa', (0, .275, -.92), (.46, .07, .58), m.alu_cast, bev=.010, uv=8)
    for z in (-1.16, -1.04, -.92, -.80, -.68):
        cube(ctx, 'Nervura estrutural do bloco', (0, .40, z), (.43, .16, .012), m.alu_cast, bev=.002)
    cyl(ctx, 'Virabrequim · munhão dianteiro', (0, .40, -.60), .028, .05, m.steel, axis=FWD, verts=28, spin=6.0)
    cyl(ctx, 'Amortecedor de vibrações torcionais', (0, .40, -.575), .055, .018, m.steel_dark, axis=FWD, verts=36, spin=6.0)
    cyl(ctx, 'Flange do volante para a embreagem', (0, .415, -1.235), .085, .018, m.steel, axis=FWD, verts=40, spin=6.0)
    # Bancadas: bloco de cilindros, cabeçote, tampa de comando, bobinas e portas de escape
    for side in (-1, 1):
        up, out = bank_frame(side)
        lab = 'esquerda' if side < 0 else 'direita'
        rot = (0, 0, -side * 45)
        base = (0, .46, -.92)
        cube(ctx, f'Bancada de cilindros {lab}', add(base, up, .10), (.20, .16, .56), m.alu_cast, rot=rot, bev=.008, uv=8)
        cube(ctx, f'Cabeçote {lab}', add(base, up, .215), (.21, .075, .56), m.alu_cast, rot=rot, bev=.006, uv=8)
        cover = cube(ctx, f'Tampa de comando {lab}', add(base, up, .285), (.19, .065, .54), m.carbon_matte, rot=rot, bev=.014, segments=3, uv=10)
        cube(ctx, f'Nervura da tampa de comando {lab}', add(add(base, up, .32), out, .03), (.09, .012, .50), m.carbon_matte, rot=rot, bev=.003)
        text_plate(ctx, f'Gravação da tampa {lab}', 'INTEIA V6 TURBO', add(add(base, up, .323), out, -.04), .022, m.alu_bright, normal=up, up=FWD)
        for k, z in enumerate((-1.10, -.92, -.74)):
            p = add((0, .46, z), up, .33)
            cyl(ctx, f'Bobina de ignição {lab} {k + 1}', p, .014, .05, m.plastic_black, axis=up, verts=16)
            cube(ctx, f'Conector da bobina {lab} {k + 1}', add(p, up, .03), (.02, .012, .03), m.plastic_black, bev=.001)
            # portas de escape na face externa do cabeçote
            port = add(add((0, .46, z), up, .215), out, .105)
            cyl(ctx, f'Flange da porta de escape {lab} {k + 1}', port, .030, .012, m.inconel_plain, axis=out, verts=24)
        # galeria de injeção e injetores na face interna (vale)
        rail = add(add(base, up, .26), out, -.10)
        cyl(ctx, f'Galeria de combustível {lab}', rail, .010, .52, m.alu, axis=FWD, verts=16)
        for z in (-1.10, -.92, -.74):
            cyl(ctx, f'Injetor direto {lab}', add(add((0, .46, z), up, .235), out, -.10), .006, .05, m.steel, axis=up, verts=10)
    # Turbo dividido: compressor frontal, eixo comum pelo vale, turbina traseira
    comp = (0, TURBO_Y, COMP_Z)
    lathe(ctx, 'Compressor · carcaça (voluta)', [(0, -.045), (.052, -.045), (.075, -.030), (.095, -.010), (.098, .010), (.085, .030), (.055, .040), (.0, .040)], m.alu_cast, center=comp, axis=FWD, segments=48)
    sweep(ctx, 'Compressor · saída da voluta', [(.06, TURBO_Y + .02, COMP_Z), (.12, TURBO_Y + .04, COMP_Z + .02), (.17, TURBO_Y + .02, COMP_Z + .05)], m.alu_cast, radius=.028, sides=20)
    lathe(ctx, 'Compressor · boca de entrada', [(.038, 0), (.044, 0), (.050, .04), (.056, .06), (.046, .06), (.040, .04), (.038, 0)], m.alu, center=(0, TURBO_Y, COMP_Z + .04), axis=FWD, segments=36)
    wheel = cyl(ctx, 'Rotor do compressor', (0, TURBO_Y, COMP_Z + .02), .036, .03, m.alu_bright, axis=FWD, verts=24, radius2=.012, spin=12.0)
    for b in range(9):
        a = 2 * math.pi * b / 9
        cube(ctx, 'Pá do rotor do compressor', (0.024 * math.cos(a), TURBO_Y + .024 * math.sin(a), COMP_Z + .025), (.004, .022, .028), m.alu_bright, rot=(0, 0, math.degrees(a) + 25), bev=.0005, spin=12.0)
    cyl(ctx, 'Eixo comum do turbo · titânio', (0, TURBO_Y, (COMP_Z + TURB_Z) / 2), .011, TURB_Z * -1 + COMP_Z + .0, m.titanium, axis=FWD, verts=16, spin=12.0)
    for z in (-.66, -1.20):
        cyl(ctx, 'Mancal do eixo do turbo', (0, TURBO_Y, z), .024, .04, m.steel_dark, axis=FWD, verts=24)
    # MGU-H coaxial no vale (legado 2021)
    lathe(ctx, 'MGU-H · carcaça (legado 2021)', [(.012, -.09), (.046, -.09), (.050, -.08), (.050, .08), (.046, .09), (.012, .09), (.012, -.09)], m.anod_black, center=(0, TURBO_Y, -.93), axis=FWD, segments=36, era='2021')
    for k in range(8):
        cyl(ctx, 'Aleta de refrigeração do MGU-H', (0, TURBO_Y, -.99 + k * .017), .056, .003, m.anod_black, axis=FWD, verts=36, era='2021')
    cube(ctx, 'Conector trifásico do MGU-H', (.04, TURBO_Y + .04, -.93), (.03, .02, .04), m.hv, bev=.002, era='2021')
    cyl(ctx, 'Rotor do MGU-H', (0, TURBO_Y, -.93), .020, .19, m.copper, axis=FWD, verts=24, spin=12.0, era='2021')
    text_plate(ctx, 'Etiqueta do MGU-H', 'MGU-H', (0, TURBO_Y + .052, -.93), .014, m.alu_bright, normal=UP, up=FWD, era='2021')
    # Turbina traseira em ferro fundido/Inconel com saída central e wastegates
    turb = (0, TURBO_Y - .04, TURB_Z)
    lathe(ctx, 'Turbina · carcaça quente', [(0, -.045), (.050, -.045), (.078, -.028), (.092, -.006), (.090, .016), (.070, .034), (.040, .044), (.0, .044)], m.inconel_plain, center=turb, axis=(0, 0, -1), segments=48)
    turbine_wheel = cyl(ctx, 'Rotor da turbina', (0, TURBO_Y - .04, TURB_Z - .02), .034, .03, m.inconel_plain, axis=FWD, verts=24, radius2=.014, spin=12.0)
    for b in range(11):
        a = 2 * math.pi * b / 11
        cube(ctx, 'Pá do rotor da turbina', (0.022 * math.cos(a), TURBO_Y - .04 + .022 * math.sin(a), TURB_Z - .022), (.004, .020, .026), m.inconel_plain, rot=(0, 0, math.degrees(a) - 30), bev=.0005, spin=12.0)
    # coletores de escape 3-em-1 por bancada em Inconel com pátina térmica
    for side in (-1, 1):
        up, out = bank_frame(side)
        lab = 'esquerdo' if side < 0 else 'direito'
        collector = (side * .17, .45, -1.27)
        for k, z in enumerate((-1.10, -.92, -.74)):
            port = add(add((0, .46, z), up, .225), out, .115)
            p1 = add(port, out, .06)
            p2 = (side * .335, .44, z - .08)
            pts = [port, p1, p2, (side * .31, .42, -1.19), collector]
            sweep(ctx, f'Primário de escape {lab} {k + 1}', pts, m.inconel, radius=.020, sides=16, uv_len=1.0, carrier=True)
        sweep(ctx, f'Coletor 3-em-1 {lab} → turbina', [collector, (side * .10, .50, -1.33), (side * .03, .55, -1.355)], m.inconel, radius=.030, sides=18, uv_len=1.0, carrier=True)
        # wastegate: válvula e tubo de alívio paralelo ao escape principal
        wg = (side * .075, .50, -1.42)
        cyl(ctx, f'Wastegate {lab} · atuador', add(wg, (0, .05, 0)), .016, .04, m.steel_dark, axis=UP, verts=20)
        sweep(ctx, f'Tubo da wastegate {lab}', [wg, (side * .075, .47, -1.60), (side * .07, .45, -2.06)], m.inconel, radius=.014, sides=14, uv_len=1.0, carrier=True)
    sweep(ctx, 'Escapamento central · saída da turbina', [(0, TURBO_Y - .04, TURB_Z - .05), (0, .53, -1.55), (0, .49, -1.80), (0, .475, -2.07)], m.inconel, radius=.046, sides=24, uv_len=1.0, carrier=True)
    torus(ctx, 'Braçadeira em V do escapamento', (0, .525, -1.58), .050, .006, m.steel, axis=FWD, seg=32, mseg=8)
    # Airbox: snorkel do santo antônio até a entrada do compressor; filtro e câmara
    air_in = (0, 1.02, -.34)
    sweep(ctx, 'Snorkel do airbox → compressor', [air_in, (0, .92, -.40), (0, .78, -.46), (0, TURBO_Y + .04, -.49), (0, TURBO_Y, COMP_Z + .08)], m.carbon_matte,
          section=lambda t: super_ellipse(.22 - .14 * t, .12 - .03 * t, 2.4, 24) if t < .8 else super_ellipse(.09, .09, 2.0, 24), smooth_path=True, carrier=True)
    cube(ctx, 'Elemento filtrante do airbox', (0, .93, -.40), (.16, .06, .04), m.foam, rot=(30, 0, 0), bev=.004)
    # Ar comprimido: compressor → intercooler (sidepod esquerdo) → plenums
    charge_out = [(.17, TURBO_Y + .02, COMP_Z + .05), (.10, .66, -.40), (-.18, .60, -.30), (-.40, .50, -.20)]
    sweep(ctx, 'Duto de ar comprimido · compressor → intercooler', charge_out, m.carbon_matte, radius=.030, sides=20, uv_len=6, carrier=True)
    for p in (charge_out[1], charge_out[-1]):
        torus(ctx, 'Junta e abraçadeira do duto', p, .031, .005, m.anod_blue, axis=FWD, seg=28, mseg=8)
    charge_back = [(-.40, .55, -.75), (-.26, .70, -.78), (-.10, .82, -.80), (0, .84, -.86)]
    sweep(ctx, 'Duto de ar resfriado · intercooler → plenums', charge_back, m.carbon_matte, radius=.030, sides=20, uv_len=6, carrier=True)
    torus(ctx, 'Abraçadeira do retorno do intercooler', charge_back[0], .031, .005, m.anod_blue, axis=RIGHT, seg=28, mseg=8)
    # Plenums com trompetas (velocity stacks); as tampas podem ser ocultadas no site
    for side in (-1, 1):
        up, out = bank_frame(side)
        lab = 'esquerdo' if side < 0 else 'direito'
        pc = (side * .12, .78, -.92)
        # corpo do plenum como caixa aberta no topo (paredes finas), para que as trompetas apareçam com a tampa oculta
        cube(ctx, f'Plenum de admissão {lab} · fundo', (pc[0], pc[1] - .046, pc[2]), (.15, .008, .56), m.carbon_matte, bev=.003, uv=10)
        for dx in (-1, 1):
            cube(ctx, f'Plenum de admissão {lab} · parede lateral', (pc[0] + dx * .071, pc[1], pc[2]), (.008, .10, .56), m.carbon_matte, bev=.003, uv=10)
        for dz in (-1, 1):
            cube(ctx, f'Plenum de admissão {lab} · parede de extremidade', (pc[0], pc[1], pc[2] + dz * .276), (.15, .10, .008), m.carbon_matte, bev=.003, uv=10)
        cube(ctx, f'Plenum de admissão {lab} · tampa', (pc[0], pc[1] + .054, pc[2]), (.156, .014, .566), m.carbon, bev=.006, uv=10, hide_group='plenum_lid')
        sweep(ctx, f'Ramal do plenum {lab}', [(0, .84, -.86), (side * .06, .845, -.84), (side * .12, .84, -.78)], m.carbon_matte, radius=.024, sides=16, uv_len=4, carrier=True)
        for k, z in enumerate((-1.10, -.92, -.74)):
            base = (pc[0], pc[1] - .02, z)
            lathe(ctx, f'Trompeta de admissão {lab} {k + 1}', [(.016, -.05), (.020, -.05), (.020, .0), (.024, .02), (.034, .035), (.040, .038), (.038, .040), (.028, .034), (.021, .018), (.017, 0), (.016, -.05)], m.alu, center=base, axis=up, segments=32)
            cyl(ctx, f'Borboleta de admissão {lab} {k + 1}', add(base, up, -.07), .014, .003, m.alu, axis=up, verts=20)
    # Auxiliares dianteiros: bomba d'água, bomba de óleo, reservatório de óleo do cárter seco, bomba de alta pressão
    cyl(ctx, "Bomba d'água", (.16, .40, -.585), .040, .05, m.alu_cast, axis=FWD, verts=28)
    cyl(ctx, "Polia da bomba d'água", (.16, .40, -.555), .030, .008, m.steel, axis=FWD, verts=28, spin=6.0)
    cyl(ctx, 'Bomba de óleo de estágios múltiplos', (-.16, .36, -.585), .034, .06, m.alu_cast, axis=FWD, verts=28)
    lathe(ctx, 'Reservatório de óleo do cárter seco', [(0, -.13), (.062, -.13), (.070, -.11), (.070, .11), (.062, .13), (0, .13)], m.alu, center=(-.31, .44, -.58), axis=UP, segments=36)
    cyl(ctx, 'Tampa do reservatório de óleo', (-.31, .58, -.58), .022, .012, m.anod_red, axis=UP, verts=20)
    cyl(ctx, 'Bomba de combustível de alta pressão', (.20, .60, -.66), .024, .08, m.alu, axis=(1, .5, 0), verts=24)
    sweep(ctx, 'Correia de comando dos auxiliares', [(.16, .43, -.552), (.0, .455, -.552), (-.16, .39, -.552), (0, .345, -.552)], m.rubber, radius=.006, sides=8, closed=True, smooth_path=True)
    # Fluxos didáticos: ar → compressor → intercooler → plenums → cilindros → escape → turbina → escapamento
    flow_ribbon(ctx, 'Ar de admissão · airbox → compressor', [(0, 1.06, -.30), (0, .92, -.40), (0, .78, -.46), (0, TURBO_Y, COMP_Z + .06)], 'air', radius=.007)
    flow_ribbon(ctx, 'Ar comprimido · compressor → intercooler', charge_out, 'charge', radius=.006)
    flow_ribbon(ctx, 'Ar resfriado · intercooler → plenums', charge_back + [(-.12, .82, -.92)], 'charge', radius=.006)
    flow_ribbon(ctx, 'Gases de escape · coletores → turbina → escapamento', [(.26, .48, -1.0), (.12, .50, -1.28), (0, .56, -1.36), (0, .53, -1.55), (0, .475, -2.10)], 'exhaust', radius=.007)
    flow_ribbon(ctx, 'Gases de escape · bancada esquerda', [(-.26, .48, -1.0), (-.12, .50, -1.28), (0, .56, -1.36)], 'exhaust', radius=.007)
