import sys
import os
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

pages = [
    'el__viografiko.html',
    'el__therapeftiki-proseggisi.html',
    'el__therapeftiki-proseggisi__velonismos.html',
    'el__therapeftiki-proseggisi__onehealing.html',
    'el__therapeftiki-proseggisi__psychiatriki.html',
    'el__syxnes-erotiseis.html',
    'el__prosopikes-martyries.html',
    'el__epikoinonia.html'
]

for p in pages:
    path = os.path.join('scraped_data', 'live_pages_raw', p)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        content = soup.find('main', class_='tm-content')
        title = soup.find('title')
        print(f"=== {p} ===")
        print("Title:", title.text if title else None)
        if content:
            # First 300 chars of content
            print("Content tag:", content.name, "Length:", len(str(content)))
            print(str(content)[:250].replace('\n', ' '))
        print()
