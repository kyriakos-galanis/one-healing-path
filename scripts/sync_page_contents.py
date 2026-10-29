import sys
import os
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

pages_map = [
    {
        'raw_file': 'el__viografiko.html',
        'astro_file': 'src/pages/el/viografiko.astro',
        'title': 'Βιογραφικo - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Βιογραφικό' }]"
    },
    {
        'raw_file': 'el__therapeftiki-proseggisi.html',
        'astro_file': 'src/pages/el/therapeftiki-proseggisi/index.astro',
        'title': 'Θεραπευτικη Προσεγγιση - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Θεραπευτική Προσέγγιση' }]"
    },
    {
        'raw_file': 'el__therapeftiki-proseggisi__velonismos.html',
        'astro_file': 'src/pages/el/therapeftiki-proseggisi/velonismos.astro',
        'title': 'Βελονισμός - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Θεραπευτική Προσέγγιση', href: '/el/therapeftiki-proseggisi' }, { label: 'Βελονισμός' }]"
    },
    {
        'raw_file': 'el__therapeftiki-proseggisi__onehealing.html',
        'astro_file': 'src/pages/el/therapeftiki-proseggisi/onehealing.astro',
        'title': 'Ψυχοθεραπεία - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Θεραπευτική Προσέγγιση', href: '/el/therapeftiki-proseggisi' }, { label: 'Ψυχοθεραπεία' }]"
    },
    {
        'raw_file': 'el__therapeftiki-proseggisi__psychiatriki.html',
        'astro_file': 'src/pages/el/therapeftiki-proseggisi/psychiatriki.astro',
        'title': 'Ψυχιατρική - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Θεραπευτική Προσέγγιση', href: '/el/therapeftiki-proseggisi' }, { label: 'Ψυχιατρική' }]"
    },
    {
        'raw_file': 'el__syxnes-erotiseis.html',
        'astro_file': 'src/pages/el/syxnes-erotiseis.astro',
        'title': 'Συχνες Ερωτησεις - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Συχνές Ερωτήσεις' }]"
    },
    {
        'raw_file': 'el__prosopikes-martyries.html',
        'astro_file': 'src/pages/el/prosopikes-martyries.astro',
        'title': 'Προσωπικες Μαρτυριες - onehealing.gr',
        'breadcrumbs': "[{ label: 'Αρχική', href: '/el/' }, { label: 'Προσωπικές Μαρτυρίες' }]"
    }
]

def clean_html(html_str):
    # Remove system-message-container empty div if any
    html_str = re.sub(r'<div id="system-message-container">\s*</div>', '', html_str)
    # Replace absolute URLs of onehealing.gr with relative
    html_str = re.sub(r'https?://(www\.)?onehealing\.gr/el/', '/el/', html_str)
    html_str = re.sub(r'https?://(www\.)?onehealingpath\.gr/el/', '/el/', html_str)
    return html_str.strip()

for item in pages_map:
    raw_path = os.path.join('scraped_data', 'live_pages_raw', item['raw_file'])
    if not os.path.exists(raw_path):
        print(f"File not found: {raw_path}")
        continue
    
    with open(raw_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    content = soup.find('main', class_='tm-content')
    if not content:
        print(f"No tm-content found in {raw_path}")
        continue
    
    # Extract inner HTML of tm-content
    inner_html = "".join(str(c) for c in content.children if c.name or (isinstance(c, str) and c.strip()))
    inner_html = clean_html(inner_html)
    
    # Calculate relative layout path based on depth from src/
    # E.g. src/pages/el/viografiko.astro -> 3 dirs deep from src: pages, el -> ../../layouts/Layout.astro
    # src/pages/el/therapeftiki-proseggisi/index.astro -> 3 dirs deep: pages, el, therapeftiki-proseggisi -> ../../../layouts/Layout.astro
    dir_depth = os.path.dirname(item['astro_file']).replace('\\', '/').split('/')[1:] # ignore 'src'
    layout_rel = ('../' * len(dir_depth)) + 'layouts/Layout.astro'

    astro_content = f"""---
import Layout from '{layout_rel}';
---

<Layout 
  title="{item['title']}"
  breadcrumbs={{{item['breadcrumbs']}}}
>
  <div class="page-content">
    {inner_html}
  </div>
</Layout>
"""
    # Write to target Astro file
    os.makedirs(os.path.dirname(item['astro_file']), exist_ok=True)
    with open(item['astro_file'], 'w', encoding='utf-8') as out:
        out.write(astro_content)
    print(f"Generated {item['astro_file']} from {item['raw_file']}")
