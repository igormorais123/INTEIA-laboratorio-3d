"""14 · Sensores e telemetria: tubo de Pitot, sensores de velocidade de roda com anéis dentados,
câmeras infravermelhas de pneu, lasers de altura, ECU padrão, gravador de acidentes, IMU,
células de carga nos push/pull-rods, termopares de escape, transceptor e antena de telemetria,
chicote principal com conectores e fluxos de dados.
"""
import math
from lib import *
from s03_suspension import PICKUPS

SYSTEM = ('sensors', 'Sensores e telemetria')

ECU = (-0.22, 0.22, 0.32)
SHOTS = {
    'pitot': ((0.0, 0.38, 1.98), 0.16, (1, .5, .8)),
    'ecu': ((-0.22, 0.24, 0.32), 0.24, (-1, .8, .6)),
    'roda': ((0.62, 0.30, 1.52), 0.18, (-.6, .5, .8)),
    'antena': ((0.0, 0.75, 1.10), 0.22, (1, .5, .8)),
}

def build(ctx):
    m = ctx.m
    # Tubo de Pitot no nariz com mastro carenado e tomadas estáticas
    sweep(ctx, 'Mastro do Pitot', [(0, .33, 1.98), (0, .44, 1.98)], m.carbon_fine, section=lambda t: airfoil(.03, .3, 0, 10), smooth_path=False)
    cyl(ctx, 'Tubo de Pitot', (0, .445, 2.06), .005, .17, m.alu_bright, axis=FWD, verts=12)
    tube_cyl(ctx, 'Ponta do Pitot · tomada dinâmica', (0, .445, 2.15), .0028, .0006, .02, m.brass, axis=FWD, verts=24)
    for a in (0, 90, 180, 270):
        cyl(ctx, f'Tomada estática {a}°', (0.006 * math.cos(math.radians(a)), .445 + .006 * math.sin(math.radians(a)), 2.08), .001, .003, m.steel_dark, axis=(math.cos(math.radians(a)), math.sin(math.radians(a)), 0), verts=6)
    flow_ribbon(ctx, 'Pressão do Pitot → transdutor → ECU', [(0, .445, 2.06), (0, .36, 1.90), (-.10, .30, 1.40), (-.20, .26, .90), ECU], 'data', radius=.003)
    # Sensores de velocidade de roda e anéis dentados nos cubos; câmeras IR de pneu
    for wheel, front in (((0.735, 0.329, 1.521), True), ((0.735, 0.342, -1.838), False)):
        for side in (-1, 1):
            lab = f'{"dianteiro" if front else "traseiro"} {"esquerdo" if side < 0 else "direito"}'
            gear(ctx, f'Anel dentado do sensor de velocidade {lab}', (side * .56, wheel[1], wheel[2]), 48, .0022, .006, m.steel, axis=RIGHT, bore=.045, spin=1.2)
            cyl(ctx, f'Sensor de velocidade de roda {lab}', (side * .555, wheel[1] + .075, wheel[2]), .007, .03, m.plastic_black, axis=UP, verts=12)
            cube(ctx, f'Câmera infravermelha de temperatura do pneu {lab}', (side * .60, .42, wheel[2] + (.30 if front else -.30)), (.03, .03, .05), m.plastic_black, bev=.003)
            cyl(ctx, f'Lente da câmera IR {lab}', (side * .60, .42, wheel[2] + (.325 if front else -.325)), .008, .004, m.glass_tint, axis=(0, 0, 1 if front else -1), verts=12)
    # Lasers de altura sob a célula, dianteiro e traseiro
    for z, lab in ((1.20, 'dianteiro'), (-1.40, 'traseiro')):
        cube(ctx, f'Sensor laser de altura {lab}', (.12, .17, z), (.05, .03, .07), m.anod_black, bev=.003)
        cube(ctx, f'Janela do laser {lab}', (.12, .154, z), (.03, .002, .04), m.led_red)
        flow_ribbon(ctx, f'Feixe do laser de altura {lab}', [(.12, .15, z), (.12, .0, z)], 'data', radius=.002)
    # ECU padrão, gravador de acidentes, IMU e transceptor de telemetria
    cube(ctx, 'ECU padrão · unidade de controle', ECU, (.11, .05, .24), m.alu_cast, bev=.004, uv=8)
    for k in range(3):
        p=(ECU[0], ECU[1]+.03, ECU[2]-.08+k*.08)
        tube_cyl(ctx,f'Conector circular da ECU {k + 1}',p,.017,.0025,.018,m.anod_black,axis=UP,verts=32)
        cyl(ctx,f'Isolador do conector ECU {k + 1}',(p[0],p[1]-.003,p[2]),.0135,.008,m.plastic_black,axis=UP,verts=24)
        for pin in range(7):
            a=pin*2*math.pi/6
            rr=.008 if pin<6 else 0
            cyl(ctx,f'Contato do conector ECU {k + 1} · pino {pin + 1}',(p[0]+rr*math.cos(a),p[1]+.003,p[2]+rr*math.sin(a)),.0013,.009,m.brass,axis=UP,verts=8,bev=.0002)
        torus(ctx,f'Anel de trava do conector ECU {k + 1}',(p[0],p[1]+.006,p[2]),.017,.0013,m.alu,axis=UP,seg=32,mseg=6)
    text_plate(ctx, 'Gravação da ECU', 'SECU', (ECU[0] - .056, ECU[1], ECU[2]), .014, m.alu_bright, normal=(-1, 0, 0), up=UP)
    cube(ctx, 'Gravador de dados de acidente', (.22, .22, .32), (.10, .03, .14), m.anod_red, bev=.003)
    cube(ctx, 'Unidade inercial · IMU', (0, .30, -.05), (.05, .03, .05), m.anod_black, bev=.003)
    cube(ctx, 'Transceptor de telemetria', (-.22, .22, .06), (.10, .04, .10), m.anod_black, bev=.003)
    sweep(ctx, 'Cabo coaxial → antena', [(-.22, .24, .06), (-.24, .30, .40), (-.14, .50, .90), (0, .66, 1.10)], m.cable, radius=.003, sides=8)
    sweep(ctx, 'Antena de telemetria em lâmina', [(0, .68, 1.10), (0, .80, 1.06)], m.carbon_fine, section=lambda t: airfoil(.05 - .02 * t, .25, 0, 10), smooth_path=False)
    # Células de carga nos push/pull-rods e termopares de escape, sensores de pressão de freio
    for axle in ('front', 'rear'):
        P = PICKUPS[axle]
        for side in (-1, 1):
            a, b = P['pro'], P['rocker_arm']
            mid = (side * (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
            d = (side * (b[0] - a[0]), b[1] - a[1], b[2] - a[2])
            cyl(ctx, f'Célula de carga do {"push" if axle == "front" else "pull"}-rod {"esquerdo" if side < 0 else "direito"}', mid, .016, .04, m.anod_gold, axis=d, verts=16)
    for side in (-1, 1):
        cyl(ctx, f'Termopar de escape {"esquerdo" if side < 0 else "direito"}', (side * .335, .47, -1.05), .004, .04, m.steel, axis=UP, verts=8)
    for x, lab in ((-.096, 'dianteiro'), (-.024, 'traseiro')):
        cyl(ctx, f'Sensor de pressão do freio · circuito {lab}', (x, .345, 1.235), .007, .025, m.brass, axis=UP, verts=10)
    cyl(ctx, "Sensor de temperatura da água", (.24, .66, -1.16), .006, .03, m.brass, axis=UP, verts=8)
    cyl(ctx, 'Sensor de pressão do óleo', (-.31, .58, -.52), .006, .03, m.brass, axis=UP, verts=8)
    # Chicote principal com conectores e fluxos de dados até a ECU e ao box
    loom_rear = [ECU, (-.27, .24, -.30), (-.22, .42, -.70), (-.16, .46, -1.20), (-.10, .40, -1.55)]
    loom_front = [ECU, (-.22, .30, .90), (-.14, .34, 1.25), (-.10, .36, 1.40)]
    for pts, lab in ((loom_rear, 'traseiro'), (loom_front, 'dianteiro')):
        sweep(ctx, f'Chicote principal {lab}', pts, m.braid, radius=.010, sides=12, uv_len=30, carrier=True)
        for p in pts[1:]:
            cyl(ctx, f'Conector do chicote {lab}', p, .013, .02, m.plastic_grey, axis=FWD, verts=14)
        flow_ribbon(ctx, f'Dados dos sensores → ECU ({lab})', list(reversed(pts)), 'data', radius=.0035)
    flow_ribbon(ctx, 'Telemetria carro → box', [(0, .80, 1.06), (.30, 1.10, 1.0), (.70, 1.50, .90), (1.2, 1.9, .8)], 'data', radius=.006)
