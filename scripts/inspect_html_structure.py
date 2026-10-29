import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('File size:', len(text))
keywords = ['tm-toolbar', 'tm-headerbar', 'tm-navbar', 'tm-sliderbar', 'tm-middle', 'tm-main', 'tm-sidebar-b', 'tm-bottom-b', 'tm-footer', 'id="offcanvas"']
for kw in keywords:
    m = re.search(kw, text)
    if m:
        pos = m.start()
        print(f'{kw} found at {pos}')
    else:
        print(f'{kw} NOT found')
