"""04 · Direção: coluna em carbono com juntas universais, pinhão e cremalheira hidráulica
transversal na antepara dianteira, barras de direção em perfil de asa até os uprights,
servo hidráulico e linhas de assistência.
"""
import math
from lib import *
from s03_suspension import PICKUPS

SYSTEM = ('steering', 'Direção')

RACK = (0.0, 0.340, 1.360)      # centro da caixa da cremalheira
HUB = (0.0, 0.620, 0.52)        # cubo do volante do carro v2
SHOTS = {
    'cremalheira': ((0.0, 0.34, 1.36), 0.34, (.9, .55, .8)),
    'coluna': ((0.0, 0.52, 0.85), 0.36, (1, .35, .4)),
    'track-rod': ((0.45, 0.35, 1.40), 0.22, (.6, .5, .9)),
}

def build(ctx):
    m = ctx.m
    P = PICKUPS['front']
    # Caixa da cremalheira em alumínio usinado, fixada à antepara, com coifas de borracha
    lathe(ctx, 'Caixa da cremalheira', [(.0, -.20), (.024, -.20), (.024, -.09), (.030, -.09), (.030, .09), (.024, .09), (.024, .20), (.0, .20)], m.alu, center=RACK, axis=RIGHT, segments=32)
    cube(ctx, 'Flange de fixação da cremalheira', (0, RACK[1] - .01, RACK[2] - .02), (.11, .05, .012), m.alu, bev=.002)
    bolt_ring(ctx, 'Parafusos da cremalheira', (0, RACK[1] - .01, RACK[2] - .027), .04, 4, (0, 0, -1), m.steel, size=.005, head=.003, start=math.pi / 4)
    for side in (-1, 1):
        # coifas sanfonadas e pontas da cremalheira (aço) até as rótulas
        helix(ctx, f'Coifa da cremalheira {"esquerda" if side < 0 else "direita"}', (side * .225, RACK[1], RACK[2]), .022, .012, 4, .004, m.rubber, axis=RIGHT, per_turn=20)
        sweep(ctx, f'Ponta da cremalheira {"esquerda" if side < 0 else "direita"}', [(side * .20, RACK[1], RACK[2]), (side * P['rack_end'][0], P['rack_end'][1], P['rack_end'][2])], m.steel, radius=.010, sides=16, smooth_path=False)
        sphere(ctx, f'Rótula interna da barra de direção {"esquerda" if side < 0 else "direita"}', (side * P['rack_end'][0], P['rack_end'][1], P['rack_end'][2]), .011, m.titanium)
        # barra de direção (track rod) em perfil de asa até o braço do upright
        sweep(ctx, f'Barra de direção · track rod {"esquerda" if side < 0 else "direita"}', [(side * P['rack_end'][0], P['rack_end'][1], P['rack_end'][2]), (side * P['tro'][0], P['tro'][1], P['tro'][2])], m.carbon_fine,
              section=lambda t: airfoil(.040, .36, 0, 12), smooth_path=False)
        sphere(ctx, f'Rótula externa da barra de direção {"esquerda" if side < 0 else "direita"}', (side * P['tro'][0], P['tro'][1], P['tro'][2]), .010, m.titanium)
    # Pinhão e carcaça do pinhão (entrada da coluna, deslocada para a esquerda)
    pin = (-.045, RACK[1] + .028, RACK[2] - .018)
    gear(ctx, 'Pinhão da direção', pin, 9, .0045, .022, m.gear, axis=(0, .55, -.85), spin=0)
    cyl(ctx, 'Carcaça do pinhão', (pin[0], pin[1] + .012, pin[2] - .018), .020, .05, m.alu, axis=(0, .55, -.85), verts=24)
    # Servo hidráulico da direção assistida: válvula rotativa e cilindro de assistência sobre a cremalheira
    cyl(ctx, 'Válvula rotativa da assistência hidráulica', (pin[0], pin[1] + .04, pin[2] - .045), .017, .04, m.alu_cast, axis=(0, .55, -.85), verts=24)
    cyl(ctx, 'Cilindro de assistência hidráulica', (.06, RACK[1] + .012, RACK[2] + .036), .015, .14, m.anod_black, axis=RIGHT, verts=20)
    for i, (dx, lab) in enumerate(((-.05, 'pressão'), (.05, 'retorno'))):
        cyl(ctx, f'Conexão hidráulica · {lab}', (.06 + dx, RACK[1] + .03, RACK[2] + .036), .006, .02, m.anod_blue, axis=UP, verts=10)
        pts = [(.06 + dx, RACK[1] + .04, RACK[2] + .036), (.10 + i * .02, RACK[1] + .06, 1.20), (.16, .38, .60), (.20, .34, .0), (.24, .40, -.55)]
        sweep(ctx, f'Linha hidráulica da direção · {lab}', pts, m.braid, radius=.004, sides=10, uv_len=40, carrier=True)
        flow_ribbon(ctx, f'Fluido hidráulico · {lab}', pts, 'hyd', radius=.0015)
    # Coluna: dois tubos de carbono, duas juntas universais e mancal na antepara do painel
    j1 = (0, .47, .98); j2 = (pin[0], pin[1] + .03, pin[2] - .07)
    sweep(ctx, 'Coluna de direção · tubo superior', [HUB, (0, .56, .72), j1], m.carbon_fine, radius=.016, sides=20, uv_len=6, carrier=True)
    sweep(ctx, 'Coluna de direção · tubo inferior', [j1, j2], m.carbon_fine, radius=.013, sides=20, smooth_path=False, uv_len=6, carrier=True)
    for i, j in enumerate((j1, j2)):
        sphere(ctx, f'Junta universal {i + 1}', j, .019, m.steel, scale=(1, 1, 1.25))
        cyl(ctx, f'Cruzeta da junta universal {i + 1}', j, .0045, .046, m.steel_dark, axis=RIGHT, verts=10)
    cyl(ctx, 'Mancal da coluna na antepara', (0, .49, .90), .030, .014, m.alu, axis=(0, .5, 1), verts=24)
    cube(ctx, 'Suporte do mancal da coluna', (0, .47, .90), (.09, .012, .06), m.carbon_matte, bev=.001)
    cyl(ctx, 'Eixo estriado do engate rápido', (0, .618, .49), .012, .05, m.steel, axis=(0, .12, 1), verts=18)
    cyl(ctx, 'Sensor de ângulo de direção', (0, .52, .82), .014, .02, m.plastic_black, axis=(0, .5, 1), verts=16)
    # Fluxo do movimento (didático): do volante à cremalheira
    flow_ribbon(ctx, 'Comando do piloto · volante → cremalheira', [HUB, (0, .56, .72), j1, j2, pin], 'data', radius=.004)
