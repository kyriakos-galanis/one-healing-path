import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("--- 1. TM-TOOLBAR ---")
tb = soup.find('div', class_='tm-toolbar')
if tb:
    print(tb.prettify()[:1000])

print("\n--- 2. TM-HEADERBAR ---")
hb = soup.find('div', class_='tm-headerbar')
if hb:
    print(hb.prettify())

print("\n--- 3. TM-NAVBAR ---")
nb = soup.find('nav', class_='tm-navbar')
if not nb:
    nb = soup.find(class_='tm-navbar')
if nb:
    print(nb.prettify()[:1500])

print("\n--- 4. OFFCANVAS ---")
oc = soup.find(id='offcanvas')
if oc:
    print(oc.prettify()[:1000])

print("\n--- 5. FOOTER ---")
ft = soup.find('footer', class_='tm-footer')
if ft:
    print(ft.prettify()[:2000])
