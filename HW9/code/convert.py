from PIL import Image
import glob
import os

from pathlib import Path

current_dir = Path('.').resolve()

out_dir = current_dir / "converted"
os.mkdir(out_dir)
cnt = 0

for img in glob.glob(str(current_dir / "*.bmp")):
    filename = Path(img).stem
    Image.open(img).save(str(out_dir / f'{filename}.png'))
