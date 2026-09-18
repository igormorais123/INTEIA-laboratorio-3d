"""11 · Segurança: Halo e acolchoado do cockpit copiados da malha visível do carro v2 (coincidência exata),
estrutura principal de capotamento dentro do airbox, cone de impacto dianteiro dentro do envelope do nariz,
estrutura de impacto traseira, tubos anti-intrusão laterais, dois cabos de retenção de roda por canto,
extintor e chaves externas. Luz de chuva no mesmo lugar do LED traseiro do carro.
"""
import math
from lib import *
from s03_suspension import PICKUPS

X_CONVENTION = 'piloto'   # +X = esquerda do piloto (ver lib.lado)
SYSTEM = ('safety', 'Segurança')

SHOTS = {
    'halo': ((0.0, 0.78, 0.35), 0.55, (1, .5, .9)),
    'impacto-dianteiro': ((0.0, 0.35, 2.15), 0.45, (1, .4, 1)),
    'impacto-traseiro': ((0.0, 0.35, -2.25), 0.40, (1, .4, -1)),
    'retencao-roda': ((0.45, 0.35, 1.52), 0.35, (1, .5, .8)),
}

def build(ctx):
    m = ctx.m
    # Halo: a malha é a mesma do carro v2 (arco + pilar central), com acabamento de titânio Ti-6Al-4V.
    # Ilhas da carroceria com y > 0,66 e que chegam ao nariz (z > 0,85): arco externo e as duas metades internas.
    car_part(ctx, 'Halo · arco principal', m.titanium, box=((-.32, .66, -.30), (.32, .88, .95)),
             select=lambda c: c['max'][2] > .85 and c['n'] > 300)
    for side in (-1, 1):
        lab = lado(side, True)
        cube(ctx, f'Fixação traseira do Halo {lab}', (side * .276, .705, -.285), (.075, .025, .10), m.titanium, bev=.004)
        bolt_ring(ctx, f'Parafusos da fixação do Halo {lab}', (side * .276, .72, -.285), .026, 3, UP, m.steel, size=.005, head=.004)
    cube(ctx, 'Fixação dianteira do Halo', (0, .66, .82), (.10, .012, .24), m.titanium, bev=.003)
    bolt_ring(ctx, 'Parafusos da fixação dianteira do Halo', (0, .667, .82), .035, 4, UP, m.steel, size=.005, head=.003)
    # Estrutura principal de capotamento: arco no bocal do airbox (o ponto mais alto do carro, y ≈ 0,99)
    hoop = [(-.15, .70, -.24), (-.145, .86, -.235), (-.10, .955, -.23), (0, .985, -.23), (.10, .955, -.23), (.145, .86, -.235), (.15, .70, -.24)]
    sweep(ctx, 'Estrutura principal de capotamento', hoop, m.titanium_blue, radius=.022, sides=16, per_segment=10)
    sweep(ctx, 'Escora da estrutura de capotamento', [(0, .965, -.26), (0, .88, -.55), (0, .80, -.75)], m.titanium_blue, radius=.014, sides=14, smooth_path=False)
    for side in (-1, 1):
        cube(ctx, f'Base da estrutura de capotamento {lado(side, True)}', (side * .15, .69, -.24), (.06, .02, .06), m.titanium, bev=.003)
    # Cone de impacto dianteiro dentro do envelope do nariz do carro (topo y≈0,55 e fundo y≈0,26 em z=1,8)
    secs = []
    for z, w, h, yc in ((1.82, .26, .24, .41), (2.05, .22, .20, .37), (2.28, .18, .14, .30), (2.50, .10, .07, .21)):
        secs.append([(px, yc + py, z) for px, py in super_ellipse(w, h, 2.6, 28)])
    shell(ctx, 'Cone de impacto dianteiro · laminado', secs, m.carbon_matte, thickness=.008)
    for z, w, h, yc in ((1.98, .24, .21, .39), (2.18, .20, .16, .33), (2.38, .14, .10, .26)):
        loft(ctx, f'Antepara de colapso z={z:.2f}', [[(px, yc + py, z - .004) for px, py in super_ellipse(w, h, 2.6, 24)], [(px, yc + py, z + .004) for px, py in super_ellipse(w, h, 2.6, 24)]], m.honeycomb)
    # Estrutura de impacto traseira atrás do câmbio; a luz de chuva coincide com o LED traseiro do carro
    secs = []
    for z, w, h, yc in ((-2.0, .24, .24, .36), (-2.20, .19, .20, .355), (-2.40, .13, .14, .35), (-2.53, .08, .09, .345)):
        secs.append([(px, yc + py, z) for px, py in super_ellipse(w, h, 2.6, 28)])
    shell(ctx, 'Estrutura de impacto traseira', secs, m.carbon_matte, thickness=.008)
    loft(ctx, 'Antepara de colapso traseira', [[(px, .355 + py, -2.24) for px, py in super_ellipse(.18, .19, 2.6, 24)], [(px, .355 + py, -2.232) for px, py in super_ellipse(.18, .19, 2.6, 24)]], m.honeycomb)
    cube(ctx, 'Luz de chuva LED', (0, .315, -2.545), (.042, .11, .012), m.led_red)
    # Tubos anti-intrusão laterais (SIS): dois por lado, cônicos, do costado da célula à pele do sidepod
    for side in (-1, 1):
        lab = lado(side)
        for k, (z, y) in enumerate(((.30, .40), (-.30, .36))):
            sweep(ctx, f'Tubo anti-intrusão lateral {k + 1} {lab}', [(side * .30, y, z), (side * .66, y - .02, z - .05)], m.carbon_matte, radius=.045, radii=[.045, .028], sides=20, smooth_path=False)
            cube(ctx, f'Flange do tubo anti-intrusão {k + 1} {lab}', (side * .31, y, z), (.012, .12, .12), m.titanium, bev=.002)
    # Cabos de retenção de roda (Zylon): dois por canto desde 2011, em caminhos independentes pelos wishbones
    # superior e inferior, para que um segure a roda se o outro romper.
    for axle, front in (('front', True), ('rear', False)):
        P = PICKUPS[axle]
        for side in (-1, 1):
            lab = f'{"dianteiro" if front else "traseiro"} {lado(side)}'
            routes = [(P['uwo'], P['uwi_f']), (P['lwo'], P['lwi_a'])]
            for k, (a, b) in enumerate(routes):
                a2 = (side * a[0], a[1] + .02, a[2]); b2 = (side * b[0], b[1] + .02, b[2])
                sweep(ctx, f'Cabo de retenção {k + 1} {lab}', [a2, b2], m.zylon, radius=.004, sides=8, smooth_path=False)
                sphere(ctx, f'Terminal do cabo de retenção {k + 1} {lab}', b2, .008, m.steel)
    # Encosto de cabeça removível: a mesma peça em U do carro v2, em espuma Confor com revestimento Nomex
    car_part(ctx, 'Encosto de cabeça removível', m.nomex, box=((-.27, .72, -.17), (.27, .88, .43)), select=lambda c: c['n'] > 50, uv=4)
    for side in (-1, 1):
        cyl(ctx, f'Pino de retenção do encosto {lado(side)}', (side * .215, .84, .40), .006, .018, m.anod_red, axis=UP, verts=12)
    # Extintor sob as pernas do piloto, bicos para o cockpit e para o compartimento do motor, chaves externas
    lathe(ctx, 'Extintor · garrafa', [(0, -.13), (.05, -.13), (.056, -.11), (.056, .10), (.048, .125), (.02, .13), (0, .13)], m.paint_red, center=(0, .22, .62), axis=FWD, segments=32)
    cyl(ctx, 'Válvula do extintor', (0, .22, .765), .022, .03, m.alu, axis=FWD, verts=20)
    sweep(ctx, 'Bico do extintor · cockpit', [(0, .24, .78), (.10, .32, .60), (.18, .40, .40)], m.braid, radius=.004, sides=10)
    sweep(ctx, 'Bico do extintor · compartimento do motor', [(0, .22, .49), (-.10, .24, .0), (-.20, .40, -.60), (-.20, .50, -.90)], m.braid, radius=.004, sides=10)
    cyl(ctx, 'Chave externa · corte geral (E)', (.22, .80, -.28), .012, .03, m.anod_red, axis=UP, verts=12)
    cyl(ctx, 'Chave externa · extintor', (.16, .80, -.28), .012, .03, m.anod_red, axis=UP, verts=12)
    text_plate(ctx, 'Marcação de corte geral', 'E', (.22, .82, -.28), .02, m.paint_white, normal=UP, up=FWD)
