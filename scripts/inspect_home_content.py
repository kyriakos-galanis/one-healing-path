import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('main', class_='tm-content')
if not content:
    content = soup.find(class_='tm-content')
if content:
    print(content.prettify()[:2000])
