import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el__item__16-alexithymia.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('main', class_='tm-content')
if content:
    print(content.prettify()[:1500])
