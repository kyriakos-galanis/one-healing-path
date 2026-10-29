import os
import sys
from bs4 import BeautifulSoup, Tag

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

def print_tree(elem, indent=0):
    if not isinstance(elem, Tag):
        return
    classes = ".".join(elem.get('class', []))
    id_str = f"#{elem.get('id')}" if elem.get('id') else ""
    summary = f"{elem.name}{id_str}{('.' + classes) if classes else ''}"
    
    # Don't recurse deep into article text or svg
    if 'itemBody' in classes or elem.name in ['script', 'style', 'svg']:
        print("  " * indent + summary + " (...)")
        return
        
    print("  " * indent + summary)
    for child in elem.children:
        print_tree(child, indent + 1)

print_tree(soup.body)
