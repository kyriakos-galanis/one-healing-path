import os
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("=== EXACT HEADERBAR ===")
hb = soup.find(class_='tm-headerbar')
if hb:
    print(hb.prettify())

print("\n=== EXACT NAVBAR ===")
nb = soup.find(class_='tm-navbar')
if nb:
    print(nb.prettify())

print("\n=== EXACT SLIDERBAR ===")
sb = soup.find(class_='tm-sliderbar')
if sb:
    print(sb.prettify())

print("\n=== EXACT FOOTER ===")
ft = soup.find('footer')
if ft:
    print(ft.prettify())
