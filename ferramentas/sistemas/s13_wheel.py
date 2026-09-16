"""13 · Volante e comandos: corpo de carbono com empunhaduras, display, quinze LEDs de troca,
botões, seletores rotativos, borboletas de marcha e de embreagem, engate rápido, conector e
tampa traseira. Posicionado sobre o volante do carro v2; o modo explodido separa as camadas.
"""
import math
from lib import *

SYSTEM = ('wheel', 'Volante e comandos')

HUB = (0.0, 0.62, 0.53)
SHOTS = {
    'frente': ((0.0, 0.62, 0.55), 0.20, (.15, .1, 1)),
    'tras': ((0.0, 0.62, 0.50), 0.20, (.3, .3, -1)),
    'lateral': ((0.0, 0.62, 0.52), 0.18, (1, .2, .2)),
}

def build(ctx):
    m = ctx.m
    cx, cy, cz = HUB
    body = [[(cx + px, cy + py, cz + dz) for px, py in super_ellipse(.28, .19, 2.6, 40)] for dz in (-.012, .012)]
    loft(ctx, 'Corpo do volante · placa frontal de carbono', body, m.carbon, explode=(0, 0, .12))
    loft(ctx, 'Quadro intermediário usinado', [[(cx + px * .97, cy + py * .97, cz + dz) for px, py in super_ellipse(.28, .19, 2.6, 40)] for dz in (-.030, -.012)], m.alu, explode=(0, 0, .0))
    loft(ctx, 'Tampa traseira de carbono', [[(cx + px * .95, cy + py * .95, cz + dz) for px, py in super_ellipse(.28, .19, 2.6, 40)] for dz in (-.042, -.030)], m.carbon_matte, explode=(0, 0, -.12))
    for side in (-1, 1):
        lab = 'esquerda' if side < 0 else 'direita'
        sweep(ctx, f'Empunhadura {lab}', [(cx + side * .145, cy - .07, cz + .0), (cx + side * .150, cy + .0, cz + .004), (cx + side * .145, cy + .07, cz + .0)], m.rubber, section=lambda t: rounded_rect(.038, .052, .015), smooth_path=True, explode=(side * .10, 0, .06))
        cube(ctx, f'Apoio de polegar {lab}', (cx + side * .115, cy + .075, cz + .018), (.03, .02, .012), m.rubber, bev=.004, explode=(side * .08, .04, .06))
    # Display central e bezel
    cube(ctx, 'Display LCD central', (cx, cy + .03, cz + .014), (.115, .066, .004), m.display, bev=.0005, explode=(0, 0, .18))
    cube(ctx, 'Bezel do display', (cx, cy + .03, cz + .012), (.125, .076, .004), m.anod_black, bev=.001, explode=(0, 0, .17))
    # Quinze LEDs de troca em arco: verdes, vermelhos, azuis
    for i in range(15):
        a = math.radians(150 - i * 8.6)
        p = (cx + .105 * math.cos(a), cy + .04 + .045 * math.sin(a), cz + .016)
        mat = m.led_green if i < 5 else m.led_red if i < 10 else m.led_blue
        cube(ctx, f'LED de troca {i + 1}', p, (.008, .008, .006), mat, bev=.0008, explode=(0, .02, .20))
    # Botões coloridos: seis por lado
    palette = [(m.anod_red, 'rádio'), (m.anod_blue, 'bebida'), (m.anod_gold, 'DRS'), (m.led_green, 'ultrapassagem'), (m.paint_white, 'limitador de boxes'), (m.anod_black, 'neutro')]
    for side in (-1, 1):
        for k, (mat, lab) in enumerate(palette):
            col = k % 2; row = k // 2
            p = (cx + side * (.055 + col * .03), cy + .0 - row * .03, cz + .016)
            cyl(ctx, f'Botão · {lab} {"E" if side < 0 else "D"}', p, .008, .008, mat, axis=FWD, verts=16, explode=(side * .03, 0, .15))
    # Seletores rotativos: dois grandes (estratégia/modo) e quatro pequenos
    for k, (x, y, r, lab) in enumerate(((-.03, -.06, .015, 'estratégia'), (.03, -.06, .015, 'modo do motor'), (-.09, -.055, .010, 'diferencial'), (.09, -.055, .010, 'freio motor'), (-.06, -.075, .008, 'mistura'), (.06, -.075, .008, 'ERS'))):
        cyl(ctx, f'Seletor rotativo · {lab}', (cx + x, cy + y, cz + .018), r, .012, m.anod_black, axis=FWD, verts=20, explode=(x * .5, y, .16))
        cube(ctx, f'Indicador do seletor · {lab}', (cx + x, cy + y + r * .7, cz + .025), (.002, r * .6, .002), m.paint_white, bev=.0003, explode=(x * .5, y, .16))
    # Borboletas de marcha (superiores) e de embreagem (inferiores), atrás do volante
    for side in (-1, 1):
        lab = 'esquerda' if side < 0 else 'direita'
        loft(ctx, f'Borboleta de marcha {lab} ({"−" if side < 0 else "+"})', [[(cx + side * (.06 + px * .09), cy - .01 + py * .05, cz - .055) for px, py in rounded_rect(1, 1, .2)], [(cx + side * (.06 + px * .09), cy - .01 + py * .05, cz - .050) for px, py in rounded_rect(1, 1, .2)]], m.carbon, explode=(side * .05, 0, -.20))
        loft(ctx, f'Borboleta de embreagem {lab}', [[(cx + side * (.05 + px * .08), cy - .07 + py * .035, cz - .070) for px, py in rounded_rect(1, 1, .2)], [(cx + side * (.05 + px * .08), cy - .07 + py * .035, cz - .065) for px, py in rounded_rect(1, 1, .2)]], m.carbon_matte, explode=(side * .05, -.03, -.26))
        cyl(ctx, f'Sensor da borboleta {lab}', (cx + side * .03, cy - .01, cz - .050), .008, .02, m.plastic_black, axis=FWD, verts=12, explode=(side * .02, 0, -.18))
    # Engate rápido, eixo estriado e conector elétrico com cabo helicoidal
    cyl(ctx, 'Engate rápido · cubo', (cx, cy, cz - .055), .038, .026, m.alu, axis=FWD, verts=32, explode=(0, 0, -.32))
    torus(ctx, 'Engate rápido · anel de liberação', (cx, cy, cz - .05), .040, .006, m.anod_red, axis=FWD, seg=32, mseg=8, explode=(0, 0, -.30))
    cyl(ctx, 'Eixo estriado', (cx, cy, cz - .085), .014, .04, m.steel, axis=FWD, verts=18, explode=(0, 0, -.40))
    cyl(ctx, 'Conector elétrico do volante', (cx, cy - .05, cz - .048), .012, .02, m.plastic_black, axis=FWD, verts=14, explode=(0, -.06, -.30))
    helix(ctx, 'Cabo helicoidal do volante', (cx, cy - .05, cz - .11), .010, .008, 6, .0025, m.cable, axis=FWD, per_turn=16, explode=(0, -.06, -.40))
    cube(ctx, 'Placa eletrônica do volante', (cx, cy - .005, cz - .022), (.20, .12, .004), m.pcb, bev=.0005, explode=(0, 0, .04))
    text_plate(ctx, 'Gravação INTEIA no volante', 'INTEIA', (cx, cy - .095, cz + .013), .014, m.alu_bright, normal=FWD, up=UP, explode=(0, -.02, .12))
