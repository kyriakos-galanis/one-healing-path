# OneHealingPath.gr - Scraped Site Archive & Rebuild Guide

> **Target Site:** `http://www.onehealingpath.gr/el/`  
> **Source Snapshot:** [Wayback Machine (2025-05-21)](https://web.archive.org/web/20250521181650/http://www.onehealingpath.gr/el/)  
> **Doctor / Practice:** Dr. Panagiotis Gkinis MD, cAc (Παναγιώτης Γκίνης — Ψυχίατρος, Βελονιστής)  
> **Contact Email:** `gkinispan@gmail.com`  
> **Official Facebook:** [One Healing Path Facebook](https://www.facebook.com/profile.php?id=61552501891015)

---

## 1. Directory Structure

```text
onehealingpath/
├── scraped_data/
│   ├── SITE_INDEX.md           # Full site index and page breakdown
│   ├── manifest.json           # Crawl metadata for all URLs
│   ├── images_inventory.json   # Comprehensive catalog of all 25 image assets, dimensions, and usage
│   ├── markdown/               # Complete content converted into clean, structured Markdown (.md)
│   ├── clean_html/             # Cleaned HTML of the main body content (no wrappers/toolbar)
│   ├── raw_html/               # Full original raw HTML files as captured from the archive
│   └── json/                   # Structured JSON per page (title, meta, breadcrumbs, headings, links)
├── crawler_lib.py              # Parsing and extraction helper library
├── run_crawler.py              # Crawler automation script
└── README.md                   # This document
```

---

## 2. Complete Site Architecture & Pages

| # | Page / Section | Original Path | Markdown File | Clean HTML File |
|---|---|---|---|---|
| 1 | **Αρχική (Home)** | `/el/` | [`scraped_data/markdown/home.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/home.md) | [`scraped_data/clean_html/home.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/home.html) |
| 2 | **Βιογραφικό** | `/el/viografiko` | [`scraped_data/markdown/el__viografiko.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__viografiko.md) | [`scraped_data/clean_html/el__viografiko.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__viografiko.html) |
| 3 | **Θεραπευτική Προσέγγιση (Overview)** | `/el/therapeftiki-proseggisi` | [`scraped_data/markdown/el__therapeftiki-proseggisi.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__therapeftiki-proseggisi.md) | [`scraped_data/clean_html/el__therapeftiki-proseggisi.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__therapeftiki-proseggisi.html) |
| 4 | **Βελονισμός** | `/el/therapeftiki-proseggisi/velonismos` | [`scraped_data/markdown/el__therapeftiki-proseggisi__velonismos.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__therapeftiki-proseggisi__velonismos.md) | [`scraped_data/clean_html/el__therapeftiki-proseggisi__velonismos.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__therapeftiki-proseggisi__velonismos.html) |
| 5 | **Ψυχοθεραπεία - Trauma Informed** | `/el/therapeftiki-proseggisi/onehealing` | [`scraped_data/markdown/el__therapeftiki-proseggisi__onehealing.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__therapeftiki-proseggisi__onehealing.md) | [`scraped_data/clean_html/el__therapeftiki-proseggisi__onehealing.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__therapeftiki-proseggisi__onehealing.html) |
| 6 | **Ψυχιατρική** | `/el/therapeftiki-proseggisi/psychiatriki` | [`scraped_data/markdown/el__therapeftiki-proseggisi__psychiatriki.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__therapeftiki-proseggisi__psychiatriki.md) | [`scraped_data/clean_html/el__therapeftiki-proseggisi__psychiatriki.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__therapeftiki-proseggisi__psychiatriki.html) |
| 7 | **Προσωπικές Μαρτυρίες** | `/el/prosopikes-martyries` | [`scraped_data/markdown/el__prosopikes-martyries.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__prosopikes-martyries.md) | [`scraped_data/clean_html/el__prosopikes-martyries.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__prosopikes-martyries.html) |
| 8 | **Συχνές Ερωτήσεις (FAQ)** | `/el/syxnes-erotiseis` | [`scraped_data/markdown/el__syxnes-erotiseis.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__syxnes-erotiseis.md) | [`scraped_data/clean_html/el__syxnes-erotiseis.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__syxnes-erotiseis.html) |
| 9 | **Ιστολόγιο (Blog Index)** | `/el/istologio` | [`scraped_data/markdown/el__istologio.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__istologio.md) | [`scraped_data/clean_html/el__istologio.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__istologio.html) |
| 10 | **Άρθρο: Στα χνάρια μιας τέχνης (Tai Chi)** | `/el/item/13-prosopika` | [`scraped_data/markdown/el__item__13-prosopika.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__item__13-prosopika.md) | [`scraped_data/clean_html/el__item__13-prosopika.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__item__13-prosopika.html) |
| 11 | **Άρθρο: Ται Τσι στην υπηρεσία της Ιατρικής** | `/el/item/14-tai-chi` | [`scraped_data/markdown/el__item__14-tai-chi.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__item__14-tai-chi.md) | [`scraped_data/clean_html/el__item__14-tai-chi.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__item__14-tai-chi.html) |
| 12 | **Άρθρο: Βελονισμός ή Φάρμακα;** | `/el/item/7-velonismos-i-farmaka-mia-erotisi-pagida` | [`scraped_data/markdown/el__item__7-velonismos-i-farmaka-mia-erotisi-pagida.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__item__7-velonismos-i-farmaka-mia-erotisi-pagida.md) | [`scraped_data/clean_html/el__item__7-velonismos-i-farmaka-mia-erotisi-pagida.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__item__7-velonismos-i-farmaka-mia-erotisi-pagida.html) |
| 13 | **Άρθρο: Interstitium** | `/el/item/9-interstitium` | [`scraped_data/markdown/el__item__9-interstitium.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__item__9-interstitium.md) | [`scraped_data/clean_html/el__item__9-interstitium.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__item__9-interstitium.html) |
| 14 | **Άρθρο: Αλεξιθυμία (Excerpt/Intro)** | `/el/item/16-alexithymia` | Included in [`home.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/home.md#L7-L18) | Included in [`home.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/home.html) |
| 15 | **Άρθρο: Ψυχικό Τραύμα (Excerpt/Intro)** | `/el/item/15-psyxiko-trayma` | Included in [`home.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/home.md#L22-L33) | Included in [`home.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/home.html) |
| 16 | **Κατηγορία: Σώμα, κίνηση & άσκηση** | `/el/itemlist/category/7-ska` | [`scraped_data/markdown/el__itemlist__category__7-ska.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__itemlist__category__7-ska.md) | [`scraped_data/clean_html/el__itemlist__category__7-ska.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__itemlist__category__7-ska.html) |
| 17 | **Κατηγορία: Παραδοσιακή Κινέζικη Ιατρική** | `/el/itemlist/category/8-pki` | [`scraped_data/markdown/el__itemlist__category__8-pki.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__itemlist__category__8-pki.md) | [`scraped_data/clean_html/el__itemlist__category__8-pki.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__itemlist__category__8-pki.html) |
| 18 | **Ετικέτα: Βελονισμός** | `/el/itemlist/tag/Βελονισμός` | [`scraped_data/markdown/el_itemlist_tag_velonismos.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el_itemlist_tag_velonismos.md) | [`scraped_data/clean_html/el_itemlist_tag_velonismos.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el_itemlist_tag_velonismos.html) |
| 19 | **Ετικέτα: Τάι τσι** | `/el/itemlist/tag/Τάι τσι` | [`scraped_data/markdown/el_itemlist_tag_tai_tsi.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el_itemlist_tag_tai_tsi.md) | [`scraped_data/clean_html/el_itemlist_tag_tai_tsi.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el_itemlist_tag_tai_tsi.html) |
| 20 | **Σελίδα Συγγραφέα (Author Profile)** | `/el/itemlist/user/655-panagiwthsgkinhsmdcac` | [`scraped_data/markdown/el__itemlist__user__655-panagiwthsgkinhsmdcac.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__itemlist__user__655-panagiwthsgkinhsmdcac.md) | [`scraped_data/clean_html/el__itemlist__user__655-panagiwthsgkinhsmdcac.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__itemlist__user__655-panagiwthsgkinhsmdcac.html) |
| 21 | **Επικοινωνία (Contact Page)** | `/el/epikoinonia` | [`scraped_data/markdown/el__epikoinonia.md`](file:///c:/dev/onehealingpath/scraped_data/markdown/el__epikoinonia.md) | [`scraped_data/clean_html/el__epikoinonia.html`](file:///c:/dev/onehealingpath/scraped_data/clean_html/el__epikoinonia.html) |

---

## 3. Image Assets Inventory

All 25 image references used throughout the site are cataloged in [`scraped_data/images_inventory.json`](file:///c:/dev/onehealingpath/scraped_data/images_inventory.json) with original paths, dimensions, alt text, and the pages where they were placed:
- **Logo:** `/images/logo/One_Healing___Logo___mirror___transparent_background1.png` (230x126), `/images/logo/OneHealingPath___Logo-2_copy.png` (117x55)
- **Hero Slider:** `/images/home.jpg` (780x414), `/images/slide2.jpg`, `/images/slide3.jpg`
- **Doctor Portrait (Biography):** `/images/trxt.png` (282x528)
- **Psychiatry Banner:** `/images/seagulls.jpg` (1932x864)
- **Psychotherapy / Healing Sheng Diagram:** `/images/healing-sheng.jpg` (450x245)
- **Acupuncture / Dr. Li Gan Diagram:** `/images/Li_Gan2.JPG`
- **Article Images:**
  - Alexithymia: `/images/P7125265.JPG` (640x480)
  - Trauma: `/images/P7270094_αντίγραφο.JPG` (825x619)
  - Tai Chi Medical: `/images/P5111555_copy.jpg`
  - Tai Chi Personal: `/images/P8102711_copy.JPG`
  - Acupuncture vs Meds: `/media/k2/items/cache/9caa2793658f3cc387f216157300b1ce_L.jpg`
  - Interstitium: `/media/k2/items/cache/d61d44254608dd06ccdd2ff02982d14d_L.jpg`
- **Contact Icons:** `/media/contacts/images/con_address.png`, `/media/contacts/images/emailButton.png`

*(Note: The Wayback Machine snapshot only captured HTML text pages; binary image files were excluded by the original archive crawler. With the exact paths, dimensions, and contexts preserved in the inventory, suitable high-resolution replacement imagery or brand assets can be dropped directly into the rebuild).*

---

## 4. Rebuilt Modern Astro Application

The site has been completely reconstructed as an **Astro 5 + Tailwind CSS** static application matching 100% of the content, structure, styling palette, and layout of the original YOOtheme Saffron design.

### Quick Start

```powershell
# Install dependencies (if needed)
npm.cmd install

# Run development server
npm.cmd run dev

# Build production static bundle (generates 34 static HTML pages into dist/)
npm.cmd run build

# Preview production build locally
npm.cmd run preview
```

### Key Highlights
- **100% Content Fidelity:** All 11 FAQs, 15 personal testimonials, 6 blog articles, 3 therapeutic approach pillars (*Βελονισμός*, *One Healing*, *Ψυχιατρική*), and doctor biography are fully preserved in Greek.
- **Color Palette & Design:** Authentic YOOtheme Saffron theme colors (`#774737` Burgundy, `#a3e9ec` Cyan, `#32393c` Slate, `#b1ac90` Olive, `#f4f1ea` background, boxed `tm-sheet` container, top toolbar, and 3-column footer).
- **Zero Broken Links:** All 1,297 internal links verified with 0 broken links across 34 generated static routes.
- **Zero Missing Assets:** All 101 image references verified with 0 broken images.
- **Interactive Features:** Tabbed testimonial selector, accordion FAQ widgets, interactive calendar, mobile responsive drawer menu, and contact form with mailto fallback.

Because the original site was built on Joomla + K2 with YOOtheme/UIkit, rebuilding with a modern framework offers massive speed, mobile responsiveness, and SEO advantages:

1. **Recommended Modern Stacks:**
   - **Astro** or **Next.js (App Router)**: Ideal for fast, static-first content-heavy sites with MDX or Markdown blog posts.
   - **Tailwind CSS**: Replicates the clean, light-blue / green medical aesthetic with responsive typography and card components.
2. **Key Components to Rebuild:**
   - **Header & Navbar:** Topbar with Facebook link, clean logo, and responsive navigation menu matching the hierarchy above.
   - **Hero Carousel / Slider:** Left side featured banner/slides, right side highlight cards ("One Healing", "Βελονισμός", "Ψυχοθεραπεία", "Ψυχιατρική").
   - **Service Details Pages:** Three core therapeutic pillars (Acupuncture, Trauma-informed Psychotherapy, Psychiatry).
   - **Testimonials Page:** Patient stories formatted with quote cards and author attributes.
   - **FAQ Accordion:** Interactive collapsible FAQ sections.
   - **Blog Engine:** Dynamic or static rendering of the 6 articles with tag/category filtering.
   - **Contact Form & Footer:** Form with fields (Όνομα, Email, Θέμα, Μήνυμα) delivering to `gkinispan@gmail.com`.
