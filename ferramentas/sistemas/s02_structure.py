"""02 · Estrutura central: célula de sobrevivência em sanduíche de carbono e colmeia (com janela
de corte mostrando o núcleo), anteparas dianteira, do painel e traseira, prisioneiros de fixação
do motor, insertos das ancoragens de suspensão, plank (skid block) e suportes do motor.
"""
import math
from lib import *
from s03_suspension import PICKUPS

SYSTEM = ('structure', 'Estrutura central')

TUB = [  # z, meia-largura, y inferior, y superior
    (-0.52, .30, .16, .74), (-0.30, .31, .16, .78), (-0.06, .31, .16, .66), (0.30, .30, .15, .60),
    (0.60, .29, .15, .56), (0.92, .26, .15, .52), (1.30, .22, .16, .50), (1.80, .17, .19, .42),
]
SHOTS = {
    'celula': ((0.0, 0.45, 0.6), 1.15, (1, .5, .8)),
    'corte-sanduiche': ((0.30, 0.45, 0.45), 0.30, (1, .6, .4)),
    'antepara-traseira': ((0.0, 0.45, -0.55), 0.50, (.8, .4, -1)),
    'plank': ((0.0, 0.05, -0.5), 1.2, (.5, -1, .3)),
}

def tub_section(z, w, y0, y1):
    pts = []
    for px, py in super_ellipse(2 * w, y1 - y0, 3.2, 40):
        pts.append((px, (y0 + y1) / 2 + py, z))
    return pts

def build(ctx):
    m = ctx.m
    secs = [tub_section(*row) for row in TUB]
    tub = shell(ctx, 'Célula de sobrevivência · sanduíche de carbono', secs, m.carbon, thickness=.018)
    # segundo material para a borda do sanduíche (colmeia visível nos cortes)
    tub.data.materials.append(m.honeycomb)
    for md in tub.modifiers:
        if md.type == 'SOLIDIFY':
            md.material_offset_rim = 1
            md.use_rim = True
    # abertura do cockpit e janela de corte lateral direita (para ver o núcleo de colmeia)
    cutters = []
    bpy.ops.mesh.primitive_cube_add(size=1, location=W((0, .70, .40)))
    c = bpy.context.object; c.scale = (.40, 1.10, .30); bpy.ops.object.transform_apply(scale=True); cutters.append(c)
    bpy.ops.mesh.primitive_cube_add(size=1, location=W((.32, .42, .45)))
    c = bpy.context.object; c.scale = (.10, .22, .20); bpy.ops.object.transform_apply(scale=True); cutters.append(c)
    for i, cutter in enumerate(cutters):
        md = tub.modifiers.new(f'Corte {i}', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = cutter; md.solver = 'EXACT'
    bpy.context.view_layer.objects.active = tub
    for md in list(tub.modifiers):
        bpy.ops.object.modifier_apply(modifier=md.name)
    for cutter in cutters:
        bpy.data.objects.remove(cutter)
    box_uv(tub, 8)
    # anteparas: dianteira, do painel e traseira (com furos de passagem representados por insertos)
    for z, w, y0, y1, lab in ((1.80, .17, .19, .42, 'dianteira'), (0.92, .26, .15, .52, 'do painel'), (-0.52, .30, .16, .74, 'traseira')):
        loft(ctx, f'Antepara {lab}', [tub_section(z - .008, w * .98, y0 + .01, y1 - .01), tub_section(z + .008, w * .98, y0 + .01, y1 - .01)], m.carbon_matte)
    # prisioneiros do motor na antepara traseira e tirantes de titânio até o bloco
    for x, y in ((-.24, .66), (.24, .66), (-.28, .24), (.28, .24)):
        cyl(ctx, 'Prisioneiro de fixação do motor', (x, y, -.56), .012, .06, m.steel, axis=FWD, verts=16)
        sweep(ctx, 'Tirante estrutural motor ↔ célula', [(x, y, -.58), (x * .85, y * .9 + .04, -.66)], m.titanium, radius=.010, sides=12, smooth_path=False)
    # antepara do nariz: pinos de fixação do cone (nariz destacável)
    for x, y in ((-.10, .36), (.10, .36), (-.10, .25), (.10, .25)):
        cyl(ctx, 'Pino de fixação do cone de nariz', (x, y, 1.82), .010, .05, m.steel, axis=FWD, verts=12)
    # insertos de titânio das ancoragens de suspensão dianteira colados no sanduíche
    P = PICKUPS['front']
    for key in ('uwi_f', 'uwi_a', 'lwi_f', 'lwi_a'):
        for side in (-1, 1):
            p = P[key]
            cube(ctx, 'Inserto de ancoragem da suspensão', (side * (p[0] - .02), p[1], p[2]), (.05, .05, .07), m.titanium, bev=.004)
    # suporte do balancim e da barra de torção sobre a célula
    for side in (-1, 1):
        rk = P['rocker']
        cube(ctx, 'Torre do balancim dianteiro', (side * rk[0], rk[1] - .05, rk[2]), (.07, .06, .12), m.carbon_matte, bev=.004)
    # plank (skid block) de madeira/compósito com pastilhas de titânio
    cube(ctx, 'Plank · skid block', (0, .052, -.60), (.30, .010, 2.60), m.plank, bev=.002, uv=6)
    for z in (.55, .05, -.55, -1.05, -1.55, -1.85):
        cyl(ctx, f'Pastilha de titânio do plank z={z:+.2f}', (0, .046, z), .028, .004, m.titanium, axis=UP, verts=20)
    # gabaritos: cinto do assoalho e pontos de içamento
    for side in (-1, 1):
        cube(ctx, 'Ponto de içamento lateral', (side * .30, .60, .10), (.03, .02, .06), m.steel, bev=.002)
    text_plate(ctx, 'Placa de identificação do chassi', 'INTEIA F1 · CHASSI 01', (.0, .30, 1.815), .014, m.alu_bright, normal=FWD, up=UP)
