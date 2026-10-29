import urllib.request
import ssl
import sys
import os
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_domain = 'www.onehealing.gr'
start_url = 'https://www.onehealing.gr/el/'

visited_urls = set()
to_visit = [start_url]
images = set()
stylesheets = set()
scripts = set()
pages_found = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print("Starting crawl of live site...")

while to_visit and len(visited_urls) < 100:
    url = to_visit.pop(0)
    clean_url = url.split('#')[0]
    if clean_url in visited_urls:
        continue
    visited_urls.add(clean_url)
    
    try:
        req = urllib.request.Request(clean_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content_type = resp.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                continue
            html = resp.read().decode('utf-8', errors='ignore')
            pages_found.append(clean_url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # images
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and not src.startswith('data:'):
                    images.add(urljoin(clean_url, src))
            
            # css
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    stylesheets.add(urljoin(clean_url, href))
            
            # inline style background images
            for elem in soup.find_all(style=True):
                style = elem.get('style', '')
                for bg in re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', style):
                    if not bg.startswith('data:'):
                        images.add(urljoin(clean_url, bg))

            # links
            for a in soup.find_all('a', href=True):
                href = urljoin(clean_url, a['href'])
                p = urlparse(href)
                if p.netloc in (base_domain, 'onehealing.gr'):
                    if p.path.startswith('/el') or p.path == '/':
                        target = href.split('#')[0]
                        if target not in visited_urls and target not in to_visit:
                            to_visit.append(target)
    except Exception as e:
        print(f'Error visiting {clean_url}: {e}')

print(f'\nTotal pages found: {len(pages_found)}')
for p in sorted(pages_found):
    print(f'  PAGE: {p}')

print(f'\nTotal stylesheets found: {len(stylesheets)}')
for s in sorted(stylesheets):
    print(f'  CSS: {s}')

print(f'\nTotal images found: {len(images)}')
for img in sorted(images):
    print(f'  IMG: {img}')

# Save to scraped_data/live_inventory.json
import json
os.makedirs('scraped_data', exist_ok=True)
with open('scraped_data/live_inventory.json', 'w', encoding='utf-8') as f:
    json.dump({
        'pages': sorted(pages_found),
        'stylesheets': sorted(stylesheets),
        'images': sorted(images)
    }, f, indent=2, ensure_ascii=False)
print("\nSaved inventory to scraped_data/live_inventory.json")
