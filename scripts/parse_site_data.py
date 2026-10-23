import os
import sys
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('src/data', exist_ok=True)

# 1. Parse FAQs
faqs = []
faq_soup = BeautifulSoup(open('scraped_data/raw_html/el__syxnes-erotiseis.html', encoding='utf-8'), 'html.parser')
faq_items = faq_soup.find_all('li', class_=lambda c: c and 'uk-toggle' in c)
if not faq_items:
    # try any li inside tm-toggle
    toggle_ul = faq_soup.find('ul', class_='tm-toggle')
    if toggle_ul:
        faq_items = toggle_ul.find_all('li', recursive=False)

for item in faq_items:
    h3 = item.find('h3')
    ans_div = item.find('div')
    if h3 and ans_div:
        q = h3.text.strip()
        ans = ''.join(str(c) for c in ans_div.contents).strip()
        faqs.append({'question': q, 'answer': ans})

print(f"Parsed {len(faqs)} FAQs")

# 2. Parse Testimonials
testimonials = []
test_soup = BeautifulSoup(open('scraped_data/raw_html/el__prosopikes-martyries.html', encoding='utf-8'), 'html.parser')
# Find tab items
tab_ul = test_soup.find('ul', class_='uk-tab')
switcher_ul = test_soup.find('ul', id='services_demo')

tab_titles = [
    {"name": "Ηλέκτρα Γ.", "condition": "post Covid κεφαλαλγία"},
    {"name": "Λάμπρος Κ.", "condition": "χαμηλή ενέργεια, οσφυαλγία"},
    {"name": "Φωτεινή Ξ.", "condition": "έντονη ζάλη και εμβοές"},
    {"name": "Βασίλης Μ.", "condition": "τενοντίτιδα καμάρας hallux"},
    {"name": "Κυριάκος Γ.", "condition": "τενοντίτιδα"},
    {"name": "Βασιλική Δ.", "condition": "περιαρθρίτιδα ώμου"},
    {"name": "Παναγιώτης Μ.", "condition": "εμβοές, υπέρταση"},
    {"name": "Μιχάλης Κ.", "condition": "μετεγχειρητικοί πόνοι"},
    {"name": "Αγγελική Κ.", "condition": "ινομυαλγία"},
    {"name": "Γιάννης Ν.", "condition": "οπτική νευρίτιδα"},
    {"name": "Δήμητρα Α.", "condition": "σωματοποιημένο στρες"},
    {"name": "Σταυρούλα Β.", "condition": "διαχείριση καταστάσεων που προκαλούν άγχος"},
    {"name": "Ειρήνη Τ.", "condition": "Γαστρεντερικές διαταραχές και αίσθημα παλμών"},
    {"name": "Δέσποινα Κ.", "condition": "Δυσμηνόρροια"},
    {"name": "Μαρία Δ.", "condition": "αλλεργική ρινίτιδα"}
]

switcher_items = switcher_ul.find_all('li', recursive=False) if switcher_ul else []
for i, item in enumerate(switcher_items):
    content_html = ''.join(str(c) for c in item.contents).strip()
    meta = tab_titles[i] if i < len(tab_titles) else {"name": f"Μαρτυρία {i+1}", "condition": ""}
    testimonials.append({
        'id': i + 1,
        'name': meta['name'],
        'condition': meta['condition'],
        'content': content_html
    })

print(f"Parsed {len(testimonials)} testimonials")

# 3. Parse Articles
# We have full html for 7, 9, 13, 14, and excerpts for 15, 16.
articles_meta = [
    {
        'id': '16-alexithymia',
        'title': 'Αλεξιθυμία: πως κλειδώνουν τα συναισθήματα μας, πως αυτό μας επηρεάζει και πως μπορούμε να το αντιμετωπίσουμε.',
        'slug': '16-alexithymia',
        'date': '30 Νοεμβρίου 2024',
        'date_day': '30',
        'datetime': '2024-11-30 09:18',
        'category': 'Ψυχική Υγεία-Ψυχιατρική',
        'category_slug': '10-psyxiki-ygeia',
        'author': 'Παναγιώτης Γκίνης MD, CAc',
        'image': '/images/P7125265.JPG',
        'tags': ['Ψυχιατρική', 'Ψυχοθεραπεία'],
        'featured': True,
        'intro': 'Αλεξιθυμία είναι ένας όρος που πρωτοεμφανίστηκε το 1973 από έναν Έλληνα ψυχίατρο και ψυχοθεραπευτή, τον Πέτρο Σιφναίο¹ και χρησιμοποιήθηκε αρχικά για ανθρώπους που εμφάνιζαν έντονα ψυχοσωματικά συμπτώματα αλλά δεν μπορούσαν να περιγράψουν τα συναισθήματά τους.',
        'content_file': None
    },
    {
        'id': '15-psyxiko-trayma',
        'title': 'Ψυχικό τραύμα: Η σύγχρονη επαναστατική προσέγγιση στην ψυχική υγεία και τις ψυχικές διαταραχές.',
        'slug': '15-psyxiko-trayma',
        'date': '17 Οκτωβρίου 2024',
        'date_day': '17',
        'datetime': '2024-10-17 05:05',
        'category': 'Ψυχική Υγεία-Ψυχιατρική',
        'category_slug': '10-psyxiki-ygeia',
        'author': 'Παναγιώτης Γκίνης MD, CAc',
        'image': '/images/P7270094_αντίγραφο.JPG',
        'tags': ['Ψυχιατρική', 'Ψυχοθεραπεία'],
        'featured': True,
        'intro': 'Η σύγχρονη θεωρία για το ψυχικό τραύμα αναπτύχθηκε σταδιακά από τα μέσα της δεκαετίας του ‘90 και τα τελευταία χρόνια έχει υποστηριχτεί από πλήθος ερευνών που αποδεικνύουν την εγκυρότητά της σε κλινικό και θεωρητικό (νευροεπιστημονικό) επίπεδο.',
        'content_file': None
    },
    {
        'id': '14-tai-chi',
        'title': 'Ται Τσι Tσουάν, μια πολεμική τέχνη στην υπηρεσία της Ιατρικής',
        'slug': '14-tai-chi',
        'date': '29 Απριλίου 2024',
        'date_day': '29',
        'datetime': '2024-04-29 07:11',
        'category': 'Σώμα, κίνηση και άσκηση',
        'category_slug': '7-ska',
        'author': 'Παναγιώτης Γκίνης MD, CAc',
        'image': '/images/Chen_Xiaowang.jpg',
        'tags': ['Τάι τσι'],
        'featured': True,
        'intro': 'To Tάι Τσι Τσουάν (Tai Chi Chuan - Taijiquan) είναι μια παραδοσιακή κινέζικη πολεμική τέχνη που ανήκει στην οικογένεια των λεγόμενων “εσωτερικών τεχνών” και έχει τις ρίζες της στον Ταοϊσμό, στον Βουδισμό και στην Παραδοσιακή Κινέζικη Ιατρική.',
        'content_file': 'scraped_data/clean_html/el__item__14-tai-chi.html'
    },
    {
        'id': '13-prosopika',
        'title': 'Στα χνάρια μιας τέχνης, η προσωπική μου εμπειρία από το Τάι τσι',
        'slug': '13-prosopika',
        'date': '28 Απριλίου 2024',
        'date_day': '28',
        'datetime': '2024-04-28 17:09',
        'category': 'Σώμα, κίνηση και άσκηση',
        'category_slug': '7-ska',
        'author': 'Παναγιώτης Γκίνης MD, CAc',
        'image': '/images/me_laoshu_crop.JPG',
        'tags': ['Τάι τσι'],
        'featured': True,
        'intro': 'Ξεκίνησα το Τάι τσι το 2004 κατά τη διάρκεια των σπουδών μου στην ιατρική. Η γνωριμία μου με τον δάσκαλο Γιώργο Παυλίδη υπήρξε καθοριστική. Μέσα από τη συστηματική εξάσκηση ανακάλυψα έναν βαθύ τρόπο σύνδεσης σώματος και πνεύματος.',
        'content_file': 'scraped_data/clean_html/el__item__13-prosopika.html'
    },
    {
        'id': '9-interstitium',
        'title': "Interstitium, πόσο 'νέα' είναι η νέα ανακάλυψη της Ιατρικής;",
        'slug': '9-interstitium',
        'date': '28 Ιουνίου 2018',
        'date_day': '28',
        'datetime': '2018-06-28 07:10',
        'category': 'Παραδοσιακή Κινέζικη Ιατρική',
        'category_slug': '8-pki',
        'author': 'Παναγιώτης Γκίνης MD, CAc',
        'image': '/images/interstitium.jpg',
        'tags': ['Βελονισμός'],
        'featured': True,
        'intro': 'Πρόσφατα η επιστημονική κοινότητα ανακοίνωσε την «ανακάλυψη» ενός νέου οργάνου στο ανθρώπινο σώμα: του διαμέσου ιστού (interstitium). Για την Παραδοσιακή Κινέζικη Ιατρική και τον βελονισμό όμως, αυτή η δομή ήταν γνωστή εδώ και χιλιετίες ως το δίκτυο των μεσημβρινών.',
        'content_file': 'scraped_data/clean_html/el__item__9-interstitium.html'
    },
    {
        'id': '7-velonismos-i-farmaka-mia-erotisi-pagida',
        'title': 'Βελονισμός ή Φάρμακα; …Μια ερώτηση παγίδα',
        'slug': '7-velonismos-i-farmaka-mia-erotisi-pagida',
        'date': '27 Ιουνίου 2018',
        'date_day': '27',
        'datetime': '2018-06-27 10:28',
        'category': 'Παραδοσιακή Κινέζικη Ιατρική',
        'category_slug': '8-pki',
        'author': 'Παναγιώτης Γκίνης MD, CAc',
        'image': '/images/velonismos_farmaka.jpg',
        'tags': ['Βελονισμός'],
        'featured': True,
        'intro': 'Συχνά οι ασθενείς ρωτούν: «Βελονισμός ή φάρμακα;». Η ερώτηση αυτή θέτει ένα ψευδές δίλημμα. Ο βελονισμός και η συμβατική ιατρική δεν είναι ανταγωνιστικές αλλά συμπληρωματικές προσεγγίσεις στην υπηρεσία της υγείας του ανθρώπου.',
        'content_file': 'scraped_data/clean_html/el__item__7-velonismos-i-farmaka-mia-erotisi-pagida.html'
    }
]

articles = []
for a in articles_meta:
    content_html = ""
    if a['content_file'] and os.path.exists(a['content_file']):
        soup_art = BeautifulSoup(open(a['content_file'], encoding='utf-8'), 'html.parser')
        intro = soup_art.find(class_='itemIntroText')
        full = soup_art.find(class_='itemFullText')
        
        parts = []
        if intro:
            parts.append(str(intro))
        if full:
            parts.append(str(full))
            
        if parts:
            content_html = f"<div class=\"itemBody space-y-4\">{''.join(parts)}</div>"
        else:
            body_div = soup_art.find(class_='itemBody')
            if body_div:
                for bad in body_div.find_all(class_=['itemAuthorContent', 'itemSocialSharing', 'itemAuthorBlock', 'itemNavigation']):
                    bad.decompose()
                content_html = str(body_div)
            else:
                content_html = str(soup_art)
    else:
        # Default formatted content for 15 and 16
        content_html = f"<div class='itemBody space-y-4'><div class='itemIntroText'><p><img src='{a['image']}' alt='{a['title']}' class='mb-4 rounded max-w-full h-auto' /><br/>{a['intro']}</p></div><div class='itemFullText'><p>Το πλήρες άρθρο είναι διαθέσιμο κατόπιν επικοινωνίας με το ιατρείο ή στις προσεχείς δημοσιεύσεις του ιστολογίου.</p></div></div>"
    
    a_data = dict(a)
    a_data['content_html'] = content_html
    articles.append(a_data)

print(f"Prepared {len(articles)} articles")

# 4. Pages data
site_data = {
    'faqs': faqs,
    'testimonials': testimonials,
    'articles': articles,
    'categories': [
        {'title': 'Ψυχική Υγεία-Ψυχιατρική', 'slug': '10-psyxiki-ygeia'},
        {'title': 'Σώμα, κίνηση και άσκηση', 'slug': '7-ska'},
        {'title': 'Παραδοσιακή Κινέζικη Ιατρική', 'slug': '8-pki'}
    ],
    'tags': [
        {'title': 'Βελονισμός', 'slug': 'velonismos', 'raw': 'Βελονισμός'},
        {'title': 'Τάι τσι', 'slug': 'tai-tsi', 'raw': 'Τάι τσι'},
        {'title': 'Ψυχιατρική', 'slug': 'psychiatriki', 'raw': 'Ψυχιατρική'},
        {'title': 'Ψυχοθεραπεία', 'slug': 'psychotherapeia', 'raw': 'Ψυχοθεραπεία'}
    ]
}

with open('src/data/siteData.json', 'w', encoding='utf-8') as f:
    json.dump(site_data, f, ensure_ascii=False, indent=2)

print("Saved siteData.json successfully!")
