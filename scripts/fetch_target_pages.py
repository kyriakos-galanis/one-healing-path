import os
import sys
import json
import urllib.request
import urllib.parse
import ssl
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

target_pages = [
    ('/', '/el/'),
    ('/el/', '/el/'),
    ('/el/viografiko', '/el/viografiko'),
    ('/el/therapeftiki-proseggisi', '/el/therapeftiki-proseggisi'),
    ('/el/therapeftiki-proseggisi/velonismos', '/el/therapeftiki-proseggisi/velonismos'),
    ('/el/therapeftiki-proseggisi/onehealing', '/el/therapeftiki-proseggisi/onehealing'),
    ('/el/therapeftiki-proseggisi/psychiatriki', '/el/therapeftiki-proseggisi/psychiatriki'),
    ('/el/prosopikes-martyries', '/el/prosopikes-martyries'),
    ('/el/syxnes-erotiseis', '/el/syxnes-erotiseis'),
    ('/el/istologio', '/el/istologio'),
    ('/el/epikoinonia', '/el/epikoinonia'),
    ('/el/item/13-prosopika', '/el/item/13-prosopika'),
    ('/el/item/14-tai-chi', '/el/item/14-tai-chi'),
    ('/el/item/7-velonismos-i-farmaka-mia-erotisi-pagida', '/el/item/7-velonismos-i-farmaka-mia-erotisi-pagida'),
    ('/el/item/9-interstitium', '/el/item/9-interstitium'),
    ('/el/item/16-alexithymia', '/el/item/16-alexithymia'),
    ('/el/item/15-psyxiko-trayma', '/el/item/15-psyxiko-trayma'),
    ('/el/itemlist/category/7-ska', '/el/itemlist/category/7-ska'),
    ('/el/itemlist/category/8-pki', '/el/itemlist/category/8-pki'),
    ('/el/itemlist/category/10-psyxiki-ygeia', '/el/itemlist/category/10-psyxiki-ygeia'),
    ('/el/itemlist/user/655-panagiwthsgkinhsmdcac', '/el/itemlist/user/655-panagiwthsgkinhsmdcac'),
]

os.makedirs('scraped_data/live_pages_raw', exist_ok=True)
os.makedirs('scraped_data/live_pages_clean', exist_ok=True)

page_summaries = {}

for name, path in target_pages:
    url = 'https://www.onehealing.gr' + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            safe_name = path.strip('/').replace('/', '__')
            if not safe_name:
                safe_name = 'home'
            
            with open(f'scraped_data/live_pages_raw/{safe_name}.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else ''
            
            # Extract main content
            # In YOOtheme Saffron, main content is usually inside #tm-main or .tm-content or #system-message-container + div
            main = soup.find('main', id='tm-content') or soup.find('div', id='tm-content') or soup.find('div', class_='tm-main') or soup.find('div', class_='tm-content')
            
            # Sidebar
            sidebar = soup.find('aside', class_='tm-sidebar-b') or soup.find('aside', class_=lambda c: c and 'sidebar' in c)
            
            # Breadcrumbs
            breadcrumbs = []
            bc_ul = soup.find('ul', class_='uk-breadcrumb')
            if bc_ul:
                for li in bc_ul.find_all('li'):
                    breadcrumbs.append({
                        'text': li.get_text(strip=True),
                        'href': li.find('a')['href'] if li.find('a') else None
                    })
            
            page_summaries[path] = {
                'title': title,
                'breadcrumbs': breadcrumbs,
                'has_main': main is not None,
                'has_sidebar': sidebar is not None,
            }
            
            if main:
                with open(f'scraped_data/live_pages_clean/{safe_name}.html', 'w', encoding='utf-8') as f:
                    f.write(main.prettify())
            
            print(f"[OK {r.status}] {path} -> title: {title}")
    except Exception as e:
        print(f"[ERROR] {path}: {e}")

with open('scraped_data/live_page_summaries.json', 'w', encoding='utf-8') as f:
    json.dump(page_summaries, f, indent=2, ensure_ascii=False)

print("\nDone scraping live target pages!")
