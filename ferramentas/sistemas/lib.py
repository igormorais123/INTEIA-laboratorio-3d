"""Biblioteca de modelagem procedural dos sistemas internos do carro (Blender 5.2, bpy + bmesh).

Convenção de coordenadas: TODO o código dos sistemas usa o referencial do site
(glTF: X direita, Y para cima, Z para a frente do carro, metros, piso em y=0).
Os helpers convertem para o referencial do Blender (Z para cima, -Y para a frente)
e o exportador glTF devolve o referencial do site.

Geometria original INTEIA, ilustrativa e didática; não é CAD de fabricante.
"""
import bpy, bmesh, math
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix, Quaternion

# ----------------------------------------------------------------------------- referencial
def W(x, y=None, z=None):
    """Ponto/vetor do site -> Blender."""
    if y is None:
        x, y, z = x
    return Vector((x, -z, y))

def to_web(v):
    return (round(v.x, 5), round(v.z, 5), round(-v.y, 5))

UP = (0, 1, 0)
FWD = (0, 0, 1)
RIGHT = (1, 0, 0)

# ----------------------------------------------------------------------------- texturas
_images = {}

def _encode_normal(height, strength=1.0):
    gy, gx = np.gradient(height.astype(np.float32))
    nx, ny = -gx * strength, -gy * strength
    nz = np.ones_like(nx)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    return np.stack([(nx / n) * .5 + .5, (ny / n) * .5 + .5, (nz / n) * .5 + .5, np.ones_like(nx)], -1)

def image_from_array(name, rgba, srgb=True):
    """rgba: float array (h, w, 4) em 0..1. Retorna bpy.types.Image empacotada."""
    if name in _images:
        return _images[name]
    h, w = rgba.shape[:2]
    img = bpy.data.images.new(name, width=w, height=h, alpha=True)
    img.colorspace_settings.name = 'sRGB' if srgb else 'Non-Color'
    img.pixels.foreach_set(np.ascontiguousarray(rgba, dtype=np.float32).ravel())
    img.pack()
    _images[name] = img
    return img

def tex_twill(size=256, tow=16, base=(.028, .032, .038), lift=.055):
    y, x = np.mgrid[0:size, 0:size]
    warp = ((x // tow + y // tow) % 4) < 2
    lane = np.where(warp, x % tow, y % tow) / (tow - 1)
    bright = np.sin(lane * math.pi) ** .6
    fibre = .5 + .5 * np.sin((np.where(warp, y, x) % tow) / tow * math.pi * 6)
    v = bright * lift + fibre * .010 + np.where(warp, .006, 0)
    col = np.stack([base[0] + v * .9, base[1] + v, base[2] + v * 1.15, np.ones_like(v)], -1)
    height = bright * .6 + np.where(warp, .15, 0)
    return image_from_array('Carbono sarja 2x2 · cor', np.clip(col, 0, 1)), image_from_array('Carbono sarja 2x2 · normal', _encode_normal(height, 1.4), False)

def tex_kevlar(size=256, tow=12):
    y, x = np.mgrid[0:size, 0:size]
    warp = ((x // tow + y // tow) % 2) == 0
    lane = np.where(warp, x % tow, y % tow) / (tow - 1)
    bright = np.sin(lane * math.pi) ** .7
    v = .55 + .35 * bright
    col = np.stack([v * .95, v * .78, v * .18, np.ones_like(v)], -1)
    return image_from_array('Kevlar · cor', np.clip(col, 0, 1)), image_from_array('Kevlar · normal', _encode_normal(bright, 1.0), False)

def tex_brushed(size=256):
    rng = np.random.default_rng(7)
    line = rng.random((size, 1)) * .35 + .55
    noise = rng.random((size, size)) * .08
    r = np.clip(np.repeat(line, size, 1) * .55 + noise + .08, 0, 1)
    return image_from_array('Alumínio escovado · rugosidade', np.stack([r, r, r, np.ones_like(r)], -1), False)

def tex_cast(size=256):
    rng = np.random.default_rng(3)
    h = rng.random((size, size))
    # Grão arredondado e periódico: evita os quadrados de 8 px do antigo mapa.
    for _ in range(4):
        h = (h * 4 + sum(np.roll(h, shift, axis) for axis in (0, 1) for shift in (-1, 1))) / 8
    h = (h - h.min()) / (h.max() - h.min())
    r = .42 + h * .16
    return image_from_array('Fundido · rugosidade', np.stack([r, r, r, np.ones_like(r)], -1), False), image_from_array('Fundido · normal', _encode_normal(h, .65), False)

def tex_heat(size=256):
    """Gradiente de pátina térmica de Inconel ao longo de U (0 = frio, 1 = quente)."""
    u = np.linspace(0, 1, size)
    stops = [(0.0, (.52, .50, .47)), (.22, (.62, .50, .30)), (.42, (.55, .32, .22)), (.62, (.42, .22, .40)), (.80, (.20, .27, .50)), (1.0, (.30, .36, .42))]
    col = np.zeros((size, 3))
    for i in range(len(stops) - 1):
        a, ca = stops[i]; b, cb = stops[i + 1]
        m = (u >= a) & (u <= b)
        t = ((u[m] - a) / (b - a))[:, None]
        col[m] = np.array(ca) * (1 - t) + np.array(cb) * t
    rgba = np.concatenate([np.repeat(col[None], 16, 0), np.ones((16, size, 1))], -1)
    return image_from_array('Inconel · pátina térmica', rgba)

def tex_brake_disc(size=512, rings=14, holes_per_ring=64, inner=.42):
    """Pista de atrito com grão e marcas concêntricas; ventilação é geometria radial."""
    y, x = np.mgrid[0:size, 0:size]
    cx = (x - size / 2) / (size / 2); cy = (y - size / 2) / (size / 2)
    r = np.sqrt(cx * cx + cy * cy)
    grain = np.random.default_rng(91).random((size, size))
    h = .1 * np.sin(r * 1100) + grain * .16
    col = .19 + h * .22
    rgba = np.stack([col * .95, col, col * 1.02, np.ones_like(col)], -1)
    return image_from_array('Disco carbono · pista de atrito', rgba), image_from_array('Disco carbono · normal', _encode_normal(h, .45), False)

def tex_fins(size=256, pitch=6):
    y, x = np.mgrid[0:size, 0:size]
    lane = (x % pitch) / (pitch - 1)
    v = .30 + .30 * np.sin(lane * math.pi)
    rgba = np.stack([v * .9, v * .95, v, np.ones_like(v)], -1)
    return image_from_array('Aletas · cor', rgba), image_from_array('Aletas · normal', _encode_normal(np.sin(lane * math.pi), 2.0), False)

def tex_honeycomb(size=256, cell=18):
    y, x = np.mgrid[0:size, 0:size]
    # padrão hexagonal aproximado por 3 famílias de linhas
    k = 2 * math.pi / cell
    v = np.cos(k * x) + np.cos(k * (x * .5 + y * .866)) + np.cos(k * (x * .5 - y * .866))
    wall = v > 1.35
    col = np.where(wall, .78, .58)
    rgba = np.stack([col * .95, col * .82, col * .48, np.ones_like(col)], -1)
    return image_from_array('Colmeia Nomex · cor', np.clip(rgba, 0, 1)), image_from_array('Colmeia Nomex · normal', _encode_normal(np.where(wall, 1.0, 0.0), 1.4), False)

def tex_kapton(size=256):
    rng = np.random.default_rng(11)
    h = rng.random((size // 6, size // 6))
    h = np.kron(h, np.ones((6, 6)))
    return image_from_array('Kapton · normal', _encode_normal(h, .8), False)

def tex_braid(size=128, tow=8):
    y, x = np.mgrid[0:size, 0:size]
    a = ((x + y) // tow) % 2 == 0
    lane = np.where(a, (x + y) % tow, (x - y) % tow) / (tow - 1)
    h = np.sin(lane * math.pi)
    return image_from_array('Trançado · normal', _encode_normal(h, 1.6), False)

def _seg7(img, ch, x0, y0, w, h, t, col):
    """Desenha um caractere de 7 segmentos (dígitos, ':' e '.'); origem (x0, y0) no canto inferior esquerdo (linha 0 da imagem Blender = base)."""
    on = {'0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd', '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg', '-': 'g'}.get(ch, '')
    H, Wd = img.shape[:2]
    def rect(xa, ya, xb, yb):
        img[max(0, ya):min(H, yb), max(0, xa):min(Wd, xb), :3] = col
    if ch == ':':
        rect(x0 + w // 2 - t // 2, y0 + h // 4 - t // 2, x0 + w // 2 + t // 2, y0 + h // 4 + t // 2)
        rect(x0 + w // 2 - t // 2, y0 + 3 * h // 4 - t // 2, x0 + w // 2 + t // 2, y0 + 3 * h // 4 + t // 2)
        return
    if ch == '.':
        rect(x0 + w // 2 - t // 2, y0, x0 + w // 2 + t // 2, y0 + t)
        return
    m = h // 2
    if 'a' in on: rect(x0, y0 + h - t, x0 + w, y0 + h)
    if 'd' in on: rect(x0, y0, x0 + w, y0 + t)
    if 'g' in on: rect(x0, y0 + m - t // 2, x0 + w, y0 + m + t // 2)
    if 'f' in on: rect(x0, y0 + m, x0 + t, y0 + h)
    if 'b' in on: rect(x0 + w - t, y0 + m, x0 + w, y0 + h)
    if 'e' in on: rect(x0, y0, x0 + t, y0 + m)
    if 'c' in on: rect(x0 + w - t, y0, x0 + w, y0 + m)

def _text7(img, text, x, y, w, h, t, col, gap=None):
    gap = gap if gap is not None else max(2, w // 3)
    for ch in text:
        cw = max(3, w // 3) if ch in ':.' else w
        _seg7(img, ch, x, y, cw, h, t, col)
        x += cw + gap

def tex_display(size=(512, 256)):
    """Página de telemetria estilo 2026: campos superiores, marcha central, tempos laterais e barra de energia."""
    w, h = size
    img = np.zeros((h, w, 4)); img[..., 3] = 1
    img[..., :3] = (.012, .014, .018)
    H = h
    def box(xa, ya, xb, yb, col):
        img[ya:yb, xa:xb, :3] = col
    cols = [(.15, .55, .25), (.70, .55, .10), (.20, .40, .80), (.75, .20, .20), (.55, .25, .70)]
    for i, c in enumerate(cols):
        xa = int(w * (.03 + i * .195)); xb = xa + int(w * .17)
        box(xa, int(h * .84), xb, int(h * .96), (.06, .07, .09))
        box(xa, int(h * .93), xb, int(h * .96), c)
        _text7(img, str((i * 3 + 2) % 10), xa + int(w * .06), int(h * .855), int(w * .035), int(h * .06), 3, (.85, .88, .9))
    box(int(w * .40), int(h * .16), int(w * .60), int(h * .80), (.03, .035, .045))
    _seg7(img, '7', int(w * .445), int(h * .22), int(w * .11), int(h * .52), int(h * .07), (.96, .96, .92))
    _text7(img, '1:28.4', int(w * .04), int(h * .62), int(w * .04), int(h * .11), 4, (.85, .9, .95))
    box(int(w * .04), int(h * .48), int(w * .36), int(h * .55), (.06, .07, .09))
    box(int(w * .20), int(h * .48), int(w * .31), int(h * .55), (.15, .85, .35))
    _text7(img, '-0.31', int(w * .04), int(h * .34), int(w * .035), int(h * .09), 3, (.15, .85, .35))
    _text7(img, '312', int(w * .04), int(h * .18), int(w * .045), int(h * .11), 4, (.85, .9, .95))
    _text7(img, '27', int(w * .66), int(h * .62), int(w * .05), int(h * .11), 4, (.85, .9, .95))
    _text7(img, '58', int(w * .82), int(h * .62), int(w * .05), int(h * .11), 4, (.6, .62, .66))
    for j, (val, c) in enumerate((('96', (.95, .6, .2)), ('112', (.3, .6, .95)), ('83', (.95, .3, .3)))):
        _text7(img, val, int(w * .66), int(h * (.44 - j * .13)), int(w * .03), int(h * .08), 3, c)
        box(int(w * .84), int(h * (.45 - j * .13)), int(w * .97), int(h * (.50 - j * .13)), (.06, .07, .09))
        box(int(w * .84), int(h * (.45 - j * .13)), int(w * (.84 + .13 * (.4 + .2 * j))), int(h * (.50 - j * .13)), c)
    for x in range(int(w * .04), int(w * .96)):
        f = (x - w * .04) / (w * .92)
        c = (min(1, 2 * f) * .9, min(1, 2 - 2 * f) * .85, .15)
        box(x, int(h * .05), x + 1, int(h * .12), c if f < .62 else (.05, .06, .08))
    return image_from_array('Display volante', np.clip(img, 0, 1))

# ----------------------------------------------------------------------------- materiais
_materials = {}

def material(name, color, metallic=0.0, roughness=0.45, *, emissive=None, emissive_strength=1.0, alpha=1.0,
             clearcoat=0.0, clearcoat_roughness=0.1, transmission=0.0, base_tex=None, normal_tex=None,
             normal_strength=1.0, rough_tex=None, uv_scale=1.0, emissive_tex=None, ior=1.45):
    if name in _materials:
        return _materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1)
    nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = roughness
    p.inputs['IOR'].default_value = ior
    if clearcoat:
        p.inputs['Coat Weight'].default_value = clearcoat
        p.inputs['Coat Roughness'].default_value = clearcoat_roughness
    if transmission:
        p.inputs['Transmission Weight'].default_value = transmission
    if alpha < 1:
        p.inputs['Alpha'].default_value = alpha
        m.blend_method = 'BLEND'
        m.surface_render_method = 'BLENDED'
    if emissive:
        p.inputs['Emission Color'].default_value = (*emissive, 1)
        p.inputs['Emission Strength'].default_value = emissive_strength
    mapping = None
    if base_tex or normal_tex or rough_tex or emissive_tex:
        coord = nt.nodes.new('ShaderNodeTexCoord')
        mapping = nt.nodes.new('ShaderNodeMapping')
        mapping.inputs['Scale'].default_value = (uv_scale, uv_scale, 1)
        nt.links.new(coord.outputs['UV'], mapping.inputs['Vector'])
    def tex_node(img):
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img
        nt.links.new(mapping.outputs['Vector'], t.inputs['Vector'])
        return t
    if base_tex:
        t = tex_node(base_tex)
        if color != (1, 1, 1):
            mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
            mix.inputs['Factor'].default_value = 1
            nt.links.new(t.outputs['Color'], mix.inputs[6]); mix.inputs[7].default_value = (*color, 1)
            nt.links.new(mix.outputs[2], p.inputs['Base Color'])
        else:
            nt.links.new(t.outputs['Color'], p.inputs['Base Color'])
    if normal_tex:
        t = tex_node(normal_tex)
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = normal_strength
        nt.links.new(t.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    if rough_tex:
        t = tex_node(rough_tex)
        nt.links.new(t.outputs['Color'], p.inputs['Roughness'])
    if emissive_tex:
        t = tex_node(emissive_tex)
        nt.links.new(t.outputs['Color'], p.inputs['Emission Color'])
        p.inputs['Emission Strength'].default_value = emissive_strength
    _materials[name] = m
    return m

class Materials:
    """Paleta física compartilhada pelos 14 sistemas."""
    def __init__(self):
        twill_c, twill_n = tex_twill()
        kev_c, kev_n = tex_kevlar()
        brushed = tex_brushed()
        cast_r, cast_n = tex_cast()
        heat = tex_heat()
        disc_c, disc_n = tex_brake_disc()
        fins_c, fins_n = tex_fins()
        hon_c, hon_n = tex_honeycomb()
        kapton_n = tex_kapton()
        braid_n = tex_braid()
        display = tex_display()
        self.carbon = material('Carbono · sarja 2x2 verniz', (1, 1, 1), 0, .28, clearcoat=1, clearcoat_roughness=.08, base_tex=twill_c, normal_tex=twill_n, normal_strength=.6, uv_scale=24)
        self.carbon_matte = material('Carbono · sarja fosca', (.9, .9, .9), 0, .62, clearcoat=.15, clearcoat_roughness=.4, base_tex=twill_c, normal_tex=twill_n, normal_strength=.8, uv_scale=24)
        self.carbon_fine = material('Carbono · tecido fino', (1, 1, 1), 0, .34, clearcoat=.8, clearcoat_roughness=.12, base_tex=twill_c, normal_tex=twill_n, normal_strength=.5, uv_scale=48)
        self.kevlar = material('Kevlar · aramida amarela', (1, 1, 1), 0, .72, base_tex=kev_c, normal_tex=kev_n, normal_strength=.7, uv_scale=30)
        self.alu = material('Alumínio usinado', (.80, .82, .84), 1, .30, rough_tex=brushed, uv_scale=6)
        self.alu_bright = material('Alumínio polido', (.88, .89, .90), 1, .16)
        self.alu_cast = material('Alumínio fundido', (.62, .64, .66), .95, .55, rough_tex=cast_r, normal_tex=cast_n, normal_strength=.5, uv_scale=8)
        self.mag_cast = material('Magnésio fundido · cinza quente', (.55, .53, .50), .9, .6, rough_tex=cast_r, normal_tex=cast_n, normal_strength=.6, uv_scale=8)
        self.titanium = material('Titânio Ti-6Al-4V', (.62, .60, .57), 1, .42, rough_tex=brushed, uv_scale=8)
        self.titanium_blue = material('Titânio · têmpera azulada', (.45, .50, .62), 1, .38)
        self.steel = material('Aço forjado', (.42, .43, .45), 1, .36)
        self.steel_dark = material('Aço · fosfatizado', (.16, .17, .19), .9, .5)
        self.gear = material('Aço cementado · engrenagens', (.66, .66, .64), 1, .26)
        self.inconel = material('Inconel · pátina térmica', (1, 1, 1), 1, .36, base_tex=heat, uv_scale=1)
        self.inconel_plain = material('Inconel · brilho quente', (.60, .56, .50), 1, .34)
        self.anod_black = material('Alumínio anodizado preto', (.05, .055, .06), .8, .38)
        self.anod_red = material('Anodizado vermelho INTEIA', (.55, .02, .03), .7, .3)
        self.anod_blue = material('Anodizado azul', (.05, .18, .55), .7, .32)
        self.anod_gold = material('Anodizado dourado', (.70, .48, .16), .85, .3)
        self.anod_green = material('Anodizado verde', (.10, .55, .12), .7, .32)
        self.anod_yellow = material('Anodizado amarelo', (.85, .70, .05), .7, .3)
        self.anod_orange = material('Anodizado laranja', (.85, .32, .04), .7, .3)
        self.anod_purple = material('Anodizado roxo', (.32, .08, .55), .7, .32)
        self.anod_cyan = material('Anodizado ciano', (.05, .55, .65), .7, .32)
        self.grip = material('Empunhadura · borracha texturizada', (.03, .03, .032), 0, .82, normal_tex=cast_n, normal_strength=.3, uv_scale=12)
        self.led_white = material('LED branco', (1, 1, .95), 0, .3, emissive=(1, 1, .9), emissive_strength=3)
        self.button_white = material('Botão branco', (.85, .85, .82), 0, .35)
        self.button_black = material('Botão preto', (.06, .06, .065), 0, .45)
        self.rubber = material('Borracha preta', (.02, .02, .022), 0, .82)
        self.silicone = material('Silicone azul · mangueira', (.06, .22, .55), 0, .55)
        self.silicone_black = material('Silicone preto · mangueira', (.03, .03, .035), 0, .6)
        self.braid = material('Mangueira trançada em aço', (.70, .72, .74), .9, .45, normal_tex=braid_n, normal_strength=1.0, uv_scale=40)
        self.hv = material('Cabo de alta tensão · laranja', (.95, .30, .02), 0, .5)
        self.cable = material('Cabo · isolamento preto', (.03, .03, .03), 0, .65)
        self.copper = material('Cobre · enrolamentos', (.78, .42, .22), 1, .4)
        self.brake_disc = material('Disco carbono-carbono', (1, 1, 1), 0, .85, base_tex=disc_c, normal_tex=disc_n, normal_strength=1.0, uv_scale=1)
        self.brake_pad = material('Pastilha carbono', (.12, .11, .10), 0, .9)
        self.glass = material('Policarbonato', (.85, .9, .95), 0, .05, transmission=.92, alpha=.35, ior=1.5)
        self.glass_tint = material('Vidro fumê', (.1, .12, .14), 0, .05, transmission=.7, alpha=.6, ior=1.5)
        self.fuel = material('Bexiga de combustível · Kevlar/nitrílica', (1, 1, 1), 0, .6, alpha=.62, base_tex=kev_c, normal_tex=kev_n, normal_strength=.4, uv_scale=28)
        self.fuel_liquid = material('Gasolina · líquido', (.85, .62, .12), 0, .05, transmission=.9, alpha=.45, ior=1.42)
        self.pcb = material('Placa de circuito', (.02, .22, .10), 0, .5)
        self.led_green = material('LED verde', (.1, .9, .2), 0, .3, emissive=(.1, 1, .2), emissive_strength=4)
        self.led_red = material('LED vermelho', (.95, .1, .1), 0, .3, emissive=(1, .1, .05), emissive_strength=4)
        self.led_blue = material('LED azul', (.2, .3, 1), 0, .3, emissive=(.2, .35, 1), emissive_strength=4)
        self.led_amber = material('LED âmbar', (1, .6, .1), 0, .3, emissive=(1, .55, .05), emissive_strength=3)
        self.display = material('Display · LCD', (.02, .02, .02), 0, .2, emissive_tex=display, emissive_strength=2.2)
        self.kapton = material('Manta térmica dourada', (.78, .56, .18), .85, .32, normal_tex=kapton_n, normal_strength=.9, uv_scale=12)
        self.honeycomb = material('Colmeia Nomex · núcleo', (1, 1, 1), 0, .7, base_tex=hon_c, normal_tex=hon_n, normal_strength=1.0, uv_scale=20)
        self.foam = material('Espuma antichama', (.06, .06, .07), 0, .95)
        self.nomex = material('Tecido Nomex · azul marinho', (.06, .08, .18), 0, .85, normal_tex=braid_n, normal_strength=.25, uv_scale=35)
        self.webbing = material('Cadarço do arnês', (.05, .08, .35), 0, .8, normal_tex=braid_n, normal_strength=.3, uv_scale=40)
        self.paint_red = material('Pintura INTEIA vermelha', (.62, .03, .05), 0, .25, clearcoat=1, clearcoat_roughness=.06)
        self.paint_white = material('Pintura branca', (.9, .9, .88), 0, .3, clearcoat=.8)
        self.radiator = material('Núcleo de radiador · aletas', (1, 1, 1), 1, .55, base_tex=fins_c, normal_tex=fins_n, normal_strength=1.0, uv_scale=60)
        self.zylon = material('Cabo Zylon · retenção', (.95, .78, .30), 0, .6)
        self.plank = material('Plank · compósito de madeira', (.40, .27, .13), 0, .75, rough_tex=brushed, uv_scale=4)
        self.brass = material('Latão', (.75, .60, .30), 1, .35)
        self.plastic_black = material('Plástico preto · conectores', (.04, .04, .045), 0, .5)
        self.plastic_grey = material('Plástico cinza', (.35, .36, .38), 0, .55)
        self.oil = material('Óleo · reservatório', (.55, .32, .06), 0, .1, transmission=.8, alpha=.5)
        self.coolant = material('Líquido de arrefecimento', (.2, .6, .9), 0, .1, transmission=.8, alpha=.5)
        self.flow = {
            'air': material('Fluxo · ar', (.9, .95, 1), 0, .4, emissive=(.75, .9, 1), emissive_strength=1.5, alpha=.55),
            'charge': material('Fluxo · ar comprimido', (1, .85, .6), 0, .4, emissive=(1, .8, .5), emissive_strength=1.5, alpha=.55),
            'exhaust': material('Fluxo · escape', (1, .5, .2), 0, .4, emissive=(1, .45, .15), emissive_strength=1.8, alpha=.55),
            'water': material('Fluxo · água', (.3, .7, 1), 0, .4, emissive=(.3, .7, 1), emissive_strength=1.6, alpha=.55),
            'oil': material('Fluxo · óleo', (.9, .6, .15), 0, .4, emissive=(1, .65, .1), emissive_strength=1.6, alpha=.55),
            'fuel': material('Fluxo · combustível', (1, .8, .2), 0, .4, emissive=(1, .8, .2), emissive_strength=1.6, alpha=.55),
            'hv': material('Fluxo · energia elétrica', (1, .55, .1), 0, .4, emissive=(1, .6, .1), emissive_strength=2.2, alpha=.6),
            'hyd': material('Fluxo · hidráulica', (.8, .4, 1), 0, .4, emissive=(.8, .45, 1), emissive_strength=1.6, alpha=.55),
            'data': material('Fluxo · dados', (.4, 1, .9), 0, .4, emissive=(.4, 1, .9), emissive_strength=2.0, alpha=.6),
            'brake': material('Fluxo · fluido de freio', (1, .3, .3), 0, .4, emissive=(1, .3, .3), emissive_strength=1.8, alpha=.55),
        }

# ----------------------------------------------------------------------------- contexto / registro
class Context:
    def __init__(self, scene, mats):
        self.scene = scene
        self.m = mats
        self.systems = {}
        self.parts = []
        self.current = None
        self.counter = 0

    def system(self, sid, label):
        e = bpy.data.objects.new(f'system_{sid}', None)
        e.empty_display_size = .05
        e['system'] = sid
        e['label'] = label
        self.scene.collection.objects.link(e)
        self.systems[sid] = e
        self.current = e
        return e

    def register(self, obj, part, *, spin=None, spin_axis='y', flow=None, era=None, explode=None, hide_group=None, tag=None, carrier=False, parent=None):
        """Registra uma malha como peça nomeada do sistema corrente com extras exportados.
        carrier=True marca tubos/eixos que conduzem um fluxo: o site os torna translúcidos com os fluxos ligados."""
        # Trama em escala métrica em todos os sistemas, sem multiplicar novamente
        # por UVs diferentes de cubos, lofts e tubos. Texturas de fluxo ficam intactas.
        if obj.type == 'MESH' and any(m and m.name.startswith(('Carbono ·', 'Kevlar ·', 'Tecido Nomex', 'Cadarço', 'Empunhadura')) for m in obj.data.materials):
            box_uv(obj, 1)
        self.counter += 1
        sid = self.current['system']
        obj.name = f'{sid}__{self.counter:03d}__{part}'[:63]
        obj['part'] = part
        obj['system'] = sid
        if spin is not None:
            obj['spin'] = float(spin); obj['spin_axis'] = spin_axis
        if flow:
            obj['flow'] = flow
        if carrier:
            obj['carrier'] = 1
        if era:
            obj['era'] = era
        if explode is not None:
            obj['explode'] = [float(c) for c in explode]
        if hide_group:
            obj['hide_group'] = hide_group
        if tag:
            obj['tag'] = tag
        obj.parent = parent or self.current
        self.parts.append(obj)
        return obj

# ----------------------------------------------------------------------------- utilidades de malha
def _link(obj):
    bpy.context.scene.collection.objects.link(obj)
    return obj

def shade_smooth(obj, angle=math.radians(38)):
    if obj.type != 'MESH':
        return obj
    for p in obj.data.polygons:
        p.use_smooth = True
    if not any(m.type == 'SMOOTH_BY_ANGLE' for m in obj.modifiers):
        try:
            bpy.context.view_layer.objects.active = obj
            with bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj]):
                bpy.ops.object.shade_smooth_by_angle(angle=angle)
        except Exception:
            pass
    return obj

def bevel(obj, width=.002, segments=2, angle=math.radians(40)):
    if obj.type != 'MESH' or width <= 0:
        return obj
    m = obj.modifiers.new('Raio usinado', 'BEVEL')
    m.width = width; m.segments = segments; m.limit_method = 'ANGLE'; m.angle_limit = angle
    m.harden_normals = True
    return obj

def box_uv(obj, scale=1.0, offset=(0.0, 0.0)):
    """Projeção em caixa (triplanar discreta) para texturas de trama."""
    me = obj.data
    if not me.uv_layers:
        me.uv_layers.new(name='UVMap')
    uv = me.uv_layers.active.data
    for poly in me.polygons:
        n = poly.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if ax == 0:
                u, v = co.y, co.z
            elif ax == 1:
                u, v = co.x, co.z
            else:
                u, v = co.x, co.y
            uv[li].uv = (u * scale + offset[0], v * scale + offset[1])
    return obj

def mesh_object(name, verts, faces, edges=(), uvs=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([Vector(v) for v in verts], list(edges), list(faces))
    me.update()
    obj = bpy.data.objects.new(name, me)
    _link(obj)
    if uvs is not None:
        layer = me.uv_layers.new(name='UVMap')
        for li, loop in enumerate(me.loops):
            layer.data[li].uv = uvs[li]
    return obj

def bm_to_object(name, bm, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free(); me.update()
    obj = bpy.data.objects.new(name, me)
    _link(obj)
    if smooth:
        shade_smooth(obj)
    return obj

def set_material(obj, mat):
    if obj.type == 'MESH':
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return obj

def orient(obj, axis):
    """Alinha o eixo local Z do objeto (Blender) ao vetor `axis` dado no referencial do site."""
    d = W(axis).normalized()
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = d.to_track_quat('Z', 'Y')
    return obj

# ----------------------------------------------------------------------------- primitivas (site frame)
def cube(ctx, part, center, size, mat, *, bev=.002, segments=2, rot=None, uv=None, **extras):
    bpy.ops.mesh.primitive_cube_add(size=1, location=W(center))
    o = bpy.context.object
    o.scale = (size[0], size[2], size[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if rot:
        o.rotation_euler = W_rot(rot)
    set_material(o, mat)
    if uv:
        box_uv(o, uv)
    bevel(o, bev, segments)
    shade_smooth(o)
    return ctx.register(o, part, **extras)

def W_rot(rot):
    """Euler (rx, ry, rz) em graus no referencial do site -> Euler Blender."""
    rx, ry, rz = [math.radians(a) for a in rot]
    m = Matrix.Rotation(rx, 3, W(RIGHT)) @ Matrix.Rotation(ry, 3, W(UP)) @ Matrix.Rotation(rz, 3, W(FWD))
    return m.to_euler()

def cyl(ctx, part, center, radius, length, mat, *, axis=UP, verts=32, bev=.0012, segments=2, radius2=None, **extras):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=radius, radius2=radius if radius2 is None else radius2, depth=length, location=W(center))
    o = bpy.context.object
    orient(o, axis)
    set_material(o, mat)
    bevel(o, min(bev, radius * .2), segments)
    shade_smooth(o)
    return ctx.register(o, part, **extras)

def tube_cyl(ctx, part, center, radius, wall, length, mat, *, axis=UP, verts=32, **extras):
    """Cilindro oco (tubo curto) com paredes."""
    bm = bmesh.new()
    ro, ri = radius, radius - wall
    for r in (ro, ri):
        ring = [bm.verts.new((r * math.cos(2 * math.pi * i / verts), r * math.sin(2 * math.pi * i / verts), -length / 2)) for i in range(verts)]
    bm.verts.ensure_lookup_table()
    outer = bm.verts[:verts]; inner = bm.verts[verts:]
    top_o = [bm.verts.new((v.co.x, v.co.y, length / 2)) for v in outer]
    top_i = [bm.verts.new((v.co.x, v.co.y, length / 2)) for v in inner]
    for i in range(verts):
        j = (i + 1) % verts
        bm.faces.new((outer[i], outer[j], top_o[j], top_o[i]))
        bm.faces.new((inner[j], inner[i], top_i[i], top_i[j]))
        bm.faces.new((outer[j], outer[i], inner[i], inner[j]))
        bm.faces.new((top_o[i], top_o[j], top_i[j], top_i[i]))
    o = bm_to_object(part, bm)
    box_uv(o, 1)
    o.location = W(center); orient(o, axis)
    set_material(o, mat)
    return ctx.register(o, part, **extras)

def sphere(ctx, part, center, radius, mat, *, segments=24, rings=16, scale=None, **extras):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=W(center))
    o = bpy.context.object
    if scale:
        o.scale = (scale[0], scale[2], scale[1])
    set_material(o, mat); shade_smooth(o)
    return ctx.register(o, part, **extras)

def torus(ctx, part, center, major, minor, mat, *, axis=UP, seg=40, mseg=12, **extras):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=seg, minor_segments=mseg, location=W(center))
    o = bpy.context.object
    orient(o, axis); set_material(o, mat); shade_smooth(o)
    return ctx.register(o, part, **extras)

# ----------------------------------------------------------------------------- tubos, lofts, hélices
def catmull(points, per_segment=8, closed=False):
    P = [Vector(p) for p in points]
    if len(P) < 3:
        return P
    out = []
    n = len(P)
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        a = P[(i - 1) % n] if closed else P[max(0, i - 1)]
        b = P[i]; c = P[(i + 1) % n]
        d = P[(i + 2) % n] if closed else P[min(n - 1, i + 2)]
        for j in range(per_segment):
            t = j / per_segment
            out.append(.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t ** 3))
    if not closed:
        out.append(P[-1])
    return out

def _frames(pts, closed=False):
    """Quadros paralelos (rotation-minimizing) ao longo da polilinha."""
    tangents = []
    n = len(pts)
    for i in range(n):
        a = pts[(i - 1) % n] if closed else pts[max(0, i - 1)]
        b = pts[(i + 1) % n] if closed else pts[min(n - 1, i + 1)]
        t = (b - a)
        tangents.append(t.normalized() if t.length > 1e-9 else Vector((0, 0, 1)))
    t0 = tangents[0]
    ref = Vector((0, 0, 1)) if abs(t0.z) < .9 else Vector((1, 0, 0))
    u = t0.cross(ref).normalized()
    frames = []
    for i, t in enumerate(tangents):
        if i:
            # transporte paralelo
            u = (u - t * u.dot(t))
            if u.length < 1e-6:
                ref = Vector((0, 0, 1)) if abs(t.z) < .9 else Vector((1, 0, 0))
                u = t.cross(ref)
            u.normalize()
        v = t.cross(u).normalized()
        frames.append((u, v))
    return frames

def sweep(ctx, part, points, mat, *, radius=.01, radii=None, sides=14, smooth_path=True, per_segment=8,
          section=None, closed=False, cap=True, uv_len=1.0, twist=0.0, open_section=False, thickness=0.0, **extras):
    """Varre uma seção (círculo por padrão, ou função t->[(x,y)...]) ao longo de pontos no referencial do site."""
    P = [W(p) for p in points]
    if smooth_path and len(P) >= 3:
        P = catmull(P, per_segment, closed)
        if radii is not None:
            # reamostra os raios linearmente
            src = np.linspace(0, 1, len(radii)); dst = np.linspace(0, 1, len(P))
            radii = list(np.interp(dst, src, radii))
    frames = _frames(P, closed)
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new('UVMap')
    rings = []
    dist = 0.0
    dists = []
    for i, p in enumerate(P):
        if i:
            dist += (P[i] - P[i - 1]).length
        dists.append(dist)
        u, v = frames[i]
        r = radii[i] if radii is not None else radius
        t = i / max(1, len(P) - 1)
        if section:
            pts2 = section(t)
        else:
            pts2 = [(r * math.cos(2 * math.pi * k / sides + twist * t), r * math.sin(2 * math.pi * k / sides + twist * t)) for k in range(sides)]
        rings.append([bm.verts.new(p + u * x + v * y) for x, y in pts2])
    total = max(dist, 1e-6)
    count = len(rings)
    seg_range = range(count) if closed else range(count - 1)
    ns = len(rings[0])
    for i in seg_range:
        a = rings[i]; b = rings[(i + 1) % count]
        for k in range(ns - 1 if open_section else ns):
            k2 = (k + 1) % ns
            try:
                f = bm.faces.new((a[k], a[k2], b[k2], b[k]))
            except ValueError:
                continue
            for loop, (ii, kk) in zip(f.loops, ((i, k), (i, k2), ((i + 1) % count, k2), ((i + 1) % count, k))):
                loop[uv_layer].uv = (kk / ns, dists[ii] / total * uv_len)
    if cap and not closed and not open_section:
        for ring, rev in ((rings[0], True), (rings[-1], False)):
            try:
                f = bm.faces.new(list(reversed(ring)) if rev else ring)
                for loop in f.loops:
                    loop[uv_layer].uv = (0, 0)
            except ValueError:
                pass
    bm.normal_update()
    o = bm_to_object(part, bm)
    set_material(o, mat)
    if thickness:
        md = o.modifiers.new('Espessura', 'SOLIDIFY'); md.thickness = thickness; md.offset = 0
    return ctx.register(o, part, **extras)

def airfoil(chord, thick, camber=0.0, n=18):
    """Seção tipo NACA simétrica (com leve arqueamento) para braços de suspensão e asas. Retorna [(x,y)] fechado."""
    pts = []
    for i in range(n + 1):
        b = math.pi * i / n
        x = .5 * (1 - math.cos(b))
        yt = 5 * thick * (.2969 * math.sqrt(x) - .1260 * x - .3516 * x * x + .2843 * x ** 3 - .1036 * x ** 4)
        yc = camber * 4 * x * (1 - x)
        pts.append(((x - .5) * chord, (yt + yc) * chord))
    for i in range(n - 1, 0, -1):
        b = math.pi * i / n
        x = .5 * (1 - math.cos(b))
        yt = 5 * thick * (.2969 * math.sqrt(x) - .1260 * x - .3516 * x * x + .2843 * x ** 3 - .1036 * x ** 4)
        yc = camber * 4 * x * (1 - x)
        pts.append(((x - .5) * chord, (yc - yt) * chord))
    return pts

def loft(ctx, part, sections, mat, *, cap=True, open_ring=False, **extras):
    """sections: lista de anéis 3D (site frame), mesmo número de pontos, em ordem. open_ring=True não fecha o anel."""
    bm = bmesh.new()
    rings = [[bm.verts.new(W(p)) for p in ring] for ring in sections]
    ns = len(rings[0])
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        for k in range(ns - 1 if open_ring else ns):
            k2 = (k + 1) % ns
            try:
                bm.faces.new((a[k], a[k2], b[k2], b[k]))
            except ValueError:
                pass
    if cap and not open_ring:
        for ring, rev in ((rings[0], True), (rings[-1], False)):
            try:
                bm.faces.new(list(reversed(ring)) if rev else ring)
            except ValueError:
                pass
    bm.normal_update()
    o = bm_to_object(part, bm)
    box_uv(o, 8)
    set_material(o, mat)
    return ctx.register(o, part, **extras)

def lathe(ctx, part, profile, mat, *, center=(0, 0, 0), axis=UP, segments=40, **extras):
    """Revolve um perfil [(raio, altura)] em torno do eixo local Z (altura) e alinha ao `axis`."""
    bm = bmesh.new()
    prof = [bm.verts.new((r, 0, h)) for r, h in profile]
    edges = [bm.edges.new((prof[i], prof[i + 1])) for i in range(len(prof) - 1)]
    bmesh.ops.spin(bm, geom=prof + edges, cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=segments, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.normal_update()
    o = bm_to_object(part, bm)
    box_uv(o, 10)
    o.location = W(center); orient(o, axis)
    set_material(o, mat)
    return ctx.register(o, part, **extras)

def ventilated_disc(ctx, part, center, inner, outer, mat, *, front=True, **extras):
    """Anel com canais radiais abertos, pistas sólidas e furos na borda, sem booleanos."""
    count, rows = (144, 7) if front else (120, 5)
    half = .016; end_skin = .0017; pitch = (2*half-2*end_skin)/rows
    verts=[]; faces=[]
    def point(r, angle, z):
        verts.append((r*math.cos(angle),r*math.sin(angle),z)); return len(verts)-1
    for i in range(count):
        mid=2*math.pi*(i+.5)/count; da=math.pi/count
        for row in range(rows):
            z=-half+end_skin+pitch*(row+.5)
            border=[(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
            loops=[]
            for r in (outer,inner):
                outside=[point(r,mid+u*da,z+v*pitch*.5) for u,v in border]
                hole=[point(r,mid+.0016/r*math.cos(-3*math.pi/4+k*math.pi/4),z+.0016*math.sin(-3*math.pi/4+k*math.pi/4)) for k in range(8)]
                loops.append(hole)
                for k in range(8):
                    j=(k+1)%8; faces.append((outside[k],outside[j],hole[j],hole[k]))
            for k in range(8):
                j=(k+1)%8;faces.append((loops[0][k],loops[0][j],loops[1][j],loops[1][k]))
        # Faixas sólidas nas duas pistas e bordas externas/internas da pele.
        for sign in (-1,1):
            z=sign*half; inside=sign*(half-end_skin)
            for a0,a1 in [(mid-da,mid),(mid,mid+da)]:
                faces.append(tuple(point(r,a,z) for r,a in [(inner,a0),(outer,a0),(outer,a1),(inner,a1)]))
                for r in (inner,outer):
                    faces.append((point(r,a0,z),point(r,a1,z),point(r,a1,inside),point(r,a0,inside)))
    o=mesh_object(part,verts,faces)
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=1e-6)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
    check=bmesh.new();check.from_mesh(o.data)
    assert all(e.is_manifold for e in check.edges), f'Disco com borda aberta: {part}'
    check.free()
    shade_smooth(o,math.radians(30));box_uv(o,1/(2*outer),(.5,.5))
    o.location=W(center);orient(o,RIGHT);set_material(o,mat)
    o['ventilation_channels']=count*rows
    return ctx.register(o,part,**extras)


def helix(ctx, part, center, radius, pitch, turns, wire, mat, *, axis=UP, per_turn=28, **extras):
    pts = []
    n = int(turns * per_turn)
    for i in range(n + 1):
        a = 2 * math.pi * i / per_turn
        pts.append((radius * math.cos(a), pitch * i / per_turn - pitch * turns / 2, radius * math.sin(a)))
    o = sweep(ctx, part, pts, mat, radius=wire, sides=10, smooth_path=False, **extras)
    o.location = W(center); orient(o, axis)
    return o

def gear(ctx, part, center, teeth, module, width, mat, *, axis=UP, bore=None, helix_deg=0, hub_r=None, hub_w=None, spokes=0, **extras):
    """Engrenagem cilíndrica de dentes retos (perfil trapezoidal aproximado). Eixo local Z = eixo de rotação."""
    rp = module * teeth / 2
    ra = rp + module
    rf = rp - 1.25 * module
    bore = bore if bore is not None else max(rf * .35, module * 2)
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new('UVMap')
    outer = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a0 = i * step
        # raiz -> flanco -> topo -> flanco -> raiz
        for frac, r in ((0.0, rf), (0.16, rf), (0.30, ra), (0.50, ra), (0.64, rf), (0.80, rf)):
            a = a0 + frac * step
            outer.append((r * math.cos(a), r * math.sin(a)))
    def ring(z, pts):
        return [bm.verts.new((x, y, z)) for x, y in pts]
    inner_pts = [(bore * math.cos(2 * math.pi * i / (teeth * 2)), bore * math.sin(2 * math.pi * i / (teeth * 2))) for i in range(teeth * 2)]
    z0, z1 = -width / 2, width / 2
    o0 = ring(z0, outer); o1 = ring(z1, outer)
    i0 = ring(z0, inner_pts); i1 = ring(z1, inner_pts)
    no = len(outer); ni = len(inner_pts)
    for k in range(no):
        k2 = (k + 1) % no
        bm.faces.new((o0[k], o0[k2], o1[k2], o1[k]))
    for k in range(ni):
        k2 = (k + 1) % ni
        bm.faces.new((i0[k2], i0[k], i1[k], i1[k2]))
    # faces laterais: fatias entre externo (6 por dente) e interno (2 por dente)
    for t in range(teeth):
        for half in range(2):
            ia = t * 2 + half; ib = (ia + 1) % ni
            oa = t * 6 + half * 3
            seg0 = [o0[(oa + s) % no] for s in range(4)]
            seg1 = [o1[(oa + s) % no] for s in range(4)]
            bm.faces.new([i0[ib], i0[ia]] + seg0)
            bm.faces.new([i1[ia], i1[ib]] + seg1[::-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if helix_deg:
        for v in bm.verts:
            ang = math.tan(math.radians(helix_deg)) * v.co.z / rp
            x, y = v.co.x, v.co.y
            v.co.x = x * math.cos(ang) - y * math.sin(ang); v.co.y = x * math.sin(ang) + y * math.cos(ang)
    bm.normal_update()
    o = bm_to_object(part, bm)
    box_uv(o, 12)
    bevel(o, module * .12, 1)
    o.location = W(center); orient(o, axis)
    set_material(o, mat)
    return ctx.register(o, part, **extras)

def bolt_ring(ctx, part, center, radius, count, axis, mat_head, *, size=.006, head=.004, start=0.0, **extras):
    """Fixadores com arruela, chanfros e encaixe sextavado rebaixado; uma malha por anel."""
    d = Vector(axis).normalized()
    # base ortonormal no site frame
    ref = Vector((0, 1, 0)) if abs(d.y) < .9 else Vector((1, 0, 0))
    u = d.cross(ref).normalized(); v = d.cross(u).normalized()
    bm = bmesh.new()
    for i in range(count):
        a = start + 2 * math.pi * i / count
        c = Vector(center) + u * radius * math.cos(a) + v * radius * math.sin(a)
        z = size * .23; top = z + head
        profile = [(1.24, 0, False), (1.35, size*.08, False), (1.35, z*.7, False),
                   (1.24, z, False), (.87, z, False), (.87, top-head*.18, False),
                   (.74, top, False), (.42, top, True), (.36, top-head*.18, True),
                   (.36, z+head*.30, True)]
        rings = []
        for r, height, hexagonal in profile:
            ring=[]
            for k in range(24):
                angle=2*math.pi*k/24
                rr=size*r*(math.cos(math.pi/6)/math.cos((angle % (math.pi/3))-math.pi/6) if hexagonal else 1)
                ring.append(bm.verts.new(W(c+d*height+u*rr*math.cos(angle)+v*rr*math.sin(angle))))
            rings.append(ring)
        for ring0,ring1 in zip(rings,rings[1:]):
            for k in range(24):
                j=(k+1)%24; bm.faces.new((ring0[k],ring0[j],ring1[j],ring1[k]))
        bm.faces.new(rings[-1]); bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_object(part, bm, smooth=False)
    box_uv(o, 1)
    shade_smooth(o, math.radians(32))
    set_material(o, mat_head)
    return ctx.register(o, part, **extras)

def join(ctx, objects, part=None, **extras):
    """Une malhas em uma só peça (aplica modificadores antes)."""
    objects = [o for o in objects if o and o.type == 'MESH']
    if not objects:
        return None
    for o in objects:
        bpy.context.view_layer.objects.active = o
        for mod in list(o.modifiers):
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception:
                o.modifiers.remove(mod)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    joined = bpy.context.object
    for o in objects[1:]:
        if o in ctx.parts:
            ctx.parts.remove(o)
    if part:
        ctx.parts.remove(joined) if joined in ctx.parts else None
        ctx.register(joined, part, **extras)
    return joined

def mirror_x(ctx, obj, part=None):
    """Duplica a peça espelhada em X (site) mantendo materiais e extras."""
    dup = obj.copy(); dup.data = obj.data.copy()
    _link(dup)
    dup.parent = obj.parent
    mw = obj.matrix_world.copy()
    dup.matrix_world = Matrix.Scale(-1, 4, Vector((1, 0, 0))) @ mw
    dup.name = (part or obj.get('part', 'peça')) + ' (espelho)'
    for k in obj.keys():
        dup[k] = obj[k]
    if part:
        dup['part'] = part
    ex = obj.get('explode')
    if ex is not None:
        dup['explode'] = [-ex[0], ex[1], ex[2]]
    ctx.parts.append(dup)
    # normais invertidas pela escala negativa: aplica escala e recalcula
    bpy.context.view_layer.objects.active = dup
    bpy.ops.object.select_all(action='DESELECT'); dup.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bm = bmesh.new(); bm.from_mesh(dup.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(dup.data); bm.free()
    return dup

def mirror_system(ctx, sid):
    """Espelha em X, no lugar, todas as peças de um sistema. Usado nos módulos escritos na convenção legada
    (−X rotulado como esquerda): o piloto olha para +Z, logo a esquerda real do carro é +X."""
    objs = [p for p in ctx.parts if p.get('system') == sid and p.type == 'MESH']
    if not objs:
        return None
    S = Matrix.Scale(-1, 4, Vector((1, 0, 0)))
    for o in objs:
        o.matrix_world = S @ o.matrix_world
        ex = o.get('explode')
        if ex is not None:
            o['explode'] = [-float(ex[0]), float(ex[1]), float(ex[2])]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # Descobre se a aplicação da escala negativa já inverteu as faces: testa o volume assinado de uma malha fechada.
    flip = None
    for o in objs:
        bm = bmesh.new(); bm.from_mesh(o.data)
        if len(bm.faces) > 4 and all(e.is_manifold for e in bm.edges):
            flip = bm.calc_volume(signed=True) < 0
            bm.free(); break
        bm.free()
    if flip:
        for o in objs:
            bm = bmesh.new(); bm.from_mesh(o.data)
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
            bm.to_mesh(o.data); bm.free(); o.data.update()
    return flip

def both_sides(fn):
    """Executa fn(side) para side em (-1, +1)."""
    return [fn(-1), fn(1)]

def hexagon(r):
    return [(r * math.cos(math.pi / 3 * i), r * math.sin(math.pi / 3 * i)) for i in range(6)]

def rounded_rect(w, h, r, n=4):
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, math.pi / 2), (-w / 2 + r, -h / 2 + r, math.pi), (w / 2 - r, -h / 2 + r, 3 * math.pi / 2)):
        for i in range(n + 1):
            a = a0 + (math.pi / 2) * i / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def super_ellipse(w, h, n=2.6, seg=32, exp=None):
    exp = exp or n
    pts = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        c, s = math.cos(a), math.sin(a)
        pts.append((math.copysign(abs(c) ** (2 / exp), c) * w / 2, math.copysign(abs(s) ** (2 / exp), s) * h / 2))
    return pts

def shell(ctx, part, sections, mat, *, thickness=.004, open_ring=False, **extras):
    """Loft aberto com espessura (modificador Solidify)."""
    o = loft(ctx, part, sections, mat, cap=False, open_ring=open_ring, **extras)
    m = o.modifiers.new('Espessura', 'SOLIDIFY'); m.thickness = thickness; m.offset = -1
    return o

def flow_ribbon(ctx, part, points, kind, *, radius=.006, **extras):
    """Fita translúcida de fluxo (o site anima o deslocamento da textura)."""
    return sweep(ctx, part, points, ctx.m.flow[kind], radius=radius, sides=8, uv_len=8, flow=kind, **extras)

def text_plate(ctx, part, text, center, size, mat, *, normal=FWD, up=UP, depth=.0006, **extras):
    curve = bpy.data.curves.new('Texto ' + text, 'FONT')
    curve.body = text; curve.size = size; curve.extrude = depth; curve.align_x = 'CENTER'; curve.align_y = 'CENTER'
    o = bpy.data.objects.new('Texto ' + text, curve)
    _link(o)
    n = W(normal).normalized(); u = W(up).normalized()
    u = (u - n * u.dot(n)).normalized()
    m = Matrix((u.cross(n), u, n)).transposed().to_4x4()
    o.matrix_world = Matrix.Translation(W(center)) @ m
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.object
    set_material(o, mat)
    return ctx.register(o, part, **extras)

def centroid(objs):
    deps = bpy.context.evaluated_depsgraph_get()
    acc = Vector(); n = 0
    for o in objs:
        if o.type != 'MESH':
            continue
        ev = o.evaluated_get(deps)
        for c in ev.bound_box:
            acc += ev.matrix_world @ Vector(c); n += 1
    return acc / max(n, 1)

def auto_explode(ctx, sid, scale=1.0, min_len=.06):
    """Preenche o extra `explode` das peças sem valor: direção do centroide do sistema para a peça."""
    parts = [p for p in ctx.parts if p.get('system') == sid]
    c = centroid(parts)
    for p in parts:
        if p.get('explode') is not None:
            continue
        pc = centroid([p])
        d = pc - c
        if d.length < 1e-4:
            d = Vector((0, 0, .1))
        d = d.normalized() * max(min_len, d.length * .35 * scale)
        p['explode'] = [round(v, 4) for v in to_web(d)]

# ----------------------------------------------------------------------------- peças copiadas do carro v2
_CAR_GLB = Path(__file__).resolve().parents[2] / 'web' / 'assets' / 'carro-aula-v2.glb'
_car_components = {}

def car_components(source='main_body__01'):
    """Importa o carro v2 uma única vez e devolve os componentes soltos (ilhas de malha) do objeto `source`
    como dicts {n, min, max, verts, faces} no referencial do site. Os objetos importados são removidos."""
    if source in _car_components:
        return _car_components[source]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(_CAR_GLB))
    new = [o for o in bpy.data.objects if o not in before]
    src = next(o for o in new if o.type == 'MESH' and o.name.split('.')[0] == source)
    bm = bmesh.new(); bm.from_mesh(src.data); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    mw = src.matrix_world
    seen = set(); comps = []
    for v in bm.verts:
        if v.index in seen:
            continue
        stack = [v]; seen.add(v.index); comp = []
        while stack:
            cur = stack.pop(); comp.append(cur)
            for e in cur.link_edges:
                w = e.other_vert(cur)
                if w.index not in seen:
                    seen.add(w.index); stack.append(w)
        idx = {vv.index: k for k, vv in enumerate(comp)}
        verts = [to_web(mw @ vv.co) for vv in comp]
        faces = []; fseen = set()
        for vv in comp:
            for f in vv.link_faces:
                if f.index in fseen:
                    continue
                fseen.add(f.index); faces.append([idx[x.index] for x in f.verts])
        mn = [min(p[i] for p in verts) for i in range(3)]; mx = [max(p[i] for p in verts) for i in range(3)]
        comps.append({'n': len(comp), 'min': mn, 'max': mx, 'verts': verts, 'faces': faces})
    bm.free()
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    _car_components[source] = comps
    return comps

def car_part(ctx, part, mat, *, source='main_body__01', box=None, select=None, smooth_angle=math.radians(45), uv=8, **extras):
    """Copia ilhas da malha do carro v2 para o sistema corrente, garantindo coincidência exata com a carroceria
    visível. `box=((xmin,ymin,zmin),(xmax,ymax,zmax))` no referencial do site; `select(comp)` refina a escolha."""
    comps = [c for c in car_components(source)
             if (box is None or all(c['min'][i] >= box[0][i] - 1e-4 and c['max'][i] <= box[1][i] + 1e-4 for i in range(3)))
             and (select is None or select(c))]
    if not comps:
        raise RuntimeError(f'car_part {part!r}: nenhum componente do carro dentro da caixa {box}')
    verts = []; faces = []
    for c in comps:
        off = len(verts)
        verts += [W(v) for v in c['verts']]
        faces += [[i + off for i in f] for f in c['faces']]
    o = mesh_object(part, verts, faces)
    shade_smooth(o, smooth_angle)
    box_uv(o, uv)
    set_material(o, mat)
    o['from_car'] = source
    return ctx.register(o, part, **extras)

def plate(ctx, part, outline, center, thickness, mat, *, normal=FWD, up=UP, bev=.0015, uv=8, **extras):
    """Placa extrudada a partir de um contorno 2D [(u,v)] no plano definido por `normal`/`up`, centrada em `center`.
    A face frontal fica no sentido de `normal`."""
    n = Vector(normal).normalized(); u_axis = Vector(up).normalized()
    u_axis = (u_axis - n * u_axis.dot(n)).normalized()
    r_axis = u_axis.cross(n)
    c = Vector(center)
    def P(u, v, w):
        p = c + r_axis * u + u_axis * v + n * w
        return (p.x, p.y, p.z)
    back = [P(u, v, -thickness / 2) for u, v in outline]
    front = [P(u, v, thickness / 2) for u, v in outline]
    o = loft(ctx, part, [back, front], mat, cap=True, **extras)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    bevel(o, bev, 2)
    return o

# ----------------------------------------------------------------------------- lados
def lado(side, fem=False):
    """Nome do lado no referencial do carro: o piloto olha para +Z, logo +X é a sua esquerda."""
    if fem:
        return 'esquerda' if side > 0 else 'direita'
    return 'esquerdo' if side > 0 else 'direito'

def arc2d(cx, cy, r, a0, a1, n=6):
    """Arco 2D em graus, para contornos de placas."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def face_uv_fit(obj, normal=FWD, tol=.9):
    """Faz as faces cuja normal aponta para `normal` (site frame) cobrirem a textura inteira (UV 0..1),
    usado em displays e placas com imagem única."""
    me = obj.data
    if not me.uv_layers:
        me.uv_layers.new(name='UVMap')
    uv = me.uv_layers.active.data
    n = W(normal).normalized()
    up = Vector((0, 0, 1)) if abs(n.z) < .9 else Vector((0, 1, 0))
    u_axis = up.cross(n).normalized(); v_axis = n.cross(u_axis).normalized()
    for poly in me.polygons:
        if poly.normal.dot(n) < tol:
            continue
        cos = [me.vertices[me.loops[li].vertex_index].co for li in poly.loop_indices]
        us = [c.dot(u_axis) for c in cos]; vs = [c.dot(v_axis) for c in cos]
        du = (max(us) - min(us)) or 1; dv = (max(vs) - min(vs)) or 1
        for li, u_, v_ in zip(poly.loop_indices, us, vs):
            uv[li].uv = ((u_ - min(us)) / du, (v_ - min(vs)) / dv)
    return obj
