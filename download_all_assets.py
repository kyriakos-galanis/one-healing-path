import os
import sys
import re
import json
import time
import urllib.parse
import requests

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = os.path.abspath("scraped_data")
JSON_DIR = os.path.join(DATA_DIR, "json")
ASSETS_DIR = os.path.join(DATA_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
CSS_DIR = os.path.join(ASSETS_DIR, "css")

for d in [ASSETS_DIR, IMAGES_DIR, CSS_DIR]:
    os.makedirs(d, exist_ok=True)

# Collect all images and CSS
all_images = set()
all_css = set()

for fname in os.listdir(JSON_DIR):
    if fname.endswith(".json"):
        with open(os.path.join(JSON_DIR, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
            for img in data.get("images", []):
                all_images.add(img)
            for css in data.get("css_files", []):
                all_css.add(css)

# Also check raw HTML files for any background images or favicon
RAW_HTML_DIR = os.path.join(DATA_DIR, "raw_html")
for fname in os.listdir(RAW_HTML_DIR):
    if fname.endswith(".html"):
        with open(os.path.join(RAW_HTML_DIR, fname), "r", encoding="utf-8") as f:
            content = f.read()
            # find background-image urls
            for match in re.finditer(r'url\([\'"]?([^\'")]+)[\'"]?\)', content):
                bg_url = match.group(1)
                if any(bg_url.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"]):
                    if "web.archive.org" in bg_url:
                        clean_bg = re.search(r'https?://web\.archive\.org/web/\d+[a-z_]*/(.*)', bg_url)
                        if clean_bg:
                            bg_url = clean_bg.group(1)
                    if bg_url.startswith("/"):
                        bg_url = "http://www.onehealingpath.gr" + bg_url
                    if "onehealingpath.gr" in bg_url:
                        all_images.add(bg_url)

print(f"Total images to download: {len(all_images)}")
print(f"Total stylesheets to download: {len(all_css)}")

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

asset_manifest = {}
manifest_file = os.path.join(DATA_DIR, "assets_manifest.json")
if os.path.exists(manifest_file):
    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            asset_manifest = json.load(f)
    except Exception:
        pass

def download_one_asset(url: str, is_css: bool = False):
    parsed = urllib.parse.urlparse(url)
    clean_path = parsed.path
    if not clean_path or clean_path == "/":
        return ""
        
    filename = urllib.parse.unquote(os.path.basename(clean_path))
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    if not filename:
        return ""
        
    subfolder = urllib.parse.unquote(os.path.dirname(clean_path)).strip("/\\")
    subfolder = re.sub(r'[\\*?:"<>|]', '_', subfolder).replace("/", os.sep)
    
    target_base = CSS_DIR if is_css else IMAGES_DIR
    target_dir = os.path.join(target_base, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, filename)
    
    rel_path = os.path.relpath(target_path, DATA_DIR)
    
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return rel_path
        
    # Wayback prefixes: try im_ or cs_ first, or redirect
    prefix = "cs_" if is_css else "im_"
    wb_url = f"https://web.archive.org/web/20250521181650{prefix}/{url}"
    
    for attempt in range(3):
        try:
            time.sleep(0.5)
            r = session.get(wb_url, headers=headers, timeout=20, allow_redirects=True)
            if r.status_code == 200 and r.content:
                # verify it's not a wayback html error page
                if is_css or not (b"<!DOCTYPE html" in r.content[:100] or b"<html" in r.content[:100]):
                    with open(target_path, "wb") as f:
                        f.write(r.content)
                    print(f"  [OK] Saved {filename} ({len(r.content):,} bytes)", flush=True)
                    return rel_path
            elif r.status_code == 429:
                print(f"  [429] Pausing 10s for {filename}...", flush=True)
                time.sleep(10)
            elif r.status_code == 404:
                # Try finding in general archive
                wb_url_general = f"https://web.archive.org/web/{prefix}/{url}"
                time.sleep(0.5)
                r_gen = session.get(wb_url_general, headers=headers, timeout=20, allow_redirects=True)
                if r_gen.status_code == 200 and r_gen.content:
                    if is_css or not (b"<!DOCTYPE html" in r_gen.content[:100] or b"<html" in r_gen.content[:100]):
                        with open(target_path, "wb") as f:
                            f.write(r_gen.content)
                        print(f"  [OK Fallback] Saved {filename} ({len(r_gen.content):,} bytes)", flush=True)
                        return rel_path
                print(f"  [404] Not found: {url}", flush=True)
                return ""
        except Exception as e:
            print(f"  [Error] {e} on {filename}", flush=True)
            time.sleep(2)
            
    return ""

print("\n--- Downloading Images ---", flush=True)
for i, img in enumerate(sorted(all_images), 1):
    print(f"[{i}/{len(all_images)}] {img}", flush=True)
    res = download_one_asset(img, is_css=False)
    if res:
        asset_manifest[img] = res
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(asset_manifest, f, ensure_ascii=False, indent=2)

print("\n--- Downloading CSS ---", flush=True)
for i, css in enumerate(sorted(all_css), 1):
    print(f"[{i}/{len(all_css)}] {css}", flush=True)
    res = download_one_asset(css, is_css=True)
    if res:
        asset_manifest[css] = res
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(asset_manifest, f, ensure_ascii=False, indent=2)

print("\nAll assets downloaded successfully!", flush=True)
