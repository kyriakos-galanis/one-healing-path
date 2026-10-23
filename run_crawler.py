import os
import sys
import json
import time
import requests
from crawler_lib import (
    BASE_TARGET, WAYBACK_PREFIX, DATA_DIR, RAW_HTML_DIR, CLEAN_HTML_DIR,
    MARKDOWN_DIR, JSON_DIR, clean_wayback_url, normalize_internal_url,
    url_to_slug, fetch_with_retry, download_asset, extract_page_data
)

sys.stdout.reconfigure(encoding='utf-8')

SEED_URLS = [
    "http://www.onehealingpath.gr/el/",
    "http://www.onehealingpath.gr/el/viografiko",
    "http://www.onehealingpath.gr/el/therapeftiki-proseggisi",
    "http://www.onehealingpath.gr/el/therapeftiki-proseggisi/velonismos",
    "http://www.onehealingpath.gr/el/therapeftiki-proseggisi/onehealing",
    "http://www.onehealingpath.gr/el/therapeftiki-proseggisi/psychiatriki",
    "http://www.onehealingpath.gr/el/prosopikes-martyries",
    "http://www.onehealingpath.gr/el/syxnes-erotiseis",
    "http://www.onehealingpath.gr/el/istologio",
    "http://www.onehealingpath.gr/el/epikoinonia",
    "http://www.onehealingpath.gr/index.php?option=com_contact&view=contact&id=1&Itemid=584&lang=el",
    "http://www.onehealingpath.gr/el/item/13-prosopika",
    "http://www.onehealingpath.gr/el/item/14-tai-chi",
    "http://www.onehealingpath.gr/el/item/15-psyxiko-trayma",
    "http://www.onehealingpath.gr/el/item/16-alexithymia",
    "http://www.onehealingpath.gr/el/item/7-velonismos-i-farmaka-mia-erotisi-pagida",
    "http://www.onehealingpath.gr/el/item/9-interstitium",
    "http://www.onehealingpath.gr/el/itemlist/category/10-psyxiki-ygeia",
    "http://www.onehealingpath.gr/el/itemlist/category/7-ska",
    "http://www.onehealingpath.gr/el/itemlist/category/8-pki",
    "http://www.onehealingpath.gr/el/itemlist/tag/Βελονισμός",
    "http://www.onehealingpath.gr/el/itemlist/tag/Τάι τσι",
    "http://www.onehealingpath.gr/el/itemlist/user/655-panagiwthsgkinhsmdcac",
]

# Additional item probes to ensure nothing is missed
for item_id in range(1, 20):
    SEED_URLS.append(f"http://www.onehealingpath.gr/el/item/{item_id}")

queue = list(dict.fromkeys(SEED_URLS))
visited = set()
all_manifest = {}
all_assets = set()
all_css = set()

# Load existing manifest if any
manifest_path = os.path.join(DATA_DIR, "manifest.json")
if os.path.exists(manifest_path):
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            all_manifest = json.load(f)
            visited = set(all_manifest.keys())
            print(f"Loaded existing manifest with {len(visited)} pages.")
    except Exception:
        pass

session = requests.Session()

print(f"Starting crawl with {len(queue)} URLs in queue...")

while queue:
    current_url = queue.pop(0)
    canonical = normalize_internal_url(current_url)
    if not canonical:
        continue
    if canonical in visited:
        continue
        
    slug = url_to_slug(canonical)
    raw_html_file = os.path.join(RAW_HTML_DIR, f"{slug}.html")
    
    print(f"\n[Crawling {len(visited)+1}] {canonical}")
    
    # Check if raw HTML already saved on disk
    if os.path.exists(raw_html_file) and os.path.getsize(raw_html_file) > 0:
        print(f"  -> Reading cached HTML from {slug}.html")
        with open(raw_html_file, "r", encoding="utf-8") as f:
            html = f.read()
        status_code = 200
        final_url = canonical
    else:
        fetch_url = f"{WAYBACK_PREFIX}{canonical}"
        resp = fetch_with_retry(fetch_url, session, delay=0.8)
        if not resp:
            print(f"  -> Failed to fetch {canonical}")
            visited.add(canonical)
            continue
        status_code = resp.status_code
        final_url = clean_wayback_url(resp.url)
        if status_code != 200:
            print(f"  -> Status {status_code}, skipping.")
            visited.add(canonical)
            all_manifest[canonical] = {"status": status_code, "url": canonical}
            continue
        html = resp.text
        # Save raw HTML
        with open(raw_html_file, "w", encoding="utf-8") as f:
            f.write(html)
            
    visited.add(canonical)
    
    # Parse page data
    page_data = extract_page_data(html, canonical)
    page_data["canonical_url"] = canonical
    page_data["final_url"] = final_url
    page_data["slug"] = slug
    page_data["status"] = status_code
    
    # Save Clean HTML
    clean_html_file = os.path.join(CLEAN_HTML_DIR, f"{slug}.html")
    with open(clean_html_file, "w", encoding="utf-8") as f:
        f.write(page_data["clean_html"])
        
    # Save Markdown
    md_file = os.path.join(MARKDOWN_DIR, f"{slug}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# {page_data['title']}\n\nURL: {canonical}\n\n" + page_data["markdown"])
        
    # Save JSON data
    json_file = os.path.join(JSON_DIR, f"{slug}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(page_data, f, ensure_ascii=False, indent=2)
        
    print(f"  -> Title: '{page_data['title']}' | Headings: {len(page_data['headings'])} | Imgs: {len(page_data['images'])}")
    
    # Collect assets
    for img in page_data["images"]:
        all_assets.add(img)
    for c in page_data["css_files"]:
        all_css.add(c)
        
    # Enqueue new internal links
    new_links_count = 0
    for link in page_data["internal_links"]:
        if link not in visited and link not in queue:
            queue.append(link)
            new_links_count += 1
            
    if new_links_count > 0:
        print(f"  -> Discovered {new_links_count} new links to queue (queue size: {len(queue)})")
        
    all_manifest[canonical] = {
        "status": status_code,
        "title": page_data["title"],
        "slug": slug,
        "meta_description": page_data["meta_description"],
        "headings": page_data["headings"],
        "images_count": len(page_data["images"]),
        "markdown_file": f"markdown/{slug}.md",
        "clean_html_file": f"clean_html/{slug}.html",
        "raw_html_file": f"raw_html/{slug}.html"
    }
    
    # Periodically save manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(all_manifest, f, ensure_ascii=False, indent=2)

print("\n==========================================")
print(f"Page crawling finished! Total pages processed: {len(visited)}")
print(f"Unique images discovered: {len(all_assets)}")
print(f"Unique CSS files discovered: {len(all_css)}")
print("==========================================\n")

print("Downloading images...")
asset_manifest = {}
for i, img_url in enumerate(sorted(all_assets), 1):
    print(f"[{i}/{len(all_assets)}] Downloading image: {img_url}")
    local_path = download_asset(img_url, session, asset_type="image")
    asset_manifest[img_url] = local_path

print("\nDownloading stylesheets...")
for i, css_url in enumerate(sorted(all_css), 1):
    print(f"[{i}/{len(all_css)}] Downloading CSS: {css_url}")
    local_path = download_asset(css_url, session, asset_type="css")
    asset_manifest[css_url] = local_path

with open(os.path.join(DATA_DIR, "assets_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(asset_manifest, f, ensure_ascii=False, indent=2)

print("\nScraping and asset download complete!")
