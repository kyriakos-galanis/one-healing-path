import os
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("=== BODY ATTRIBUTES ===")
print(soup.body.attrs if soup.body else None)

print("\n=== TOP LEVEL DIVS UNDER BODY ===")
for child in soup.body.children:
    if getattr(child, 'name', None) == 'div':
        print(f"Div: id='{child.get('id', '')}', class='{child.get('class', [])}'")

print("\n=== TM-SHEET CONTENTS ===")
sheet = soup.find(class_='tm-sheet')
if sheet:
    for child in sheet.children:
        if getattr(child, 'name', None):
            print(f"  {child.name}: id='{child.get('id', '')}', class='{child.get('class', [])}'")

print("\n=== SIDEBAR CONTENTS ===")
sidebar = soup.find('aside', class_='tm-sidebar-b')
if sidebar:
    for mod in sidebar.find_all(class_='uk-panel'):
        title = mod.find(class_='uk-panel-title')
        print("  Module:", title.get_text(strip=True) if title else "No title")

print("\n=== FOOTER CONTENTS ===")
footer = soup.find('footer')
if footer:
    print(footer.prettify()[:1000])
