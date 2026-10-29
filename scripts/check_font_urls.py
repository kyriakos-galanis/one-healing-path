import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('public/templates/saffron/styles/yassas/css/theme.css', 'r', encoding='utf-8') as f:
    text = f.read()

urls = re.findall(r'url\(([^)]+)\)', text)
clean_urls = set()
for u in urls:
    u = u.strip('\'" ')
    if 'data:' not in u:
        clean_urls.add(u)

print("URLs in theme.css:")
for u in sorted(clean_urls):
    # CSS is at public/templates/saffron/styles/yassas/css/theme.css
    # Relative paths like ../fonts/... resolve from public/templates/saffron/styles/yassas/css/
    css_dir = os.path.join('public', 'templates', 'saffron', 'styles', 'yassas', 'css')
    resolved = os.path.normpath(os.path.join(css_dir, u.split('?')[0].split('#')[0]))
    exists = os.path.exists(resolved)
    print(f"  {u} -> {resolved}: {'EXISTS' if exists else 'MISSING'}")
