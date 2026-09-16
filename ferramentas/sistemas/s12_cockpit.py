"""12 · Cockpit e retenção do piloto: assento moldado em carbono, arnês de seis pontos com fecho
rotativo, HANS, pedal do acelerador e repouso, sistema de hidratação, acolchoados de perna,
painel de chaves e rádio.
"""
import math
from lib import *

SYSTEM = ('cockpit', 'Cockpit e retenção')

BUCKLE = (0.0, 0.40, 0.30)
SHOTS = {
    'assento-arnes': ((0.0, 0.45, 0.30), 0.55, (1, .6, .9)),
    'hans': ((0.0, 0.70, 0.10), 0.28, (1, .5, .8)),
    'pedais': ((0.05, 0.28, 0.95), 0.22, (-.8, .6, -1)),
    'hidratacao': ((-0.20, 0.40, 0.20), 0.35, (-1, .6, .6)),
}

def strap(ctx, name, pts, width=.075):
    return sweep(ctx, name, pts, ctx.m.webbing, section=lambda t: rounded_rect(width, .004, .0015), smooth_path=True)

def build(ctx):
    m = ctx.m
    # Assento moldado: casca em U seguindo a postura reclinada (coxas elevadas, ombros baixos)
    spine = [(0, .21, .80), (0, .19, .55), (0, .20, .35), (0, .27, .16), (0, .40, .0), (0, .56, -.10)]
    def seat_section(t):
        w = .40 - .06 * abs(t - .45)
        h = .10 + .08 * t
        pts = []
        n = 14
        for i in range(n + 1):
            a = math.pi * i / n
            pts.append((-w / 2 * math.cos(a), h * (1 - math.sin(a)) ))
        return pts
    sweep(ctx, 'Assento moldado em carbono', spine, m.carbon, section=seat_section, open_section=True, thickness=.006, uv_len=4)
    for side in (-1, 1):
        cube(ctx, f'Apoio lateral de coxa {"esquerdo" if side < 0 else "direito"}', (side * .17, .26, .55), (.04, .10, .30), m.foam, bev=.01)
        cube(ctx, f'Acolchoado de perna {"esquerdo" if side < 0 else "direito"}', (side * .22, .33, .80), (.03, .14, .26), m.nomex, bev=.008)
    # Arnês de seis pontos: ombros, cintura e virilha convergindo no fecho rotativo
    for side in (-1, 1):
        lab = 'esquerdo' if side < 0 else 'direito'
        strap(ctx, f'Cadarço de ombro {lab}', [(side * .10, .64, -.14), (side * .10, .60, .02), (side * .07, .50, .18), (side * .03, .41, .29)])
        strap(ctx, f'Cadarço de cintura {lab}', [(side * .29, .32, .28), (side * .18, .36, .30), (side * .05, .40, .30)], .070)
        strap(ctx, f'Cadarço de virilha {lab}', [(side * .06, .19, .52), (side * .05, .28, .40), (side * .03, .38, .32)], .055)
        cube(ctx, f'Ajustador do cadarço de ombro {lab}', (side * .095, .56, .11), (.08, .012, .05), m.alu, bev=.002)
        cube(ctx, f'Ancoragem de ombro {lab}', (side * .10, .64, -.15), (.06, .03, .03), m.steel, bev=.003)
        cube(ctx, f'Ancoragem de cintura {lab}', (side * .30, .32, .28), (.02, .04, .05), m.steel, bev=.003)
    cyl(ctx, 'Fecho rotativo central do arnês', BUCKLE, .040, .022, m.alu, axis=(0, 1, .3), verts=32, bev=.003)
    cyl(ctx, 'Alavanca de liberação do fecho', (0, .415, .29), .012, .06, m.anod_red, axis=(1, .2, 0), verts=12)
    # HANS: colar de carbono sobre os ombros com dois tirantes ao capacete
    yoke = [(-.20, .66, .22), (-.24, .70, .08), (-.16, .74, -.04), (0, .76, -.08), (.16, .74, -.04), (.24, .70, .08), (.20, .66, .22)]
    sweep(ctx, 'HANS · colar de carbono', yoke, m.carbon, section=lambda t: rounded_rect(.085, .026, .01), smooth_path=True)
    for side in (-1, 1):
        strap(ctx, f'Tirante do HANS {"esquerdo" if side < 0 else "direito"}', [(side * .12, .77, -.05), (side * .11, .80, .18), (side * .10, .80, .33)], .025)
        sphere(ctx, f'Ancoragem do tirante no capacete {"esquerda" if side < 0 else "direita"}', (side * .10, .80, .34), .01, m.steel)
    # Acelerador (pé direito) e repouso do pé, batente do calcanhar
    PX = .07
    sweep(ctx, 'Braço do pedal do acelerador', [(PX, .165, 1.00), (PX, .25, .975), (PX, .34, .935), (PX, .39, .905)], m.alu, section=lambda t: rounded_rect(.012 - .003 * t, .046 - .022 * t, .003), smooth_path=True)
    sweep(ctx, 'Pedal do acelerador · pisadeira', [(PX - .035, .33, .93), (PX, .335, .925), (PX + .035, .33, .93)], m.alu, section=lambda t: rounded_rect(.010, .080, .003), smooth_path=True)
    cyl(ctx, 'Pivô do pedal do acelerador', (PX, .165, 1.0), .010, .06, m.steel, axis=RIGHT)
    cyl(ctx, 'Sensor de posição do acelerador', (PX + .04, .165, 1.0), .014, .02, m.plastic_black, axis=RIGHT, verts=16)
    cyl(ctx, 'Mola de retorno do acelerador', (PX, .22, .99), .012, .05, m.steel, axis=(0, 1, -.3), verts=10)
    cube(ctx, 'Batente do calcanhar', (PX, .16, .90), (.10, .006, .10), m.carbon_matte, bev=.001)
    # Hidratação: bolsa no costado esquerdo, bomba e tubo até o capacete
    cube(ctx, 'Bolsa de hidratação', (-.25, .30, .10), (.04, .18, .12), m.plastic_grey, bev=.01)
    cyl(ctx, 'Bomba de hidratação', (-.25, .20, .10), .018, .04, m.plastic_black, axis=UP, verts=16)
    sweep(ctx, 'Tubo de hidratação → capacete', [(-.25, .39, .10), (-.22, .55, .22), (-.12, .72, .34), (-.04, .78, .38)], m.silicone_black, radius=.004, sides=10)
    # Painel de chaves e rádio no costado do cockpit
    cube(ctx, 'Painel de chaves auxiliares', (.0, .60, .84), (.16, .05, .012), m.carbon_matte, bev=.002)
    for k, x in enumerate((-.05, -.015, .02, .055)):
        cyl(ctx, f'Chave auxiliar {k + 1}', (x, .60, .85), .006, .014, m.anod_red if k == 0 else m.plastic_black, axis=FWD, verts=10)
    cube(ctx, 'Rádio · caixa de comunicação', (.25, .32, .10), (.04, .06, .10), m.anod_black, bev=.003)
    sweep(ctx, 'Cabo do rádio → capacete', [(.25, .35, .10), (.20, .60, .28), (.06, .78, .38)], m.cable, radius=.003, sides=8)
    cube(ctx, 'Espelho retrovisor · suporte esquerdo', (-.44, .62, .45), (.10, .008, .012), m.carbon_matte, bev=.001)
    cube(ctx, 'Espelho retrovisor · suporte direito', (.44, .62, .45), (.10, .008, .012), m.carbon_matte, bev=.001)
