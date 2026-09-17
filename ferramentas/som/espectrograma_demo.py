"""Espectrograma de um WAV de demonstração (mesma STFT da análise), gravado ao lado do arquivo como .png.

Uso: ferramentas/som/.venv/Scripts/python.exe ferramentas/som/espectrograma_demo.py ferramentas/som/.demos/<arquivo>.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, soundfile as sf, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from analisar_referencias import stft_db, HOP, SR
for path in sys.argv[1:]:
    x,sr=sf.read(path); spec,freqs=stft_db(x.astype(np.float32)); t=np.arange(len(spec))*HOP/SR
    fig,ax=plt.subplots(figsize=(16,6)); keep=freqs<=8000
    ax.imshow(spec[:,keep].T,origin='lower',aspect='auto',cmap='magma',extent=[0,t[-1],0,8000],vmin=np.percentile(spec,40),vmax=spec.max())
    ax.set_title(path.split('/')[-1]); ax.set_xlabel('s'); ax.set_ylabel('Hz'); fig.tight_layout(); out=path.replace('.wav','.png'); fig.savefig(out,dpi=80); print(out)
