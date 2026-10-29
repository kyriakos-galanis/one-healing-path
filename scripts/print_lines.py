import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[240:340], start=241):
    print(f"{i:4d}: {line.rstrip()}")
