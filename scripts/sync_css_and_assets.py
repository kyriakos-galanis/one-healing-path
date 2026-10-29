import os
import sys
import re
import urllib.request
import urllib.parse
import ssl

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# First, copy css_live into public/ so the exact original paths work
import shutil
live_css_src = os.path.join('scraped_data', 'css_live')
for root, dirs, files in os.walk(live_css_src):
    for f in files:
        src_file = os.path.join(root, f)
        rel = os.path.relpath(src_file, live_css_src)
        dst_file = os.path.join('public', rel)
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)
        print(f"Copied CSS to {dst_file}")

# Now scan every .css file in public/ for url(...) references
missing_assets = set()
for root, dirs, files in os.walk('public'):
    for f in files:
        if f.endswith('.css'):
            css_path = os.path.join(root, f)
            with open(css_path, 'r', encoding='utf-8', errors='ignore') as cf:
                css_text = cf.read()
            
            # Find all urls
            for match in re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', css_text):
                clean_ref = match.split('?')[0].split('#')[0]
                if clean_ref.startswith('data:') or not clean_ref:
                    continue
                
                # Resolve relative path
                if clean_ref.startswith('/'):
                    target_local = os.path.join('public', clean_ref.lstrip('/'))
                    target_remote = 'https://www.onehealing.gr' + clean_ref
                else:
                    css_dir = os.path.dirname(css_path)
                    target_local = os.path.normpath(os.path.join(css_dir, clean_ref))
                    # remote url
                    rel_to_public = os.path.relpath(target_local, 'public').replace('\\', '/')
                    target_remote = 'https://www.onehealing.gr/' + rel_to_public
                
                if not os.path.exists(target_local):
                    print(f"Missing referenced asset: {clean_ref}")
                    print(f"  Local path: {target_local}")
                    print(f"  Remote url: {target_remote}")
                    missing_assets.add((target_local, target_remote))

print(f"\nAttempting to download {len(missing_assets)} missing assets...")
for target_local, target_remote in missing_assets:
    os.makedirs(os.path.dirname(target_local), exist_ok=True)
    try:
        parsed = urllib.parse.urlsplit(target_remote)
        enc_path = urllib.parse.quote(parsed.path)
        clean_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, enc_path, parsed.query, parsed.fragment))
        req = urllib.request.Request(clean_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            data = r.read()
            with open(target_local, 'wb') as f:
                f.write(data)
            print(f"  [SUCCESS] {target_remote} -> {target_local} ({len(data)} bytes)")
    except Exception as e:
        print(f"  [FAILED] {target_remote}: {e}")

print("CSS and asset scan complete.")
