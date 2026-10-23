import json
import os
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

pages_to_extract = [
    {
        'key': 'velonismos',
        'file': 'scraped_data/clean_html/el__therapeftiki-proseggisi__velonismos.html',
        'title': 'Βελονισμός - onehealing.gr',
        'heading': 'Βελονισμός',
        'description': 'Βελονισμός Tan Balance Method από τον ιατρό Παναγιώτη Γκίνη MD, CAc.',
        'breadcrumbs': [
            {'label': 'Αρχική', 'href': '/el/'},
            {'label': 'Θεραπευτική Προσέγγιση', 'href': '/el/therapeftiki-proseggisi'},
            {'label': 'Βελονισμός'}
        ]
    },
    {
        'key': 'onehealing',
        'file': 'scraped_data/clean_html/el__therapeftiki-proseggisi__onehealing.html',
        'title': 'One Healing - Ψυχοθεραπεία - onehealing.gr',
        'heading': 'Ψυχοθεραπεία - One Healing',
        'description': 'Ψυχοθεραπεία One Healing - Trauma Informed Therapy, ατομικές και ομαδικές συνεδρίες.',
        'breadcrumbs': [
            {'label': 'Αρχική', 'href': '/el/'},
            {'label': 'Θεραπευτική Προσέγγιση', 'href': '/el/therapeftiki-proseggisi'},
            {'label': 'Ψυχοθεραπεία'}
        ]
    },
    {
        'key': 'psychiatriki',
        'file': 'scraped_data/clean_html/el__therapeftiki-proseggisi__psychiatriki.html',
        'title': 'Ψυχιατρική - onehealing.gr',
        'heading': 'Ψυχιατρική',
        'description': 'Σύγχρονη evidence-based ψυχιατρική στην υπηρεσία της ψυχικής υγείας.',
        'breadcrumbs': [
            {'label': 'Αρχική', 'href': '/el/'},
            {'label': 'Θεραπευτική Προσέγγιση', 'href': '/el/therapeftiki-proseggisi'},
            {'label': 'Ψυχιατρική'}
        ]
    }
]

output_data = {}

for p in pages_to_extract:
    if os.path.exists(p['file']):
        soup = BeautifulSoup(open(p['file'], encoding='utf-8'), 'html.parser')
        content_div = soup.find(class_='tm-article-content')
        if not content_div:
            content_div = soup.find('article') or soup
        
        # Clean internal URLs if any still refer to old index.php
        html_str = str(content_div)
        html_str = html_str.replace('http://www.onehealingpath.gr', '')
        html_str = html_str.replace('/el/therapeftiki-proseggisi/symvoules-gia-tin-ygeia', '/el/therapeftiki-proseggisi/psychiatriki')
        html_str = html_str.replace('/el/therapeftiki-proseggisi/healing-sheng-el', '/el/therapeftiki-proseggisi/onehealing')
        
        output_data[p['key']] = {
            'title': p['title'],
            'heading': p['heading'],
            'description': p['description'],
            'breadcrumbs': p['breadcrumbs'],
            'contentHtml': html_str
        }
        print(f"Extracted {p['key']} ({len(html_str)} chars)")

with open('src/data/pagesContent.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("Saved pagesContent.json successfully!")
