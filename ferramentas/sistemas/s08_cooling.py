"""08 · Refrigeração assimétrica: intercooler ar-ar inclinado no sidepod esquerdo com o
arrefecedor de óleo do câmbio/hidráulica; radiador de água, arrefecedor de óleo do motor e
arrefecedor de baixa temperatura do ERS no sidepod direito. Tanques, mangueiras de silicone,
abraçadeiras, bocas dos sidepods e fluxos por circuito.
"""
import math
from lib import *

SYSTEM = ('cooling', 'Refrigeração')

SHOTS = {
    'sidepod-esquerdo': ((-0.52, 0.36, -0.25), 0.42, (-1, .5, .5)),
    'sidepod-direito': ((0.52, 0.36, -0.25), 0.42, (1, .5, .5)),
    'superior': ((0.0, 0.40, -0.35), 0.80, (.001, 1, .2)),
}

def core(ctx, name, center, size, tilt_deg, mat_tank):
    """Núcleo de trocador com aletas, tanques superior/inferior e tirantes; inclinado em torno do eixo longitudinal."""
    m = ctx.m
    w, h, d = size   # espessura (x), altura (y), comprimento (z)
    rot = (0, 0, tilt_deg)
    parts = [cube(ctx, f'{name} · núcleo aletado', center, (w, h, d), m.radiator, rot=rot, bev=.002, uv=1)]
    a = math.radians(tilt_deg)
    # deslocamento ao longo do eixo inclinado (para cima do núcleo): rotação de (0,1,0) por tilt em torno de Z
    up = (-math.sin(a), math.cos(a), 0)
    for s, lab in ((1, 'superior'), (-1, 'inferior')):
        c = (center[0] + up[0] * s * (h / 2 + .022), center[1] + up[1] * s * (h / 2 + .022), center[2])
        parts.append(cube(ctx, f'{name} · tanque {lab}', c, (w + .02, .044, d + .01), mat_tank, rot=rot, bev=.008, uv=6))
    for zz in (-d / 2 + .04, d / 2 - .04):
        parts.append(cube(ctx, f'{name} · moldura lateral', (center[0], center[1], center[2] + zz), (w + .004, h + .02, .012), m.carbon_matte, rot=rot, bev=.001))
    return parts, up

def hose(ctx, name, pts, kind, r=.016):
    m = ctx.m
    sweep(ctx, name, pts, m.silicone_black, radius=r, sides=16, uv_len=8, carrier=True)
    for p in (pts[0], pts[-1]):
        torus(ctx, f'Abraçadeira · {name}', p, r + .002, .003, m.anod_blue, axis=(0, 0, 1), seg=24, mseg=6)
    flow_ribbon(ctx, f'Fluxo · {name}', pts, kind, radius=r * .35)

def build(ctx):
    m = ctx.m
    # bocas dos sidepods (molduras de carbono)
    for side in (-1, 1):
        lab = 'esquerdo' if side < 0 else 'direito'
        loft(ctx, f'Boca do sidepod {lab}', [[(side * .56 + px, .40 + py, .42) for px, py in super_ellipse(.30, .20, 2.8, 32)], [(side * .56 + px * 1.06, .40 + py * 1.06, .38) for px, py in super_ellipse(.30, .20, 2.8, 32)]], m.carbon_matte, cap=False)
    # ---- sidepod esquerdo: intercooler ar-ar inclinado 40° + arrefecedor óleo do câmbio / hidráulica
    ic_parts, ic_up = core(ctx, 'Intercooler ar-ar', (-.50, .37, -.30), (.075, .34, .52), 40, m.alu)
    cube(ctx, 'Intercooler · entrada de ar comprimido', (-.40, .50, -.20), (.06, .06, .06), m.alu, bev=.006)
    cube(ctx, 'Intercooler · saída de ar resfriado', (-.40, .55, -.75), (.06, .06, .06), m.alu, bev=.006)
    core(ctx, 'Arrefecedor de óleo do câmbio e hidráulica', (-.55, .30, .12), (.05, .22, .24), 30, m.alu)
    hose(ctx, 'Óleo do câmbio · câmbio → arrefecedor', [(.155, .29, -1.56), (.0, .24, -1.30), (-.36, .22, -.60), (-.52, .26, .0)], 'oil', .010)
    hose(ctx, 'Óleo do câmbio · retorno', [(-.58, .40, .0), (-.40, .30, -.70), (-.06, .22, -1.40), (.155, .25, -1.56)], 'oil', .010)
    hose(ctx, 'Hidráulica · bomba → arrefecedor', [(-.20, .50, -.60), (-.46, .44, -.10), (-.56, .42, .05)], 'hyd', .009)
    # ---- sidepod direito: radiador de água + arrefecedor de óleo do motor + arrefecedor ERS (baixa temperatura)
    core(ctx, 'Radiador de água do motor', (.50, .37, -.28), (.06, .36, .56), -36, m.alu)
    core(ctx, 'Arrefecedor de óleo do motor', (.52, .30, -.82), (.05, .24, .28), -30, m.alu)
    core(ctx, 'Arrefecedor de baixa temperatura do ERS', (.56, .30, .14), (.05, .22, .26), -30, m.alu)
    # circuito de água: bomba (frente do motor) → cabeçotes → radiador → bomba
    hose(ctx, "Água · bomba → bloco/cabeçotes", [(.20, .40, -.585), (.26, .56, -.70), (.24, .62, -1.10)], 'water', .014)
    hose(ctx, 'Água · cabeçotes → radiador (quente)', [(.24, .64, -1.16), (.36, .62, -.90), (.50, .58, -.50), (.52, .60, -.30)], 'water', .016)
    hose(ctx, 'Água · radiador → bomba (fria)', [(.48, .16, -.30), (.42, .18, -.45), (.28, .30, -.56), (.20, .40, -.585)], 'water', .016)
    cyl(ctx, 'Tanque de expansão e desaeração', (.36, .66, -.20), .04, .12, m.alu, axis=UP, verts=28)
    cyl(ctx, 'Tampa pressurizada do tanque de expansão', (.36, .73, -.20), .022, .012, m.anod_red, axis=UP, verts=20)
    hose(ctx, 'Água · sangria para o tanque de expansão', [(.52, .60, -.30), (.42, .68, -.24), (.38, .70, -.20)], 'water', .006)
    # óleo do motor: reservatório → bomba → arrefecedor → reservatório
    hose(ctx, 'Óleo do motor · reservatório → arrefecedor', [(-.31, .31, -.58), (-.10, .24, -.62), (.30, .22, -.72), (.50, .20, -.84)], 'oil', .012)
    hose(ctx, 'Óleo do motor · arrefecedor → reservatório', [(.54, .42, -.82), (.30, .52, -.66), (-.10, .54, -.60), (-.28, .55, -.58)], 'oil', .012)
    # ERS: placa fria do energy store e inversor ↔ arrefecedor de baixa temperatura
    hose(ctx, 'ERS · placa fria e inversor → arrefecedor', [(.24, .16, -.32), (.40, .18, -.40), (.44, .22, -.10), (.56, .20, .10)], 'water', .009)
    hose(ctx, 'ERS · arrefecedor → inversor', [(.58, .40, .10), (.46, .38, -.20), (.36, .33, -.50), (.33, .32, -.55)], 'water', .009)
    # ar de arrefecimento atravessando os núcleos (fluxo didático) e saída pela traseira dos sidepods
    for side in (-1, 1):
        flow_ribbon(ctx, f'Ar de arrefecimento · boca → núcleo → saída {"esquerda" if side < 0 else "direita"}', [(side * .56, .40, .50), (side * .54, .38, .0), (side * .50, .40, -.40), (side * .40, .48, -1.0), (side * .30, .55, -1.5)], 'air', radius=.010)
