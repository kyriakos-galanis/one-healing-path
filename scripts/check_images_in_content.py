import json
with open('src/data/pagesContent.json', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'/images/[a-zA-Z0-9_\-\.]+', text):
    print(m.group(0))
