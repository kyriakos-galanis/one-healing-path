import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = glob.glob('scraped_data/json/*.json')
for f in sorted(files):
    d = json.load(open(f, encoding='utf-8'))
    print(f"{os.path.basename(f)} | title: {d.get('title')} | html_len: {len(d.get('clean_html', ''))}")

