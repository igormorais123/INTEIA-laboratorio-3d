"""07 · ERS híbrido: energy store sob o tanque (módulos de células, barramentos, contator),
eletrônica de controle/inversor, MGU-K engrenado ao virabrequim, cabos de alta tensão
laranja e caminhos de recuperação e entrega (o MGU-H coaxial está na camada Motor, era 2021).
"""
import math
from lib import *

SYSTEM = ('ers', 'ERS híbrido')

ES = (0.0, 0.215, -0.32)          # centro do energy store (sob a célula de combustível)
ES_SIZE = (0.46, 0.12, 0.30)
CE = (0.33, 0.27, -0.55)          # eletrônica de controle / inversor (lado direito, baixo)
MGUK = (0.27, 0.31, -0.93)        # MGU-K ao lado do cárter, lado direito
SHOTS = {
    'energy-store': ((0.0, 0.22, -0.32), 0.30, (.8, .8, .9)),
    'mgu-k': ((0.27, 0.32, -0.93), 0.20, (1, .5, .6)),
    'inversor': ((0.33, 0.27, -0.55), 0.18, (1, .8, .9)),
}

def build(ctx):
    m = ctx.m
    # Energy store: caixa de carbono com tampa removível, módulos de células, barramentos e contator
    cube(ctx, 'Energy store · caixa estrutural', ES, ES_SIZE, m.carbon_matte, bev=.008, uv=10)
    cube(ctx, 'Energy store · tampa', (ES[0], ES[1] + ES_SIZE[1] / 2 + .004, ES[2]), (ES_SIZE[0] + .01, .008, ES_SIZE[2] + .01), m.carbon, bev=.003, uv=10, hide_group='es_lid')
    bolt_ring(ctx, 'Parafusos da tampa do energy store', (ES[0], ES[1] + ES_SIZE[1] / 2 + .008, ES[2]), .16, 8, UP, m.steel, size=.005, head=.003)
    for i in range(7):
        for j in range(2):
            x = -.18 + i * .06; z = ES[2] - .07 + j * .14
            cube(ctx, f'Módulo de células {i + 1}{"A" if j == 0 else "B"}', (x, ES[1] + .005, z), (.05, .09, .12), m.anod_black, bev=.003)
            cube(ctx, f'Terminal do módulo {i + 1}{"A" if j == 0 else "B"}', (x, ES[1] + .055, z), (.012, .01, .012), m.copper, bev=.001)
    for j in range(2):
        cube(ctx, f'Barramento de cobre {j + 1}', (0, ES[1] + .062, ES[2] - .07 + j * .14), (.40, .004, .016), m.copper, bev=.001)
    cube(ctx, 'Contator de alta tensão', (.16, ES[1] + .07, ES[2]), (.04, .03, .05), m.plastic_grey, bev=.002)
    cube(ctx, 'Unidade de monitoramento das células', (-.16, ES[1] + .066, ES[2]), (.06, .012, .08), m.pcb, bev=.001)
    cube(ctx, 'Placa fria do energy store', (ES[0], ES[1] - ES_SIZE[1] / 2 - .004, ES[2]), (ES_SIZE[0], .008, ES_SIZE[2]), m.alu, bev=.002)
    cube(ctx, 'Conector de alta tensão do energy store', (0.20, ES[1], ES[2] - .16), (.04, .05, .03), m.hv, bev=.003)
    text_plate(ctx, 'Etiqueta de alta tensão', 'HV 800 V', (0.0, ES[1] + .012, ES[2] + ES_SIZE[2] / 2 + .002), .016, m.anod_red, normal=FWD, up=UP)
    # Eletrônica de controle / inversor: caixa aletada com conectores trifásicos e refrigeração
    cube(ctx, 'Eletrônica de controle · inversor', CE, (.18, .09, .26), m.alu_cast, bev=.006, uv=8)
    for k in range(9):
        cube(ctx, 'Aleta do inversor', (CE[0] + .095, CE[1], CE[2] - .10 + k * .025), (.012, .08, .004), m.alu, bev=.0005)
    for k, lab in enumerate(('MGU-K', 'MGU-H', 'energy store')):
        cube(ctx, f'Conector de alta tensão · {lab}', (CE[0] - .04 + k * .04, CE[1] + .055, CE[2] + .10), (.03, .03, .03), m.hv, bev=.002)
    cube(ctx, 'Conector de dados do inversor', (CE[0], CE[1] + .05, CE[2] - .11), (.03, .02, .02), m.plastic_black, bev=.001)
    cube(ctx, 'Conversor DC-DC 12 V', (CE[0] - .02, CE[1] - .06, CE[2]), (.12, .03, .14), m.anod_black, bev=.003)
    # MGU-K: carcaça com camisa de arrefecimento, engrenagem de acionamento no virabrequim, resolver
    lathe(ctx, 'MGU-K · carcaça', [(.016, -.11), (.052, -.11), (.056, -.10), (.056, .10), (.052, .11), (.016, .11), (.016, -.11)], m.anod_black, center=MGUK, axis=FWD, segments=40)
    for k in range(10):
        cyl(ctx, 'Aleta da camisa de arrefecimento do MGU-K', (MGUK[0], MGUK[1], MGUK[2] - .09 + k * .02), .061, .003, m.anod_black, axis=FWD, verts=40)
    cyl(ctx, 'Rotor do MGU-K', MGUK, .024, .23, m.copper, axis=FWD, verts=24, spin=6.0)
    gear(ctx, 'Engrenagem de acionamento do MGU-K', (MGUK[0], MGUK[1], MGUK[2] + .135), 22, .0038, .014, m.gear, axis=FWD, bore=.012, spin=6.0)
    gear(ctx, 'Engrenagem intermediária · virabrequim → MGU-K', (MGUK[0] - .092, MGUK[1] + .04, MGUK[2] + .135), 26, .0038, .014, m.gear, axis=FWD, bore=.010, spin=-6.0 * 22 / 26)
    cube(ctx, 'Carcaça do trem de engrenagens do MGU-K', (MGUK[0] - .05, MGUK[1] + .02, MGUK[2] + .15), (.20, .14, .014), m.alu_cast, bev=.004)
    cube(ctx, 'Conector trifásico do MGU-K', (MGUK[0] + .04, MGUK[1] + .055, MGUK[2] - .04), (.04, .03, .05), m.hv, bev=.003)
    cyl(ctx, 'Resolver de posição do MGU-K', (MGUK[0], MGUK[1], MGUK[2] - .125), .018, .02, m.plastic_black, axis=FWD, verts=16)
    text_plate(ctx, 'Etiqueta do MGU-K', 'MGU-K 120 kW', (MGUK[0] + .057, MGUK[1], MGUK[2]), .013, m.alu_bright, normal=RIGHT, up=UP)
    # Cabos de alta tensão (laranja, blindados) e fluxos de energia
    es_ce = [(0.20, ES[1], ES[2] - .18), (.28, .22, -.44), (CE[0] + .04, CE[1] + .07, CE[2] + .10)]
    ce_mguk = [(CE[0] - .04, CE[1] + .07, CE[2] + .10), (CE[0] - .02, CE[1] + .12, CE[2] - .15), (MGUK[0] + .04, MGUK[1] + .08, MGUK[2] - .04)]
    ce_mguh = [(CE[0], CE[1] + .07, CE[2] + .10), (.22, .50, -.60), (.06, .66, -.80), (.04, .64, -.93)]
    for pts, lab in ((es_ce, 'energy store ↔ inversor'), (ce_mguk, 'inversor ↔ MGU-K')):
        for k in range(3):
            off = (k - 1) * .011
            sweep(ctx, f'Cabo de alta tensão {k + 1} · {lab}', [(p[0], p[1] + off, p[2]) for p in pts], m.hv, radius=.006, sides=10, carrier=True)
    for k in range(3):
        off = (k - 1) * .011
        sweep(ctx, f'Cabo de alta tensão {k + 1} · inversor ↔ MGU-H (2021)', [(p[0] + off, p[1], p[2]) for p in ce_mguh], m.hv, radius=.005, sides=10, era='2021', carrier=True)
    flow_ribbon(ctx, 'Recuperação · MGU-K → inversor → energy store', list(reversed(ce_mguk)) + list(reversed(es_ce)), 'hv', radius=.004)
    flow_ribbon(ctx, 'Entrega · energy store → inversor → MGU-K', [(p[0], p[1] - .02, p[2]) for p in es_ce + ce_mguk], 'hv', radius=.004, tag='reverse')
    flow_ribbon(ctx, 'Recuperação térmica · MGU-H → inversor (2021)', list(reversed(ce_mguh)), 'hv', radius=.004, era='2021')
    # Luz de estado ERS no santo antônio (obrigatória: verde seguro / vermelho HV ativo)
    cube(ctx, 'Luz de estado do sistema elétrico', (0, 1.12, -.52), (.03, .02, .012), m.led_green)
