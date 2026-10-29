import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

for f in os.listdir('public/images'):
    if 'P7270094' in f:
        print(f"Found: {repr(f)}")
        # Let's also create an ascii-safe copy if not already there
        ascii_name = 'P7270094_antigrafo.jpg'
        src = os.path.join('public/images', f)
        dst = os.path.join('public/images', ascii_name)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Created alias: {dst}")

