"""11 · Segurança: Halo em titânio com pilar central, estrutura principal de capotamento dentro
do airbox, cone de impacto dianteiro, estrutura de impacto traseira, tubos anti-intrusão laterais,
três cabos de retenção de roda por canto, encosto de cabeça removível, extintor e chaves externas.
"""
import math
from lib import *
from s03_suspension import PICKUPS

SYSTEM = ('safety', 'Segurança')

SHOTS = {
    'halo': ((0.0, 0.85, 0.45), 0.55, (1, .5, .9)),
    'impacto-dianteiro': ((0.0, 0.30, 2.15), 0.45, (1, .4, 1)),
    'impacto-traseiro': ((0.0, 0.35, -2.25), 0.40, (1, .4, -1)),
    'retencao-roda': ((0.45, 0.35, 1.52), 0.35, (1, .5, .8)),
}

def build(ctx):
    m = ctx.m
    # Halo: arco em titânio Ti-6Al-4V com pilar central em V e fixações traseiras
    arc = [(-.33, .68, -.05), (-.37, .84, .28), (-.28, .93, .66), (-.10, .95, .88), (0, .95, .92), (.10, .95, .88), (.28, .93, .66), (.37, .84, .28), (.33, .68, -.05)]
    sweep(ctx, 'Halo · arco principal', arc, m.titanium, radius=.030, sides=20, per_segment=10, uv_len=6)
    sweep(ctx, 'Halo · pilar central', [(0, .60, .93), (0, .78, .93), (0, .93, .92)], m.titanium, section=lambda t: airfoil(.070 - .02 * t, .40, 0, 12), smooth_path=True)
    for side in (-1, 1):
        cube(ctx, f'Fixação traseira do Halo {"esquerda" if side < 0 else "direita"}', (side * .33, .655, -.05), (.06, .03, .08), m.titanium, bev=.004)
        bolt_ring(ctx, f'Parafusos da fixação do Halo {"esquerda" if side < 0 else "direita"}', (side * .33, .672, -.05), .02, 2, UP, m.steel, size=.005, head=.004)
    cube(ctx, 'Fixação dianteira do Halo', (0, .59, .93), (.07, .03, .06), m.titanium, bev=.004)
    # Estrutura principal de capotamento dentro do airbox (aço/titânio) com escora diagonal
    hoop = [(-.15, .72, -.44), (-.14, .95, -.42), (-.06, 1.12, -.40), (.06, 1.12, -.40), (.14, .95, -.42), (.15, .72, -.44)]
    sweep(ctx, 'Estrutura principal de capotamento', hoop, m.titanium_blue, radius=.020, sides=16, per_segment=10)
    sweep(ctx, 'Escora da estrutura de capotamento', [(0, 1.10, -.41), (0, .90, -.62), (0, .76, -.72)], m.titanium_blue, radius=.014, sides=14, smooth_path=False)
    for side in (-1, 1):
        cube(ctx, f'Base da estrutura de capotamento {"esquerda" if side < 0 else "direita"}', (side * .15, .71, -.44), (.06, .02, .06), m.titanium, bev=.003)
    # Cone de impacto dianteiro (estrutura interna do nariz destacável) com anteparas de colapso progressivo
    secs = []
    for z, w, h, yc in ((1.82, .34, .22, .30), (2.05, .26, .18, .28), (2.28, .18, .13, .26), (2.50, .10, .08, .24)):
        secs.append([(px, yc + py, z) for px, py in super_ellipse(w, h, 2.6, 28)])
    shell(ctx, 'Cone de impacto dianteiro · laminado', secs, m.carbon_matte, thickness=.008)
    for z, w, h, yc in ((1.98, .28, .19, .285), (2.18, .21, .15, .27), (2.38, .13, .10, .25)):
        loft(ctx, f'Antepara de colapso z={z:.2f}', [[(px, yc + py, z - .004) for px, py in super_ellipse(w, h, 2.6, 24)], [(px, yc + py, z + .004) for px, py in super_ellipse(w, h, 2.6, 24)]], m.honeycomb)
    # Estrutura de impacto traseira atrás do câmbio, com a luz de chuva na extremidade
    secs = []
    for z, w, h, yc in ((-2.0, .26, .30, .36), (-2.20, .20, .24, .35), (-2.40, .14, .16, .34), (-2.53, .09, .10, .34)):
        secs.append([(px, yc + py, z) for px, py in super_ellipse(w, h, 2.6, 28)])
    shell(ctx, 'Estrutura de impacto traseira', secs, m.carbon_matte, thickness=.008)
    loft(ctx, 'Antepara de colapso traseira', [[(px, .35 + py, -2.24) for px, py in super_ellipse(.19, .23, 2.6, 24)], [(px, .35 + py, -2.232) for px, py in super_ellipse(.19, .23, 2.6, 24)]], m.honeycomb)
    # Tubos anti-intrusão laterais (SIS): dois por lado, cônicos, do costado da célula à pele do sidepod
    for side in (-1, 1):
        lab = 'esquerdo' if side < 0 else 'direito'
        for k, (z, y) in enumerate(((.30, .40), (-.30, .36))):
            sweep(ctx, f'Tubo anti-intrusão lateral {k + 1} {lab}', [(side * .30, y, z), (side * .66, y - .02, z - .05)], m.carbon_matte, radius=.045, radii=[.045, .028], sides=20, smooth_path=False)
            cube(ctx, f'Flange do tubo anti-intrusão {k + 1} {lab}', (side * .31, y, z), (.012, .12, .12), m.titanium, bev=.002)
    # Cabos de retenção de roda (Zylon): três por canto, ao longo das pernas dos wishbones e do push/pull-rod
    for axle, front in (('front', True), ('rear', False)):
        P = PICKUPS[axle]
        for side in (-1, 1):
            lab = f'{"dianteiro" if front else "traseiro"} {"esquerdo" if side < 0 else "direito"}'
            routes = [(P['uwo'], P['uwi_f']), (P['lwo'], P['lwi_a']), (P['pro'], P['rocker_arm'])]
            for k, (a, b) in enumerate(routes):
                a2 = (side * a[0], a[1] + .02, a[2]); b2 = (side * b[0], b[1] + .02, b[2])
                sweep(ctx, f'Cabo de retenção {k + 1} {lab}', [a2, b2], m.zylon, radius=.004, sides=8, smooth_path=False)
                sphere(ctx, f'Terminal do cabo de retenção {k + 1} {lab}', b2, .008, m.steel)
    # Encosto de cabeça removível em espuma de absorção (Confor) com revestimento Nomex
    head = [(-.24, .66, .20), (-.26, .68, .05), (-.16, .70, -.08), (0, .71, -.10), (.16, .70, -.08), (.26, .68, .05), (.24, .66, .20)]
    sweep(ctx, 'Encosto de cabeça removível', head, m.nomex, section=lambda t: rounded_rect(.09, .11, .025), smooth_path=True)
    for side in (-1, 1):
        sweep(ctx, f'Apoio lateral do encosto {"esquerdo" if side < 0 else "direito"}', [(side * .25, .66, .20), (side * .23, .64, .42)], m.nomex, section=lambda t: rounded_rect(.07, .10, .02), smooth_path=False)
    cube(ctx, 'Pino de retenção do encosto', (0, .77, -.10), (.02, .02, .03), m.anod_red, bev=.002)
    # Extintor sob as pernas do piloto, chaves externas de corte e extintor
    lathe(ctx, 'Extintor · garrafa', [(0, -.13), (.05, -.13), (.056, -.11), (.056, .10), (.048, .125), (.02, .13), (0, .13)], m.paint_red, center=(0, .22, .62), axis=FWD, segments=32)
    cyl(ctx, 'Válvula do extintor', (0, .22, .765), .022, .03, m.alu, axis=FWD, verts=20)
    sweep(ctx, 'Bico do extintor · cockpit', [(0, .24, .78), (.10, .32, .60), (.18, .40, .40)], m.braid, radius=.004, sides=10)
    sweep(ctx, 'Bico do extintor · compartimento do motor', [(0, .22, .49), (-.10, .24, .0), (-.20, .40, -.60), (-.20, .50, -.90)], m.braid, radius=.004, sides=10)
    cyl(ctx, 'Chave externa · corte geral (E)', (.22, .76, -.30), .012, .03, m.anod_red, axis=UP, verts=12)
    cyl(ctx, 'Chave externa · extintor', (.16, .76, -.30), .012, .03, m.anod_red, axis=UP, verts=12)
    text_plate(ctx, 'Marcação de corte geral', 'E', (.22, .78, -.30), .02, m.paint_white, normal=UP, up=FWD)
    # Luz de chuva LED na estrutura traseira e luzes de estado ERS
    cube(ctx, 'Luz de chuva LED', (0, .34, -2.545), (.06, .10, .012), m.led_red)
