import sys
import os
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

base_url = 'https://www.onehealing.gr'

for link in soup.find_all('link'):
    href = link.get('href')
    if href and href.startswith('/') and (href.endswith('.css') or '.css?' in href or href.endswith('.ico') or href.endswith('.png')):
        clean_path = href.split('?')[0].lstrip('/')
        local_path = os.path.join('public', clean_path)
        if not os.path.exists(local_path):
            url = base_url + '/' + clean_path
            print(f'Downloading link: {url} -> {local_path}')
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            try:
                res = requests.get(url, headers=headers, timeout=10)
                if res.status_code == 200:
                    with open(local_path, 'wb') as out:
                        out.write(res.content)
                    print(' OK')
                else:
                    print(f' Failed ({res.status_code})')
            except Exception as e:
                print(f' Error: {e}')
        else:
            print(f'Already exists: {local_path}')

for s in soup.find_all('script'):
    src = s.get('src')
    if src and src.startswith('/') and (src.endswith('.js') or '.js?' in src):
        clean_path = src.split('?')[0].lstrip('/')
        local_path = os.path.join('public', clean_path)
        if not os.path.exists(local_path):
            url = base_url + '/' + clean_path
            print(f'Downloading script: {url} -> {local_path}')
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            try:
                res = requests.get(url, headers=headers, timeout=10)
                if res.status_code == 200:
                    with open(local_path, 'wb') as out:
                        out.write(res.content)
                    print(' OK')
                else:
                    print(f' Failed ({res.status_code})')
            except Exception as e:
                print(f' Error: {e}')
        else:
            print(f'Already exists: {local_path}')
