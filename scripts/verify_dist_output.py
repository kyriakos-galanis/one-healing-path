import os
import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFYING DIST OUTPUT ===")

dist_html = 'dist/el/index.html'
if not os.path.exists(dist_html):
    print("dist/el/index.html does not exist!")
    sys.exit(1)

with open(dist_html, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("1. Title:", soup.title.string if soup.title else None)

print("\n2. Stylesheets in <head>:")
for link in soup.find_all('link', rel=lambda r: r and 'stylesheet' in r):
    href = link.get('href')
    # strip base prefix '/one-healing-path'
    local_path = href.replace('/one-healing-path/', 'dist/').lstrip('/')
    exists = os.path.exists(local_path)
    print(f"   {href} -> {local_path}: {'OK' if exists else 'MISSING'}")

print("\n3. Body id and classes:")
body = soup.find('body')
print("   Body:", body.attrs if body else None)

print("\n4. Layout elements:")
for cls in ['tm-sheet', 'tm-toolbar', 'tm-headerbar', 'tm-navbar', 'tm-sliderbar', 'tm-middle', 'tm-sidebar-b', 'tm-footer', 'uk-offcanvas']:
    el = soup.find(class_=cls) or soup.find(id=cls)
    print(f"   .{cls}: {'FOUND' if el else 'NOT FOUND'}")

print("\n5. Checking all <img> tags in dist/el/index.html:")
missing_imgs = []
for img in soup.find_all('img'):
    src = img.get('src')
    if src and not src.startswith('data:'):
        clean_src = src.replace('/one-healing-path/', 'dist/').lstrip('/')
        exists = os.path.exists(clean_src)
        if not exists:
            missing_imgs.append((src, clean_src))
        print(f"   <img> {src} -> {'OK' if exists else 'MISSING'}")

if missing_imgs:
    print(f"WARNING: {len(missing_imgs)} missing images!")
else:
    print("ALL images in homepage exist in dist!")
