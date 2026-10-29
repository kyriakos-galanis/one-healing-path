import os
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING ALL IMAGES IN ALL DIST HTML FILES ===")

dist_dir = 'dist'
html_files = []
for root, dirs, files in os.walk(dist_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

total_imgs = 0
missing = []

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and not src.startswith('data:'):
            total_imgs += 1
            clean_src = src.replace('/one-healing-path/', 'dist/').lstrip('/')
            # Also handle if query param exists
            clean_src = clean_src.split('?')[0]
            if not os.path.exists(clean_src):
                missing.append((hf, src, clean_src))

print(f"Scanned {len(html_files)} HTML files, found {total_imgs} image tags.")
if missing:
    print(f"FAILED: {len(missing)} missing images:")
    for hf, src, clean in missing[:20]:
        print(f"  In {hf}: {src} -> {clean}")
else:
    print("SUCCESS: 100% of images referenced across ALL built HTML pages exist in dist!")
