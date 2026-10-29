import os
import sys
import re
import urllib.request
import urllib.parse
import ssl
import json

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_url(url):
    # Quote non-ascii in URL path
    parsed = urllib.parse.urlsplit(url)
    encoded_path = urllib.parse.quote(parsed.path)
    clean_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, encoded_path, parsed.query, parsed.fragment))
    req = urllib.request.Request(clean_url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return resp.read(), resp.status
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None, None

# 1. Download all images from live_inventory.json
with open('scraped_data/live_inventory.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

# Also check known common images like favicon, slide2.jpg, etc.
extra_urls = [
    'https://www.onehealing.gr/favicon.ico',
    'https://www.onehealing.gr/images/slide2.jpg',
    'https://www.onehealing.gr/images/slide1.jpg',
    'https://www.onehealing.gr/images/logo/OneHealingPath___Logo-2_copy.png',
    'https://www.onehealing.gr/images/logo/OneHealingPath___Logo-1.png',
]
all_images = set(inventory['images'] + extra_urls)

print(f"Downloading {len(all_images)} potential image URLs...")
for img_url in sorted(all_images):
    parsed = urllib.parse.urlsplit(img_url)
    # relative local path in public/
    rel_path = parsed.path.lstrip('/')
    if not rel_path:
        continue
    # unquote for filename
    decoded_rel_path = urllib.parse.unquote(rel_path)
    local_path = os.path.join('public', decoded_rel_path.replace('/', os.sep))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    data, status = fetch_url(img_url)
    if data and status == 200:
        with open(local_path, 'wb') as f:
            f.write(data)
        print(f"  [OK] Saved {len(data)} bytes -> {local_path}")
    else:
        print(f"  [MISSING/FAIL] {img_url}")

# 2. Download and analyze CSS files
css_dir = os.path.join('scraped_data', 'css_live')
os.makedirs(css_dir, exist_ok=True)

css_urls = inventory.get('stylesheets', [])
for css_url in sorted(css_urls):
    parsed = urllib.parse.urlsplit(css_url)
    rel_path = parsed.path.lstrip('/')
    decoded_rel_path = urllib.parse.unquote(rel_path)
    local_path = os.path.join(css_dir, decoded_rel_path.replace('/', os.sep))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    data, status = fetch_url(css_url)
    if data and status == 200:
        with open(local_path, 'wb') as f:
            f.write(data)
        print(f"  [OK CSS] Saved {len(data)} bytes -> {local_path}")
        
        # Check for font files or images inside CSS
        text = data.decode('utf-8', errors='ignore')
        for match in re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', text):
            match_clean = match.split('?')[0].split('#')[0]
            if match_clean.startswith('data:'):
                continue
            asset_full = urllib.parse.urljoin(css_url, match)
            print(f"    CSS asset found: {match} -> {asset_full}")
            
            # Download asset to public/
            asset_parsed = urllib.parse.urlsplit(asset_full)
            if asset_parsed.netloc in ('www.onehealing.gr', 'onehealing.gr'):
                asset_rel = urllib.parse.unquote(asset_parsed.path.lstrip('/'))
                asset_local = os.path.join('public', asset_rel.replace('/', os.sep))
                os.makedirs(os.path.dirname(asset_local), exist_ok=True)
                adata, astatus = fetch_url(asset_full)
                if adata and astatus == 200:
                    with open(asset_local, 'wb') as af:
                        af.write(adata)
                    print(f"      [OK ASSET] -> {asset_local}")

print("Asset sync complete!")
