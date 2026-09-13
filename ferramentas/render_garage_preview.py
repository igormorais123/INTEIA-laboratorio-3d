import bpy,sys
from pathlib import Path
repo=Path(sys.argv[sys.argv.index('--')+1])
bpy.ops.wm.open_mainfile(filepath=str(repo/'ambientes/INTEIA_Box_com_carro.blend'))
s=bpy.context.scene;s.render.threads_mode='FIXED';s.render.threads=6;s.cycles.samples=64;s.cycles.use_denoising=True;s.render.resolution_x=1600;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.filepath=str(repo/'ambientes/Previa-Box.png')
bpy.ops.render.render(write_still=True)
print('BOX_RENDER_COMPLETE')
