import sys
import os
import requests

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    '/media/widgetkit/widgets/lightbox/images/blank.gif',
    '/media/widgetkit/widgets/lightbox/images/buttons.png',
    '/media/widgetkit/widgets/lightbox/images/close.png',
    '/media/widgetkit/widgets/lightbox/images/loading.png',
    '/media/widgetkit/widgets/slideshow/styles/default/images/buttons.png',
    '/media/widgetkit/widgets/slideshow/styles/default/images/nav.png',
    '/media/widgetkit/widgets/spotlight/images/magnifier.png',
    '/media/widgetkit/widgets/twitter/styles/bubbles/images/arrow.png',
    '/media/widgetkit/widgets/twitter/styles/single/images/bird.png'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

base = 'https://www.onehealing.gr'

for u in urls:
    local_path = os.path.join('public', u.lstrip('/'))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    full_url = base + u
    try:
        r = requests.get(full_url, headers=headers, timeout=10)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(r.content)
            print(f'Downloaded: {u} -> {local_path}')
        else:
            print(f'Not found ({r.status_code}): {full_url}')
    except Exception as e:
        print(f'Error downloading {full_url}: {e}')
