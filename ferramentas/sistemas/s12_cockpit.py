"""12 · Cockpit e retenção do piloto: assento moldado dentro da cavidade real do cockpit do carro v2
(piso em y ≈ 0,33 e paredes em x = ±0,154), arnês de seis pontos com fecho rotativo, HANS, pedal do
acelerador no pé direito (x < 0), sistema de hidratação, acolchoados de perna, painel de chaves e rádio.
"""
import math
from lib import *

X_CONVENTION = 'piloto'   # +X = esquerda do piloto (ver lib.lado)
SYSTEM = ('cockpit', 'Cockpit e retenção')

BUCKLE = (0.0, 0.46, 0.30)
SHOTS = {
    'assento-arnes': ((0.0, 0.50, 0.25), 0.55, (1, .6, .9)),
    'hans': ((0.0, 0.72, 0.10), 0.28, (1, .5, .8)),
    'pedais': ((-0.05, 0.28, 0.95), 0.22, (.8, .6, -1)),
    'hidratacao': ((0.12, 0.42, 0.45), 0.35, (1, .6, .6)),
}

def strap(ctx, name, pts, width=.075):
    return sweep(ctx, name, pts, ctx.m.webbing, section=lambda t: rounded_rect(width, .004, .0015), smooth_path=True)

def build(ctx):
    m = ctx.m
    # Assento moldado: casca em U que segue o piso da cavidade do cockpit (coxas elevadas, ombros baixos)
    spine = [(0, .445, .82), (0, .42, .62), (0, .36, .45), (0, .34, .30), (0, .33, .12), (0, .35, -.02), (0, .44, -.12), (0, .58, -.18), (0, .70, -.22)]
    def seat_section(t):
        w = .29 if t < .55 else .29 + .11 * (t - .55) / .45
        h = .09 + .10 * t
        pts = []
        n = 14
        for i in range(n + 1):
            a = math.pi * i / n
            pts.append((-w / 2 * math.cos(a), h * (1 - math.sin(a))))
        return pts
    sweep(ctx, 'Assento moldado em carbono', spine, m.carbon, section=seat_section, open_section=True, thickness=.006, uv_len=4)
    for side in (-1, 1):
        cube(ctx, f'Apoio lateral de coxa {lado(side)}', (side * .125, .40, .55), (.03, .08, .26), m.foam, bev=.008)
        cube(ctx, f'Acolchoado de perna {lado(side)}', (side * .10, .50, .80), (.03, .10, .24), m.nomex, bev=.008)
    # Arnês de seis pontos: ombros, cintura e virilha convergindo no fecho rotativo
    for side in (-1, 1):
        lab = lado(side)
        strap(ctx, f'Cadarço de ombro {lab}', [(side * .10, .66, -.15), (side * .10, .62, .0), (side * .07, .53, .16), (side * .03, .47, .28)])
        strap(ctx, f'Cadarço de cintura {lab}', [(side * .15, .36, .30), (side * .11, .42, .30), (side * .05, .45, .30)], .070)
        strap(ctx, f'Cadarço de virilha {lab}', [(side * .05, .36, .52), (side * .045, .42, .40), (side * .03, .445, .33)], .055)
        cube(ctx, f'Ajustador do cadarço de ombro {lab}', (side * .095, .585, .09), (.08, .012, .05), m.alu, bev=.002)
        cube(ctx, f'Ancoragem de ombro {lab}', (side * .10, .66, -.16), (.06, .03, .03), m.steel, bev=.003)
        cube(ctx, f'Ancoragem de cintura {lab}', (side * .155, .36, .30), (.012, .04, .05), m.steel, bev=.003)
    cyl(ctx, 'Fecho rotativo central do arnês', BUCKLE, .040, .022, m.alu, axis=(0, 1, .3), verts=32, bev=.003)
    cyl(ctx, 'Alavanca de liberação do fecho', (0, .475, .29), .012, .06, m.anod_red, axis=(1, .2, 0), verts=12)
    # HANS: colar de carbono sobre os ombros com dois tirantes ao capacete
    yoke = [(-.20, .68, .22), (-.24, .72, .08), (-.16, .76, -.04), (0, .78, -.08), (.16, .76, -.04), (.24, .72, .08), (.20, .68, .22)]
    sweep(ctx, 'HANS · colar de carbono', yoke, m.carbon, section=lambda t: rounded_rect(.085, .026, .01), smooth_path=True)
    for side in (-1, 1):
        strap(ctx, f'Tirante do HANS {lado(side)}', [(side * .12, .79, -.05), (side * .11, .82, .18), (side * .10, .82, .33)], .025)
        sphere(ctx, f'Ancoragem do tirante no capacete {lado(side, True)}', (side * .10, .82, .34), .01, m.steel)
    # Acelerador no pé direito (x < 0), pisadeira, pivô, sensor, mola e batente do calcanhar
    PX = -.07
    sweep(ctx, 'Braço do pedal do acelerador', [(PX, .165, 1.00), (PX, .25, .975), (PX, .34, .935), (PX, .39, .905)], m.alu, section=lambda t: rounded_rect(.012 - .003 * t, .046 - .022 * t, .003), smooth_path=True)
    sweep(ctx, 'Pedal do acelerador · pisadeira', [(PX - .035, .33, .93), (PX, .335, .925), (PX + .035, .33, .93)], m.alu, section=lambda t: rounded_rect(.010, .080, .003), smooth_path=True)
    cyl(ctx, 'Pivô do pedal do acelerador', (PX, .165, 1.0), .010, .06, m.steel, axis=RIGHT)
    cyl(ctx, 'Sensor de posição do acelerador', (PX - .04, .165, 1.0), .014, .02, m.plastic_black, axis=RIGHT, verts=16)
    cyl(ctx, 'Mola de retorno do acelerador', (PX, .22, .99), .012, .05, m.steel, axis=(0, 1, -.3), verts=10)
    cube(ctx, 'Batente do calcanhar', (PX, .16, .90), (.10, .006, .10), m.carbon_matte, bev=.001)
    # Hidratação: bolsa ao lado da coxa esquerda (x > 0), bomba e tubo até o capacete
    cube(ctx, 'Bolsa de hidratação', (.12, .42, .55), (.035, .09, .14), m.plastic_grey, bev=.008)
    cyl(ctx, 'Bomba de hidratação', (.12, .37, .46), .016, .04, m.plastic_black, axis=FWD, verts=16)
    sweep(ctx, 'Tubo de hidratação → capacete', [(.12, .47, .55), (.16, .58, .35), (.10, .72, .30), (.04, .80, .36)], m.silicone_black, radius=.004, sides=10)
    # Painel de chaves auxiliares no painel, rádio ao lado da coxa direita
    cube(ctx, 'Painel de chaves auxiliares', (.0, .555, .83), (.16, .045, .012), m.carbon_matte, bev=.002)
    for k, x in enumerate((-.05, -.015, .02, .055)):
        cyl(ctx, f'Chave auxiliar {k + 1}', (x, .555, .84), .006, .014, m.anod_red if k == 0 else m.plastic_black, axis=FWD, verts=10)
    cube(ctx, 'Rádio · caixa de comunicação', (-.12, .40, .35), (.035, .05, .10), m.anod_black, bev=.003)
    sweep(ctx, 'Cabo do rádio → capacete', [(-.12, .43, .35), (-.16, .60, .28), (-.06, .80, .36)], m.cable, radius=.003, sides=8)
