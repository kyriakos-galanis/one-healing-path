import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("--- SLIDERBAR ---")
sb = soup.find(class_='tm-sliderbar')
if sb:
    print(sb.prettify()[:2500])

print("\n--- SIDEBAR ---")
sdb = soup.find(class_='tm-sidebar-b')
if sdb:
    print(sdb.prettify()[:2500])

print("\n--- FOOTER COMPLETE ---")
ft = soup.find('footer', class_='tm-footer')
if ft:
    print(ft.prettify())
