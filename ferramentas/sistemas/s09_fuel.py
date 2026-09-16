"""09 · Célula de combustível: bexiga flexível em Kevlar/nitrílica atrás do piloto, anteparas
internas com portinholas, copo coletor, bombas de elevação, medidor de vazão FIA, bomba de alta
pressão no motor, acoplamento de abastecimento, respiro e linhas seguras fora do cockpit.
"""
import math
from lib import *

SYSTEM = ('fuel', 'Célula de combustível')

ZC = -0.33
SHOTS = {
    'celula': ((0.0, 0.50, -0.33), 0.40, (1, .5, .7)),
    'interior': ((0.0, 0.45, -0.33), 0.30, (.9, .3, -.6)),
    'linhas': ((0.15, 0.50, -0.55), 0.30, (1, .6, .2)),
}

def bladder_sections():
    secs = []
    for y, w, d in ((.29, .56, .30), (.36, .60, .33), (.50, .60, .34), (.62, .54, .32), (.72, .38, .28), (.78, .20, .22)):
        secs.append([(px, y, ZC + py) for px, py in super_ellipse(w, d, 3.0, 28)])
    return secs

def build(ctx):
    m = ctx.m
    secs = bladder_sections()
    loft(ctx, 'Bexiga flexível · Kevlar/nitrílica', secs, m.fuel)
    # combustível (nível parcial) e espuma anti-oscilação nas bordas
    liquid = loft(ctx, 'Gasolina · nível de 55 %', [[(px * .96, y, ZC + py * .96) for px, py in sec_pts] for (y, sec_pts) in [(.30, super_ellipse(.56, .30, 3.0, 28)), (.36, super_ellipse(.60, .33, 3.0, 28)), (.50, super_ellipse(.60, .34, 3.0, 28)), (.56, super_ellipse(.58, .33, 3.0, 28))]], m.fuel_liquid, hide_group='fuel_liquid')
    # anteparas internas com portinholas unidirecionais
    for k, z in enumerate((ZC - .08, ZC, ZC + .08)):
        cube(ctx, f'Antepara interna {k + 1}', (0, .50, z), (.54, .40, .004), m.rubber, bev=.001)
        for x in (-.15, .15):
            cube(ctx, f'Portinhola unidirecional {k + 1}', (x, .34, z + .006), (.06, .05, .003), m.plastic_grey, bev=.0005)
    # copo coletor (swirl pot) e bombas de elevação nos cantos
    lathe(ctx, 'Copo coletor · swirl pot', [(0, -.06), (.048, -.06), (.052, -.05), (.052, .05), (.048, .06), (0, .06)], m.alu, center=(0, .35, ZC - .02), axis=UP, segments=32)
    for x in (-.22, .22):
        cyl(ctx, f'Bomba de elevação {"esquerda" if x < 0 else "direita"}', (x, .33, ZC + .02), .022, .07, m.anod_black, axis=UP, verts=24)
        sweep(ctx, f'Linha da bomba de elevação → coletor {"esquerda" if x < 0 else "direita"}', [(x, .37, ZC + .02), (x * .5, .40, ZC), (.04, .40, ZC - .02)], m.braid, radius=.006, sides=10, uv_len=20)
    cyl(ctx, 'Bomba do coletor · alimentação de baixa pressão', (0, .29, ZC - .12), .024, .06, m.anod_black, axis=FWD, verts=24)
    # placa de fixações no topo traseiro: saída, retorno, respiro, sensor de nível
    cube(ctx, 'Placa de conexões da célula', (0.10, .74, ZC - .10), (.16, .008, .10), m.alu, bev=.002)
    for dx, lab in ((-.05, 'saída de combustível'), (.0, 'retorno'), (.05, 'respiro com válvula anticapotamento')):
        cyl(ctx, f'Conexão · {lab}', (0.10 + dx, .755, ZC - .10), .009, .024, m.anod_blue, axis=UP, verts=12)
    cyl(ctx, 'Sensor de nível capacitivo', (.06, .55, ZC - .12), .006, .40, m.steel, axis=UP, verts=10)
    # medidor de vazão FIA, filtro e linha de alta pressão até a bomba HP no motor (fora do cockpit)
    cube(ctx, 'Medidor de vazão de combustível FIA', (.14, .60, -.52), (.05, .05, .09), m.anod_black, bev=.004)
    cyl(ctx, 'Filtro de combustível', (.10, .52, -.48), .018, .08, m.alu, axis=FWD, verts=20)
    feed = [(0.05, .77, ZC - .10), (.10, .74, -.46), (.12, .64, -.50), (.14, .60, -.56), (.18, .60, -.62), (.20, .60, -.66)]
    sweep(ctx, 'Linha de alimentação · célula → medidor → bomba HP', feed, m.braid, radius=.006, sides=12, uv_len=30, carrier=True)
    flow_ribbon(ctx, 'Combustível · alimentação', feed, 'fuel', radius=.0025)
    ret = [(.21, .62, -.68), (.16, .70, -.56), (.10, .78, -.44), (.10, .77, ZC - .10)]
    sweep(ctx, 'Linha de retorno de combustível', ret, m.braid, radius=.005, sides=12, uv_len=30, carrier=True)
    flow_ribbon(ctx, 'Combustível · retorno', ret, 'fuel', radius=.002)
    sweep(ctx, 'Linha da bomba de baixa pressão → medidor', [(0, .29, ZC - .16), (.08, .30, -.46), (.12, .45, -.50), (.14, .55, -.52)], m.braid, radius=.006, sides=12, uv_len=30)
    # acoplamento de abastecimento (lado direito) com tampa e válvula de segurança de desconexão
    cyl(ctx, 'Acoplamento de abastecimento', (.31, .60, ZC), .030, .04, m.alu, axis=RIGHT, verts=28)
    cyl(ctx, 'Tampa do acoplamento de abastecimento', (.335, .60, ZC), .034, .01, m.anod_red, axis=RIGHT, verts=28)
    cyl(ctx, 'Válvula de desconexão autosselante', (.24, .60, ZC), .018, .05, m.steel, axis=RIGHT, verts=20)
    sweep(ctx, 'Duto de abastecimento → célula', [(.29, .60, ZC), (.22, .62, ZC), (.15, .66, ZC)], m.rubber, radius=.020, sides=14)
    # cintas de retenção e cantoneiras de fixação à estrutura
    for z in (ZC - .10, ZC + .10):
        sweep(ctx, f'Cinta de retenção da célula {z:.2f}', [(-.30, .30, z), (-.31, .62, z), (-.16, .77, z), (.16, .77, z), (.31, .62, z), (.30, .30, z)], m.webbing, section=lambda t: rounded_rect(.030, .003, .001), smooth_path=True)
