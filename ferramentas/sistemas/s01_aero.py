"""01 · Aerodinâmica: o que a carroceria esconde — túneis venturi do assoalho, cercas de borda,
palhetas do difusor, asa de viga (beam wing), atuador hidráulico do DRS, defletores laterais
(bargeboards), ajustadores do flap dianteiro e trajetórias de fluxo (fitas animadas no site).
As asas e o assoalho externos permanecem no carro v2.
"""
import math
from lib import *

SYSTEM = ('aero', 'Aerodinâmica')

SHOTS = {
    'assoalho-por-baixo': ((0.0, 0.15, -0.9), 1.3, (.6, -1, .4)),
    'difusor': ((0.0, 0.25, -2.3), 0.55, (.8, .35, -1)),
    'drs': ((0.0, 0.82, -2.30), 0.40, (.7, .5, -1)),
    'bargeboards': ((0.48, 0.28, 0.65), 0.35, (1, .4, .8)),
}

def build(ctx):
    m = ctx.m
    # Túneis venturi sob o assoalho: garganta atrás da roda dianteira, expansão até o difusor
    for side in (-1, 1):
        lab = 'esquerdo' if side < 0 else 'direito'
        secs = []
        for z, w, h, xc, y0 in ((0.95, .28, .05, .40, .075), (0.40, .30, .09, .44, .075), (-0.60, .32, .07, .46, .075), (-1.40, .34, .09, .46, .075), (-1.95, .36, .16, .46, .075), (-2.45, .42, .32, .44, .075)):
            # teto do túnel: meia superelipse (de uma borda à outra passando pelo topo)
            pts = []
            for i in range(17):
                a = math.pi * i / 16
                c, s = math.cos(a), math.sin(a)
                px = math.copysign(abs(c) ** (2 / 2.2), c) * w / 2
                py = abs(s) ** (2 / 2.2) * h
                pts.append((side * (xc + px), y0 + py, z))
            secs.append(pts)
        shell(ctx, f'Túnel venturi {lab} · teto do assoalho', secs, m.carbon_matte, thickness=.005, open_ring=True)
        # cerca de borda (edge wing) e vórtice de selagem
        sweep(ctx, f'Cerca de borda do assoalho {lab}', [(side * .82, .07, .90), (side * .84, .07, .20), (side * .85, .07, -.70), (side * .84, .07, -1.50)], m.carbon_matte,
              section=lambda t: rounded_rect(.006, .07 + .03 * t, .002), smooth_path=True)
        flow_ribbon(ctx, f'Vórtice de borda do assoalho {lab}', [(side * (.86 + .02 * math.sin(k * .9)), .06 + .03 + .03 * math.cos(k * .9), .9 - k * .16) for k in range(16)], 'air', radius=.006)
        # túneis: fluxo acelerado sob o carro
        flow_ribbon(ctx, f'Fluxo do túnel venturi {lab}', [(side * .44, .10, 1.0), (side * .46, .11, -.2), (side * .46, .12, -1.4), (side * .44, .20, -2.1), (side * .40, .38, -2.6)], 'air', radius=.008)
    # Difusor: palhetas verticais (strakes) e borda de saída
    for x in (-.52, -.32, -.12, .12, .32, .52):
        secs = [[(x + px, .10 + py, -1.90) for px, py in rounded_rect(.006, .06, .002)], [(x + px, .18 + py, -2.15) for px, py in rounded_rect(.006, .16, .002)], [(x + px, .28 + py, -2.48) for px, py in rounded_rect(.006, .30, .002)]]
        loft(ctx, f'Palheta do difusor x={x:+.2f}', secs, m.carbon_matte)
    sweep(ctx, 'Gurney do difusor', [(-.65, .43, -2.52), (0, .44, -2.53), (.65, .43, -2.52)], m.carbon_matte, section=lambda t: rounded_rect(.004, .03, .001), smooth_path=True)
    # Asa de viga (beam wing) em dois elementos sob a asa traseira
    for y, z, chord, lab in ((.46, -2.32, .09, 'inferior'), (.53, -2.26, .07, 'superior')):
        secs = [[(x, y + py * 1.0, z + px) for px, py in airfoil(chord, .12, .06, 12)] for x in (-.36, -.18, 0, .18, .36)]
        loft(ctx, f'Beam wing · elemento {lab}', secs, m.carbon)
    # DRS: atuador hidráulico central, balancim, hastes até os pivôs do flap e linha hidráulica
    cyl(ctx, 'Atuador hidráulico do DRS', (0, .87, -2.25), .020, .09, m.anod_black, axis=(0, .3, -1), verts=24)
    cyl(ctx, 'Haste do atuador do DRS', (0, .885, -2.31), .006, .06, m.alu_bright, axis=(0, .3, -1), verts=12)
    cube(ctx, 'Balancim do DRS', (0, .90, -2.34), (.05, .012, .05), m.alu, bev=.002)
    for side in (-1, 1):
        sweep(ctx, f'Haste de comando do flap {"esquerda" if side < 0 else "direita"}', [(side * .02, .90, -2.34), (side * .30, .86, -2.32), (side * .58, .83, -2.30)], m.alu_bright, radius=.005, sides=10)
        sphere(ctx, f'Pivô do flap DRS {"esquerdo" if side < 0 else "direito"}', (side * .59, .82, -2.30), .012, m.titanium)
    hyd = [(0, .86, -2.20), (0, .80, -2.05), (0, .62, -1.90), (-.06, .40, -1.70)]
    sweep(ctx, 'Linha hidráulica do DRS', hyd, m.braid, radius=.004, sides=10, uv_len=30, carrier=True)
    flow_ribbon(ctx, 'Pressão hidráulica → DRS', hyd, 'hyd', radius=.0015)
    flow_ribbon(ctx, 'Fluxo sobre a asa traseira · DRS fechado', [(0, .70, -1.80), (0, .78, -2.10), (0, .86, -2.30), (0, .78, -2.60), (0, .70, -2.95)], 'air', radius=.008)
    # Defletores laterais (bargeboards) à frente dos sidepods
    for side in (-1, 1):
        lab = 'esquerdo' if side < 0 else 'direito'
        for k, (x, z0, z1, h) in enumerate(((.46, .92, .55, .30), (.56, .80, .50, .22), (.66, .72, .48, .16))):
            secs = []
            for t in (0, .5, 1):
                z = z0 + (z1 - z0) * t
                xx = x + .04 * math.sin(math.pi * t)
                secs.append([(side * (xx + px * .2), .10 + h / 2 + py * (h / 2) * (1 - .3 * t), z) for px, py in rounded_rect(.03, 2, .01)])
            loft(ctx, f'Defletor lateral {k + 1} {lab}', secs, m.carbon)
        flow_ribbon(ctx, f'Fluxo dos defletores → lateral do assoalho {lab}', [(side * .36, .28, 1.2), (side * .50, .22, .70), (side * .68, .16, .30), (side * .80, .12, -.2)], 'air', radius=.007)
    # Ajustadores do flap dianteiro e fluxo Y250
    for side in (-1, 1):
        cyl(ctx, f'Ajustador de incidência do flap dianteiro {"esquerdo" if side < 0 else "direito"}', (side * .56, .30, 2.16), .008, .05, m.alu, axis=UP, verts=12)
        cyl(ctx, f'Cabeça do ajustador {"esquerdo" if side < 0 else "direito"}', (side * .56, .33, 2.16), .012, .01, m.anod_red, axis=UP, verts=12, bev=.001)
        vortex = [(side * (.25 + .05 * math.cos(k * .8)), .30 + .05 * math.sin(k * .8), 2.2 - k * .17) for k in range(20)]
        flow_ribbon(ctx, f'Vórtice Y250 {"esquerdo" if side < 0 else "direito"}', vortex, 'air', radius=.006)
    # Fluxo externo principal: nariz → cockpit → tomada de ar → asa traseira
    flow_ribbon(ctx, 'Fluxo externo · eixo central', [(0, .40, 2.9), (0, .52, 1.6), (0, .80, .6), (0, 1.05, -.30), (0, 1.02, -1.2), (0, .95, -2.3), (0, .92, -3.0)], 'air', radius=.009)
    for side in (-1, 1):
        flow_ribbon(ctx, f'Fluxo externo · sidepod {"esquerdo" if side < 0 else "direito"}', [(side * .55, .45, 1.2), (side * .60, .48, .40), (side * .58, .52, -.60), (side * .40, .60, -1.60), (side * .30, .70, -2.3)], 'air', radius=.009)
