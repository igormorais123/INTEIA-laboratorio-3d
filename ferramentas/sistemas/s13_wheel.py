"""13 · Volante e comandos, leiaute inspirado no protótipo Ferrari 2026 (testado em Abu Dhabi, 2025):
corpo de carbono retangular e achatado com orelhas laterais, empunhaduras verticais, display largo com
régua de quinze LEDs, colunas de botões coloridos, balancins de freio, três seletores grandes na base,
rolos de polegar, borboletas de marcha e de embreagem, engate rápido, eixo estriado e cabo helicoidal.
Centrado no cubo do volante do carro v2 (0; 0,5925; 0,527); a face dos comandos olha para o piloto (−Z).
Regulamento 2026: sem DRS; botões de override manual (OT) e aerodinâmica ativa (AA).
"""
import math
from lib import *

X_CONVENTION = 'piloto'   # +X = esquerda do piloto (ver lib.lado)
SYSTEM = ('wheel', 'Volante e comandos')

HUB = (0.0, 0.5925, 0.518)
SHOTS = {
    'frente': ((0.0, 0.59, 0.50), 0.20, (.15, .1, -1)),
    'tras': ((0.0, 0.59, 0.55), 0.20, (.3, .3, 1)),
    'lateral': ((0.0, 0.59, 0.52), 0.18, (1, .2, -.2)),
}

def build(ctx):
    m = ctx.m
    cx, cy, cz = HUB
    BACK = (0, 0, -1)                      # normal da face voltada ao piloto
    def Q(u, v, w=0.0):
        """u = direita do piloto, v = para cima, w = em direção ao piloto."""
        return (cx - u, cy + v, cz - w)
    def E(u, v, w):
        return (-u, v, -w)
    # Contorno do corpo (metade direita, do centro inferior ao centro superior) espelhado
    R = [(0, -.095), (.070, -.095)] + arc2d(.070, -.080, .015, -90, 0)[1:] + [(.085, -.060), (.100, -.045), (.132, -.030), (.145, -.005), (.146, .030), (.138, .058)] + arc2d(.118, .058, .020, 0, 90)[1:] + [(0, .078)]
    outline = R + [(-u, v) for u, v in reversed(R)][1:-1]
    plate(ctx, 'Corpo do volante · placa de carbono', outline, Q(0, 0, 0), .018, m.carbon, normal=BACK, explode=(0, 0, 0))
    plate(ctx, 'Tampa traseira de carbono', [(u * .93, v * .93) for u, v in outline], Q(0, 0, -.016), .014, m.carbon_matte, normal=BACK, explode=(0, 0, .14))
    cube(ctx, 'Placa eletrônica do volante', Q(0, -.005, -.012), (.20, .12, .003), m.pcb, bev=.0005, explode=(0, 0, .06))
    # Empunhaduras verticais em borracha texturizada e rolos de polegar
    for s in (-1, 1):
        lab = lado(-s)
        sweep(ctx, f'Empunhadura {lado(-s, True)}', [Q(s * .127, .058), Q(s * .129, .0), Q(s * .123, -.055), Q(s * .114, -.108)], m.grip,
              section=lambda t: rounded_rect(.030, .042, .011), smooth_path=True, explode=(-s * .10, -.02, 0))
        cyl(ctx, f'Rolo de polegar {lab} · ajuste fino', Q(s * .116, .046, .014), .007, .012, m.anod_black, axis=RIGHT, verts=16, explode=(-s * .06, .02, -.12))
    # Display largo com moldura e régua de quinze LEDs de troca acima
    cube(ctx, 'Moldura do display', Q(0, .028, .012), (.134, .070, .006), m.anod_black, bev=.001, explode=(0, 0, -.17))
    lcd = cube(ctx, 'Display LCD central', Q(0, .028, .0155), (.120, .058, .002), m.display, bev=.0005, explode=(0, 0, -.18))
    face_uv_fit(lcd, BACK)
    for i in range(15):
        u = -.056 + i * .008
        mat = m.led_green if i < 5 else m.led_red if i < 10 else m.led_blue
        cube(ctx, f'LED de troca {i + 1}', Q(u, .070, .012), (.006, .006, .005), mat, bev=.0008, explode=(0, .02, -.20))
    for s in (-1, 1):
        for k, (mat, cor) in enumerate(((m.led_amber, 'amarela'), (m.led_blue, 'azul'), (m.led_white, 'branca'))):
            cube(ctx, f'LED de bandeira {cor} {lado(-s)}', Q(s * .074, .056 - k * .012, .012), (.005, .005, .004), mat, bev=.0006, explode=(-s * .02, 0, -.16))
    # Botões: colunas laterais e cantos superiores (u < 0 = esquerda do piloto)
    buttons = [
        (-.098, .058, .010, m.anod_green, 'N', 'N · ponto morto'),
        (-.078, .052, .0075, m.anod_blue, 'R', 'R · rádio'),
        (-.078, .030, .0075, m.anod_cyan, 'DRK', 'DRINK · bebida'),
        (-.078, .008, .0075, m.anod_orange, 'OT', 'OT · override manual (2026)'),
        (-.098, .010, .0075, m.button_white, 'OK', 'OK · confirmação'),
        (.098, .058, .010, m.anod_red, 'P', 'P · limitador de boxes'),
        (.078, .052, .0075, m.anod_yellow, 'K1', 'K1 · recuperação extra de energia'),
        (.078, .030, .0075, m.anod_purple, 'AA', 'AA · aerodinâmica ativa (2026)'),
        (.078, .008, .0075, m.anod_gold, 'SOC', 'SOC · gestão de carga da bateria'),
        (.098, .010, .0075, m.anod_red, 'KO', 'KO · cancelar'),
        (-.120, .066, .006, m.button_black, 'PF', 'PF · chamada de boxes'),
        (.120, .066, .006, m.button_black, 'FLG', 'FLAG · confirmação de bandeira'),
    ]
    for u, v, r, mat, code, lab in buttons:
        cyl(ctx, f'Botão · {lab}', Q(u, v, .013), r, .008, mat, axis=FWD, verts=18, explode=(-u * .3, v * .3, -.16))
        text_plate(ctx, f'Legenda {code}', code, Q(u, v - r - .0055, .0095), .0042, m.paint_white, normal=BACK, up=UP, explode=(-u * .3, v * .3, -.16))
    # Balancins de freio (migração à esquerda, balanço à direita) e seletores pequenos
    cube(ctx, 'Balancim BMIG · migração de freio (−10/+10)', Q(-.104, -.016, .012), (.010, .022, .008), m.button_black, bev=.001, explode=(.04, 0, -.14))
    cube(ctx, 'Balancim BBAL · balanço de freio (−1/+1)', Q(.104, -.016, .012), (.010, .022, .008), m.button_black, bev=.001, explode=(-.04, 0, -.14))
    cyl(ctx, 'Seletor MID · mapa intermediário', Q(-.104, -.048, .014), .009, .012, m.anod_black, axis=FWD, verts=18, explode=(.04, -.02, -.15))
    cyl(ctx, 'Seletor EB · freio-motor', Q(.104, -.048, .014), .009, .012, m.anod_black, axis=FWD, verts=18, explode=(-.04, -.02, -.15))
    # Três seletores grandes na base, com anéis de posições coloridas
    palette = [m.anod_red, m.anod_yellow, m.anod_green, m.anod_cyan, m.anod_blue, m.anod_purple, m.anod_orange, m.button_white]
    for u, v, r, n, lab in ((-.062, -.062, .018, 8, 'Seletor multifunção esquerdo · estratégia (1–8)'), (0, -.060, .021, 12, 'Seletor central · modo de corrida'), (.062, -.062, .018, 12, 'Seletor multifunção direito · energia (1–12)')):
        cyl(ctx, lab, Q(u, v, .016), r, .014, m.anod_black, axis=FWD, verts=24, explode=(-u * .5, v, -.16))
        cyl(ctx, f'Tampa usinada · {lab.split(" · ")[0]}', Q(u, v, .0245), r * .6, .004, m.alu, axis=FWD, verts=20, explode=(-u * .5, v, -.17))
        cube(ctx, f'Indicador · {lab.split(" · ")[0]}', Q(u, v + r * .45, .0245), (.0015, r * .5, .0012), m.paint_white, bev=.0003, explode=(-u * .5, v, -.17))
        for k in range(n):
            a = math.radians(225 - 270 * k / (n - 1))
            cube(ctx, f'Posição {k + 1} · {lab.split(" · ")[0]}', Q(u + (r + .006) * math.cos(a), v + (r + .006) * math.sin(a), .0095), (.0035, .0035, .0015), palette[k % len(palette)], bev=.0004, explode=(-u * .5, v, -.15))
    cyl(ctx, 'Emblema INTEIA do seletor central', Q(0, -.060, .0265), .008, .0015, m.anod_red, axis=FWD, verts=20, explode=(0, -.06, -.18))
    text_plate(ctx, 'Gravação INTEIA no volante', 'INTEIA', Q(0, -.088, .0095), .008, m.alu_bright, normal=BACK, up=UP, explode=(0, -.02, -.12))
    # Borboletas atrás do volante: marcha (superiores, longas) e embreagem (inferiores)
    for s in (-1, 1):
        lab = lado(-s, True)
        plate(ctx, f'Borboleta de marcha {lab} ({"+" if s > 0 else "−"})', rounded_rect(.095, .045, .012), Q(s * .100, .012, -.032), .004, m.carbon, normal=BACK, explode=(-s * .05, 0, .20))
        plate(ctx, f'Borboleta de embreagem {lab}', rounded_rect(.080, .035, .010), Q(s * .090, -.050, -.042), .004, m.carbon_matte, normal=BACK, explode=(-s * .05, -.03, .26))
        cyl(ctx, f'Sensor da borboleta {lab}', Q(s * .045, .012, -.030), .008, .02, m.plastic_black, axis=FWD, verts=12, explode=(-s * .02, 0, .18))
    # Engate rápido, eixo estriado e conector elétrico com cabo helicoidal (lado da coluna, +Z)
    cyl(ctx, 'Engate rápido · cubo', Q(0, 0, -.034), .036, .026, m.alu, axis=FWD, verts=32, explode=(0, 0, .32))
    torus(ctx, 'Engate rápido · anel de liberação', Q(0, 0, -.028), .040, .006, m.anod_red, axis=FWD, seg=32, mseg=8, explode=(0, 0, .30))
    cyl(ctx, 'Eixo estriado', Q(0, 0, -.065), .014, .04, m.steel, axis=FWD, verts=18, explode=(0, 0, .40))
    cyl(ctx, 'Conector elétrico do volante', Q(0, -.05, -.028), .012, .02, m.plastic_black, axis=FWD, verts=14, explode=(0, -.06, .30))
    helix(ctx, 'Cabo helicoidal do volante', Q(0, -.05, -.09), .010, .008, 6, .0025, m.cable, axis=FWD, per_turn=16, explode=(0, -.06, .40))
