"""03 · Suspensão: wishbones em perfil aerodinâmico, uprights usinados, pushrod dianteiro,
pullrod traseiro, balancins, barras de torção, amortecedores inboard, elemento heave com
pilha Belleville e barras antirrolagem. Pontos de ancoragem compartilhados com direção,
freios e segurança (PICKUPS).
"""
import math
from lib import *

SYSTEM = ('suspension', 'Suspensão')

FRONT_WHEEL = (0.735, 0.329, 1.521)
REAR_WHEEL = (0.735, 0.342, -1.838)

# Pontos de ancoragem do lado direito (x > 0); o lado esquerdo é espelhado.
PICKUPS = {
    'front': {
        'uwo': (0.610, 0.470, 1.521), 'uwi_f': (0.250, 0.535, 1.745), 'uwi_a': (0.250, 0.515, 1.335),
        'lwo': (0.625, 0.205, 1.521), 'lwi_f': (0.240, 0.190, 1.725), 'lwi_a': (0.240, 0.180, 1.315),
        'pro': (0.560, 0.222, 1.505), 'rocker': (0.205, 0.600, 1.455), 'rocker_arm': (0.265, 0.585, 1.470),
        'damper_a': (0.125, 0.660, 1.415), 'damper_b': (0.125, 0.660, 1.140),
        'tro': (0.610, 0.360, 1.400), 'rack_end': (0.265, 0.340, 1.360),
    },
    'rear': {
        'uwo': (0.615, 0.470, -1.838), 'uwi_f': (0.175, 0.505, -1.610), 'uwi_a': (0.175, 0.495, -2.010),
        'lwo': (0.630, 0.215, -1.838), 'lwi_f': (0.160, 0.205, -1.590), 'lwi_a': (0.160, 0.195, -2.030),
        'pro': (0.590, 0.455, -1.800), 'rocker': (0.185, 0.245, -1.720), 'rocker_arm': (0.245, 0.262, -1.735),
        'damper_a': (0.120, 0.230, -1.680), 'damper_b': (0.120, 0.230, -1.440),
        'tro': (0.615, 0.300, -1.925), 'rack_end': (0.165, 0.300, -2.020),
    },
}
SHOTS = {
    'dianteira': ((0.42, 0.40, 1.50), 0.42, (1, .45, .9)),
    'dianteira-inboard': ((0.15, 0.60, 1.35), 0.26, (.7, .8, .6)),
    'traseira': ((0.42, 0.35, -1.80), 0.42, (1, .4, -.8)),
    'upright': ((0.61, 0.33, 1.52), 0.18, (-.9, .35, .5)),
}

def leg(ctx, name, a, b, mat, chord=.048, thick=.26, camber=0.0):
    return sweep(ctx, name, [a, b], mat, section=lambda t: airfoil(chord, thick, camber, 14), smooth_path=False)

def mirror_side(v):
    return (-v[0], v[1], v[2])

def rod_end(ctx, name, p, mat, r=.011):
    """Rótula esférica em alojamento usinado."""
    return sphere(ctx, name, p, r, mat)

def upright(ctx, P, front, label):
    m = ctx.m
    y_lo, y_hi = P['lwo'][1], P['uwo'][1]
    xc = 0.625 if front else 0.63
    zc = P['uwo'][2]
    # corpo em alumínio usinado: loft de seções entre os pontos inferior e superior
    sections = []
    for t in (0, .18, .40, .62, .82, 1):
        y = y_lo + (y_hi - y_lo) * t
        w = .052 + .038 * math.sin(math.pi * t) ** .8
        d = .090 + .090 * math.sin(math.pi * t) ** .6
        sections.append([(xc + px, y, zc + py) for px, py in rounded_rect(w, d, .012)])
    body = loft(ctx, f'Upright usinado {label}', sections, m.alu)
    # alojamento do rolamento do cubo
    lathe(ctx, f'Alojamento do rolamento {label}', [(.040, -.040), (.066, -.040), (.070, -.030), (.070, .034), (.062, .040), (.040, .040), (.040, -.040)], m.alu, center=(xc + .012, P['uwo'][1] - (y_hi - y_lo) * .48, zc), axis=RIGHT, segments=44)
    bolt_ring(ctx, f'Parafusos da tampa do rolamento {label}', (xc - .028, P['uwo'][1] - (y_hi - y_lo) * .48, zc), .058, 6, (-1, 0, 0), m.steel, size=.005, head=.003)
    # garfos (clevis) das rótulas superior e inferior
    for key, nm in (('uwo', 'Garfo superior'), ('lwo', 'Garfo inferior')):
        p = P[key]
        cube(ctx, f'{nm} do upright {label}', (p[0] - .010, p[1], p[2]), (.036, .026, .05), m.alu, bev=.003)
        rod_end(ctx, f'Rótula {nm.lower()} {label}', p, m.titanium)
    # braço de direção / toe link
    p = P['tro']
    cube(ctx, f'Braço de direção do upright {label}', ((p[0] + xc) / 2, p[1], (p[2] + zc) / 2), (abs(p[0] - xc) + .02, .022, abs(p[2] - zc) + .03), m.alu, bev=.003)
    rod_end(ctx, f'Rótula do braço de direção {label}', p, m.titanium)
    # sensor de curso / mangueira do duto e furos de refrigeração do cubo já pertencem a outros sistemas
    return body

def corner(ctx, P, front, label):
    m = ctx.m
    wish = m.carbon_fine
    parts = []
    # wishbones superior e inferior, duas pernas em perfil de asa convergindo na rótula externa
    for key_o, key_f, key_a, nm, chord in (('uwo', 'uwi_f', 'uwi_a', 'superior', .050), ('lwo', 'lwi_f', 'lwi_a', 'inferior', .056)):
        parts.append(leg(ctx, f'Wishbone {nm} · perna dianteira {label}', P[key_f], P[key_o], wish, chord))
        parts.append(leg(ctx, f'Wishbone {nm} · perna traseira {label}', P[key_a], P[key_o], wish, chord))
        for key in (key_f, key_a):
            p = P[key]
            parts.append(cube(ctx, f'Alojamento da rótula interna {nm} {label}', (p[0] + .012, p[1], p[2]), (.03, .034, .05), m.titanium, bev=.003))
            parts.append(rod_end(ctx, f'Rótula interna {nm} {label}', p, m.steel, .010))
        # cobertura aerodinâmica na junção externa
        p = P[key_o]
        parts.append(sphere(ctx, f'Carenagem da junção externa {nm} {label}', (p[0] - .006, p[1], p[2]), .022, wish, scale=(1.2, .7, 1.6)))
    parts.append(upright(ctx, P, front, label))
    # push-rod (dianteira) ou pull-rod (traseira): perfil oval inclinado até o balancim
    rod_name = 'Push-rod' if front else 'Pull-rod'
    parts.append(sweep(ctx, f'{rod_name} {label}', [P['pro'], P['rocker_arm']], wish, section=lambda t: airfoil(.040, .42, 0, 12), smooth_path=False))
    for key in ('pro', 'rocker_arm'):
        parts.append(rod_end(ctx, f'Rótula do {rod_name.lower()} {label}', P[key], m.titanium, .010))
    # balancim (rocker) usinado em L, girando em eixo longitudinal
    rk = P['rocker']
    parts.append(cyl(ctx, f'Eixo do balancim {label}', rk, .014, .07, m.steel, axis=FWD, verts=20))
    ra = P['rocker_arm']; da = P['damper_a']
    parts.append(sweep(ctx, f'Balancim · braço do {rod_name.lower()} {label}', [rk, ra], m.alu, section=lambda t: rounded_rect(.028, .020 - .006 * t, .004), smooth_path=False))
    parts.append(sweep(ctx, f'Balancim · braço do amortecedor {label}', [rk, da], m.alu, section=lambda t: rounded_rect(.028, .020 - .006 * t, .004), smooth_path=False))
    # barra de torção coaxial ao balancim, correndo para dentro da estrutura
    sgn = 1 if front else -1
    parts.append(cyl(ctx, f'Barra de torção {label}', (rk[0], rk[1], rk[2] - sgn * .20), .010, .36, m.steel_dark, axis=FWD, verts=16))
    parts.append(cyl(ctx, f'Estriado da barra de torção {label}', (rk[0], rk[1], rk[2] - sgn * .385), .016, .03, m.steel, axis=FWD, verts=24))
    parts.append(cube(ctx, f'Suporte do balancim na estrutura {label}', (rk[0], rk[1] - .022, rk[2]), (.05, .016, .06), m.carbon_matte, bev=.002))
    # amortecedor inboard longitudinal: corpo anodizado, haste polida, reservatório e ajustadores
    db = P['damper_b']
    body_a = (da[0], da[1], da[2] + (db[2] - da[2]) * .30); body_b = db
    parts.append(sweep(ctx, f'Corpo do amortecedor {label}', [body_a, body_b], m.anod_black, radius=.021, sides=24, smooth_path=False))
    parts.append(sweep(ctx, f'Haste do amortecedor {label}', [da, body_a], m.alu_bright, radius=.007, sides=16, smooth_path=False))
    parts.append(cyl(ctx, f'Ajustador de compressão {label}', (db[0], db[1] + .012, db[2]), .012, .03, m.anod_blue, axis=(0, .3, sgn), verts=16))
    parts.append(cyl(ctx, f'Reservatório de gás do amortecedor {label}', (db[0] + .03, db[1], db[2] + sgn * .05), .013, .07, m.anod_black, axis=FWD, verts=20))
    parts.append(rod_end(ctx, f'Olhal do amortecedor {label}', da, m.titanium, .009))
    parts.append(cube(ctx, f'Suporte do amortecedor na estrutura {label}', (db[0], db[1] - .02, db[2]), (.04, .012, .04), m.carbon_matte, bev=.002))
    return parts

def center_elements(ctx, P, front):
    """Elemento heave com pilha Belleville e barra antirrolagem entre os dois balancins."""
    m = ctx.m
    rk = P['rocker']; sgn = 1 if front else -1
    zc = rk[2] + sgn * .04; yc = rk[1] + .03
    lab = 'dianteiro' if front else 'traseiro'
    cyl(ctx, f'Elemento heave · corpo {lab}', (0, yc, zc), .019, .16, m.anod_black, axis=RIGHT, verts=24)
    cyl(ctx, f'Elemento heave · haste {lab}', (0, yc, zc), .006, .32, m.alu_bright, axis=RIGHT, verts=12)
    for i in range(10):
        x = .095 + i * .009
        cyl(ctx, f'Arruela Belleville {i + 1} {lab}', (x, yc, zc), .020, .0035, m.steel, axis=RIGHT, verts=24, radius2=.014 if i % 2 else .020)
    for side in (-1, 1):
        sphere(ctx, f'Rótula do heave no balancim {lab}', (side * .165, yc, zc), .008, m.titanium)
    # barra antirrolagem: tubo de torção transversal, lâminas ajustáveis e bieletas até os balancins
    za = rk[2] - sgn * .06; ya = rk[1] - .015
    cyl(ctx, f'Barra antirrolagem · tubo de torção {lab}', (0, ya, za), .011, .30, m.steel_dark, axis=RIGHT, verts=16)
    for side in (-1, 1):
        cube(ctx, f'Lâmina ajustável da barra antirrolagem {lab}', (side * .16, ya + .02, za), (.006, .05, .018), m.steel, bev=.001)
        sweep(ctx, f'Bieleta da barra antirrolagem {lab}', [(side * .16, ya + .045, za), (side * rk[0], rk[1], rk[2] - sgn * .02)], m.titanium, radius=.005, sides=10, smooth_path=False)
        cube(ctx, f'Mancal da barra antirrolagem {lab}', (side * .10, ya, za), (.03, .028, .028), m.alu, bev=.003)

def build(ctx):
    for axle, front, label in (('front', True, 'dianteiro direito'), ('rear', False, 'traseiro direito')):
        P = PICKUPS[axle]
        parts = corner(ctx, P, front, label)
        for p in parts:
            mirror_x(ctx, p, p['part'].replace('direito', 'esquerdo').replace('direita', 'esquerda'))
        center_elements(ctx, P, front)
