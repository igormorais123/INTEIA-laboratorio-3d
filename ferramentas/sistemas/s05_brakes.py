"""05 · Freios: discos carbono-carbono, campânulas, pinças monobloco, tambores de refrigeração,
pedal, cilindros mestres, barra de balanço, brake-by-wire traseiro e linhas hidráulicas.
Escala do carro v2: rodas dianteiras em (±0,735; 0,329; 1,521) e traseiras em (±0,735; 0,342; −1,838).
"""
import math
from lib import *

SYSTEM = ('brakes', 'Freios')

FRONT = (0.735, 0.329, 1.521)
REAR = (0.735, 0.342, -1.838)
DISC_X = 0.665
SHOTS = {
    'canto-dianteiro': ((0.66, 0.33, 1.52), 0.26, (1, .35, .9)),
    'canto-por-dentro': ((0.66, 0.33, 1.52), 0.26, (-1, .3, .6)),
    'pedaleira': ((0.0, 0.30, 1.05), 0.22, (-.8, .6, -1)),
    'brake-by-wire': ((0.15, 0.40, -0.26), 0.14, (1, .6, .5)),
}

def arc(center, radius, a0, a1, n=12):
    """Pontos no plano da roda: ângulo medido de +Z (frente) para +Y (cima), em graus."""
    cx, cy, cz = center
    if n <= 1:
        return [(cx, cy + radius * math.sin(math.radians(a0)), cz + radius * math.cos(math.radians(a0)))]
    return [(cx, cy + radius * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1))), cz + radius * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1)))) for i in range(n)]

def corner(ctx, wheel, front, label):
    m = ctx.m
    y, z = wheel[1], wheel[2]
    c = (DISC_X, y, z)
    r_out = .164 if front else .140
    r_in = r_out - .066
    made = []
    # Disco ventilado carbono-carbono (anel com 1.100+ furos radiais representados em textura)
    prof = [(r_in, -.016), (r_out, -.016), (r_out, .016), (r_in, .016), (r_in, -.016)]
    disc = lathe(ctx, f'Disco carbono-carbono {label}', prof, m.brake_disc, center=c, axis=RIGHT, segments=64, spin=1.2, tag='disc')
    box_uv(disc, 1 / (2 * r_out), (.5, .5))
    made.append(disc)
    # Campânula (bell) em alumínio usinado com pinos de arrasto flutuantes
    bell_prof = [(.046, -.082), (.060, -.082), (.060, -.040), (r_in + .004, -.024), (r_in + .004, -.010), (r_in - .004, -.010), (r_in - .004, -.020), (.052, -.034), (.052, -.082), (.046, -.082)]
    bell = lathe(ctx, f'Campânula do disco {label}', bell_prof, m.alu, center=c, axis=RIGHT, segments=48, spin=1.2)
    made.append(bell)
    made.append(bolt_ring(ctx, f'Pinos flutuantes do disco {label}', (DISC_X - .017, y, z), r_in + .001, 12, (-1, 0, 0), m.steel, size=.006, head=.004))
    # Cubo e porca central
    made.append(cyl(ctx, f'Cubo da roda {label}', (DISC_X - .04, y, z), .040, .19, m.steel_dark, axis=RIGHT, verts=40, spin=1.2))
    made.append(cyl(ctx, f'Porca central da roda {label}', (DISC_X + .07, y, z), .028, .026, m.anod_red, axis=RIGHT, verts=6, bev=.003, spin=1.2))
    made.append(cyl(ctx, f'Sextavado de acionamento da porca {label}', (DISC_X + .088, y, z), .016, .012, m.steel, axis=RIGHT, verts=6, bev=.001, spin=1.2))
    # Pinça monobloco de seis pistões, montada baixa (menor centro de gravidade)
    a0, a1 = (-56, -124) if front else (-50, -118)
    rc = r_out - .022
    caliper = sweep(ctx, f'Pinça monobloco {label}', arc(c, rc, a0, a1, 14), m.anod_black, section=lambda t: rounded_rect(.104, .058, .014), smooth_path=False)
    made.append(caliper)
    for half in (-1, 1):
        for a in (a0 + 12, (a0 + a1) / 2, a1 - 12):
            p = arc(c, rc, a, a, 1)[0]
            made.append(cyl(ctx, f'Pistão da pinça {label}', (DISC_X + half * .034, p[1], p[2]), .016, .020, m.titanium, axis=RIGHT, verts=20))
        pad = sweep(ctx, f'Pastilha carbono {label}', arc(c, rc, a0 + 4, a1 - 4, 10), m.brake_pad, section=lambda t: rounded_rect(.012, .044, .004), smooth_path=False)
        pad.location = W((half * .022, 0, 0)) + pad.location
        made.append(pad)
    for a in (a0 - 4, a1 + 4):
        p = arc(c, rc + .022, a, a, 1)[0]
        made.append(cyl(ctx, f'Sangrador da pinça {label}', (DISC_X + .04, p[1], p[2]), .004, .014, m.brass, axis=RIGHT, verts=8))
    made.append(text_plate(ctx, f'Gravação da pinça {label}', 'INTEIA', (DISC_X + .054, y - rc, z), .014, m.anod_red, normal=RIGHT, up=FWD))
    # Tambor (cake tin) e duto de refrigeração em carbono
    made.append(tube_cyl(ctx, f'Tambor de refrigeração do freio {label}', (DISC_X - .012, y, z), .204, .004, .11, m.carbon_matte, axis=RIGHT, verts=48))
    plate = lathe(ctx, f'Placa interna do tambor {label}', [(.062, -.066), (.204, -.066), (.204, -.062), (.062, -.062), (.062, -.066)], m.carbon_matte, center=c, axis=RIGHT, segments=48)
    made.append(plate)
    scoop = sweep(ctx, f'Entrada de ar do duto de freio {label}', [(DISC_X - .06, y - .03, z + .40), (DISC_X - .05, y - .02, z + .30), (DISC_X - .03, y, z + .22)], m.carbon_matte,
                  section=lambda t: rounded_rect(.10 - .03 * t, .07 - .02 * t, .012), smooth_path=True)
    made.append(scoop)
    made.append(cyl(ctx, f'Sensor infravermelho de temperatura do disco {label}', (DISC_X - .045, y + r_out * .55, z - r_out * .60), .006, .03, m.plastic_black, axis=RIGHT, verts=12))
    return made

def build(ctx):
    m = ctx.m
    for wheel, front, label in ((FRONT, True, 'dianteiro direito'), (REAR, False, 'traseiro direito')):
        parts = corner(ctx, wheel, front, label)
        for p in parts:
            mirror_x(ctx, p, p['part'].replace('direito', 'esquerdo'))
    # Pedal de freio (pé esquerdo): braço usinado afunilado com alívios, pisadeira curva e pivô no assoalho
    PX = -.06
    arm = [(PX, .165, 1.00), (PX, .25, .975), (PX, .34, .935), (PX, .39, .905)]
    sweep(ctx, 'Braço do pedal de freio', arm, m.alu, section=lambda t: rounded_rect(.014 - .004 * t, .052 - .026 * t, .003), smooth_path=True)
    for k, yy in enumerate((.215, .26, .30)):
        cyl(ctx, 'Alívio de massa do braço do pedal', (PX, yy, 1.0 - (yy - .165) * .28), .009 - k * .0015, .02, m.alu, axis=RIGHT, verts=16)
    pad = sweep(ctx, 'Pedal de freio · pisadeira', [(PX - .045, .33, .93), (PX, .335, .925), (PX + .045, .33, .93)], m.alu,
                section=lambda t: rounded_rect(.010, .085, .003), smooth_path=True)
    for k in range(5):
        cube(ctx, 'Nervura antiderrapante da pisadeira', (PX, .30 + k * .018, .945 - k * .0068), (.084, .0035, .006), m.anod_black, rot=(-22, 0, 0), bev=.0006)
    cyl(ctx, 'Pivô do pedal de freio', (PX, .165, 1.0), .010, .07, m.steel, axis=RIGHT)
    cube(ctx, 'Suporte do pedal no assoalho', (PX, .152, 1.0), (.08, .026, .06), m.alu_cast, bev=.003)
    cube(ctx, 'Apoio de calcanhar', (PX, .148, .90), (.12, .006, .12), m.carbon_matte, bev=.001)
    # Barra de balanço (bias bar) atravessando o braço do pedal, entre os dois cilindros mestres
    cyl(ctx, 'Barra de balanço · ajuste de bias', (PX, .31, 1.03), .006, .10, m.steel, axis=RIGHT, verts=16)
    sphere(ctx, 'Rótula da barra de balanço', (PX, .31, 1.03), .012, m.steel)
    sweep(ctx, 'Cabo de ajuste de bias para o cockpit', [(PX - .05, .31, 1.03), (PX - .10, .33, .90), (-.14, .40, .55), (-.18, .46, .30)], m.cable, radius=.003, sides=8)
    # Cilindros mestres duplos com reservatórios
    for x, label in ((PX - .036, 'circuito dianteiro'), (PX + .036, 'circuito traseiro')):
        cyl(ctx, f'Haste do cilindro mestre · {label}', (x, .31, 1.06), .005, .075, m.steel, axis=FWD, verts=12)
        cyl(ctx, f'Cilindro mestre · {label}', (x, .31, 1.165), .019, .14, m.alu, axis=FWD, verts=28, bev=.002)
        cyl(ctx, f'Tampa do cilindro mestre · {label}', (x, .31, 1.098), .021, .012, m.anod_black, axis=FWD, verts=28)
        cyl(ctx, f'Reservatório · {label}', (x, .36, 1.19), .015, .055, m.plastic_grey, axis=UP, verts=20)
        cyl(ctx, f'Tampa do reservatório · {label}', (x, .39, 1.19), .016, .008, m.anod_black, axis=UP, verts=20)
        cyl(ctx, f'Conexão de saída · {label}', (x, .31, 1.245), .008, .02, m.anod_blue, axis=FWD, verts=12)
    cube(ctx, 'Suporte dos cilindros mestres', (PX, .285, 1.10), (.13, .012, .10), m.carbon_matte, bev=.001)
    # Brake-by-wire do circuito traseiro: bloco hidráulico, solenoides, acumulador e sensor de pressão
    cube(ctx, 'Unidade brake-by-wire · bloco hidráulico', (.14, .40, -.26), (.10, .07, .12), m.anod_black, bev=.003)
    for dz in (-.035, 0, .035):
        cyl(ctx, 'Solenoide brake-by-wire', (.14, .45, -.26 + dz), .012, .03, m.steel_dark, axis=UP, verts=16)
    cyl(ctx, 'Acumulador de pressão brake-by-wire', (.20, .40, -.30), .018, .07, m.alu, axis=FWD, verts=20)
    cyl(ctx, 'Sensor de pressão do circuito traseiro', (.20, .40, -.22), .007, .03, m.brass, axis=FWD, verts=12)
    cube(ctx, 'Conector elétrico brake-by-wire', (.10, .445, -.20), (.03, .02, .02), m.plastic_black, bev=.001)
    # Linhas hidráulicas: rígidas ao longo da célula, trançadas nos trechos flexíveis
    caliper_in = lambda side, wheel: (side * .60, wheel[1] - .13, wheel[2] + .02)
    front_lines = {
        -1: [(-.096, .31, 1.25), (-.14, .33, 1.30), (-.24, .30, 1.36), (-.40, .26, 1.46), caliper_in(-1, FRONT)],
        1: [(-.096, .31, 1.25), (-.02, .35, 1.32), (.24, .30, 1.36), (.40, .26, 1.46), caliper_in(1, FRONT)],
    }
    rear_feed = [(-.024, .31, 1.25), (.04, .36, 1.10), (.10, .27, .60), (.13, .24, .10), (.14, .34, -.20), (.14, .40, -.26)]
    rear_lines = {
        -1: [(.14, .40, -.26), (.06, .30, -.55), (-.22, .22, -1.0), (-.40, .20, -1.55), (-.55, .20, -1.80), caliper_in(-1, REAR)],
        1: [(.14, .40, -.26), (.22, .30, -.55), (.32, .22, -1.0), (.42, .20, -1.55), (.55, .20, -1.80), caliper_in(1, REAR)],
    }
    for side, pts in front_lines.items():
        sweep(ctx, f'Linha rígida · circuito dianteiro {"esquerdo" if side < 0 else "direito"}', pts[:-2], m.steel, radius=.0028, sides=10, carrier=True)
        sweep(ctx, f'Mangueira trançada · pinça dianteira {"esquerda" if side < 0 else "direita"}', pts[-3:], m.braid, radius=.0045, sides=12, uv_len=30, carrier=True)
        flow_ribbon(ctx, f'Fluido de freio · circuito dianteiro {"esquerdo" if side < 0 else "direito"}', pts, 'brake', radius=.0016)
    sweep(ctx, 'Linha rígida · cilindro mestre traseiro → brake-by-wire', rear_feed, m.steel, radius=.0028, sides=10, carrier=True)
    flow_ribbon(ctx, 'Fluido de freio · alimentação traseira', rear_feed, 'brake', radius=.0016)
    for side, pts in rear_lines.items():
        sweep(ctx, f'Linha rígida · circuito traseiro {"esquerdo" if side < 0 else "direito"}', pts[:-2], m.steel, radius=.0028, sides=10, carrier=True)
        sweep(ctx, f'Mangueira trançada · pinça traseira {"esquerda" if side < 0 else "direita"}', pts[-3:], m.braid, radius=.0045, sides=12, uv_len=30, carrier=True)
        flow_ribbon(ctx, f'Fluido de freio · circuito traseiro {"esquerdo" if side < 0 else "direito"}', pts, 'brake', radius=.0016)
    # Braçadeiras P das linhas na célula
    for p in ((-.24, .30, 1.36), (.24, .30, 1.36), (.10, .27, .60), (.13, .24, .10), (-.22, .22, -1.0), (.32, .22, -1.0)):
        cyl(ctx, 'Braçadeira da linha de freio', p, .006, .008, m.anod_black, axis=UP, verts=10)
