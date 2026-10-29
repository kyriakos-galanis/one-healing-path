import urllib.request
import ssl
import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.onehealing.gr/el/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8', errors='ignore')

with open('scraped_data/live_home.html', 'w', encoding='utf-8') as f:
    f.write(html)

soup = BeautifulSoup(html, 'html.parser')

print('=== HEAD TAGS & FONTS ===')
for link in soup.find_all('link'):
    print(link)

print('\n=== INLINE STYLES / SCRIPTS IN HEAD ===')
for style in soup.find_all('style'):
    print(style.get_text()[:300])

print('\n=== HEADER / LOGO ===')
header = soup.find(class_=re.compile(r'header|brand|logo|tm-'))
if header:
    print(header.prettify()[:1000])

print('\n=== NAV STRUCTURE ===')
nav = soup.find('nav') or soup.find(class_=re.compile(r'navbar|menu'))
if nav:
    print(nav.prettify()[:1500])

print('\n=== SLIDER / HERO ===')
hero = soup.find(class_=re.compile(r'wk-slideshow|slideshow|slider'))
if hero:
    print(hero.prettify()[:1500])

print('\n=== FOOTER ===')
footer = soup.find('footer') or soup.find(class_=re.compile(r'footer|tm-footer'))
if footer:
    print(footer.prettify()[:1500])

