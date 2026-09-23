"""Converte a oclusão do piso (assar_sombra.py) em PNG de 8 bits e, se pedido,
anexa a sombra ao arquivo de oclusão por vértice (seção SHD1).

python gravar_sombra.py <sombra.png> [<malha.ao.bin>]

Seção SHD1: 'SHD1', uint32 tamanho do JSON, JSON (limites no referencial do GLB),
uint32 tamanho do PNG, PNG.
"""
import io
import json
import struct
import sys
import numpy as np
from PIL import Image, ImageFilter

dst = sys.argv[1]
base = dst.rsplit('.', 1)[0]
gray = np.load(base + '.npy')
# Um desfoque de 1,2 px tira o granulado das amostras sem apagar o contato dos pneus.
image = Image.fromarray(np.round(gray * 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.2))
image.save(dst, optimize=True)
print(dst, gray.shape, round(float(gray.mean()), 3))

if len(sys.argv) > 2:
    target = sys.argv[2]
    blob = open(target, 'rb').read()
    assert blob[:4] == b'AOV1', 'arquivo de oclusão inválido'
    count = struct.unpack_from('<I', blob, 4)[0]
    total = sum(struct.unpack_from(f'<{count}I', blob, 8))
    blob = blob[:8 + 4 * count + total]  # substitui uma seção SHD1 anterior
    meta = json.load(open(base + '.json'))
    keep = {k: meta[k] for k in ('minX', 'maxX', 'minZ', 'maxZ', 'y')}
    js = json.dumps(keep).encode()
    buf = io.BytesIO(); image.save(buf, 'PNG', optimize=True); png = buf.getvalue()
    open(target, 'wb').write(blob + b'SHD1' + struct.pack('<I', len(js)) + js + struct.pack('<I', len(png)) + png)
    print(target, 'com sombra de', len(png), 'bytes')
