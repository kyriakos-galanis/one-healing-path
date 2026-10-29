import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el__epikoinonia.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('main', class_='tm-content')
if content:
    # Remove system-message-container empty div
    for sm in content.find_all(id='system-message-container'):
        sm.decompose()
    
    # Replace email cloak span with direct mailto
    for sp in content.find_all('span', class_='contact-emailto'):
        sp.clear()
        sp.append(BeautifulSoup('<a href="mailto:gkinispan@gmail.com">gkinispan@gmail.com</a>', 'html.parser'))
    
    # Replace any absolute live URLs
    html_str = str(content)
    # Remove <main class="tm-content"> wrapper itself since Layout supplies it
    html_str = re.sub(r'^<main class="tm-content">', '', html_str)
    html_str = re.sub(r'</main>$', '', html_str)
    html_str = html_str.replace('https://www.onehealing.gr/el/', '/el/')
    html_str = html_str.replace('http://www.onehealing.gr', '/el/')

    astro_content = f"""---
import Layout from '../../layouts/Layout.astro';
---

<Layout 
  title="Επικοινωνια - onehealing.gr"
  breadcrumbs={{[
    {{ label: 'Αρχική', href: '/el/' }},
    {{ label: 'Επικοινωνία' }}
  ]}}
>
  <div class="page-content contact-page">
    {html_str}
  </div>
</Layout>
"""

    with open('src/pages/el/epikoinonia.astro', 'w', encoding='utf-8') as out:
        out.write(astro_content)
    print("Updated src/pages/el/epikoinonia.astro successfully.")
