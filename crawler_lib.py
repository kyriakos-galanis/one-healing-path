import os
import sys
import re
import time
import json
import urllib.parse
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

sys.stdout.reconfigure(encoding='utf-8')

BASE_TARGET = "http://www.onehealingpath.gr"
WAYBACK_PREFIX = "https://web.archive.org/web/20250521181650id_/"
WAYBACK_IMG_PREFIX = "https://web.archive.org/web/20250521181650im_/"
WAYBACK_CSS_PREFIX = "https://web.archive.org/web/20250521181650cs_/"

DATA_DIR = os.path.abspath("scraped_data")
RAW_HTML_DIR = os.path.join(DATA_DIR, "raw_html")
CLEAN_HTML_DIR = os.path.join(DATA_DIR, "clean_html")
MARKDOWN_DIR = os.path.join(DATA_DIR, "markdown")
JSON_DIR = os.path.join(DATA_DIR, "json")
ASSETS_DIR = os.path.join(DATA_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
CSS_DIR = os.path.join(ASSETS_DIR, "css")

for d in [DATA_DIR, RAW_HTML_DIR, CLEAN_HTML_DIR, MARKDOWN_DIR, JSON_DIR, ASSETS_DIR, IMAGES_DIR, CSS_DIR]:
    os.makedirs(d, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_wayback_url(url: str) -> str:
    """Strip wayback machine wrappers to get canonical url."""
    if not url:
        return ""
    # Remove wayback prefix if present
    match = re.search(r'https?://web\.archive\.org/web/\d+[a-z_]*/(.*)', url)
    if match:
        url = match.group(1)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
    return url

def normalize_internal_url(url: str, base_url: str = BASE_TARGET) -> str:
    """Normalize url relative to base, strip query tracking / fragments."""
    if not url:
        return ""
    url = clean_wayback_url(url)
    
    # Ignore mailto, tel, javascript
    if any(url.lower().startswith(x) for x in ["mailto:", "tel:", "javascript:", "#"]):
        return ""
    
    full = urllib.parse.urljoin(base_url, url)
    parsed = urllib.parse.urlparse(full)
    
    # Must be on onehealingpath.gr
    if "onehealingpath.gr" not in parsed.netloc:
        return ""
    
    # Ignore calendar infinite loops
    if "/calendar/" in parsed.path:
        return ""
    
    # Ignore feeds
    if "format=feed" in parsed.query:
        return ""
        
    # Standardize scheme & host
    clean_path = parsed.path
    if not clean_path:
        clean_path = "/"
        
    # Reassemble url without fragment
    query = f"?{parsed.query}" if parsed.query else ""
    return f"http://www.onehealingpath.gr{clean_path}{query}"

def url_to_slug(url: str) -> str:
    """Create a filesystem-friendly slug for a URL."""
    clean = clean_wayback_url(url)
    parsed = urllib.parse.urlparse(clean)
    path = parsed.path.strip("/")
    if not path or path == "el":
        slug = "home"
    else:
        # replace slashes and dots
        slug = path.replace("/", "__").replace(":", "_")
    if parsed.query:
        q = re.sub(r'[^a-zA-Z0-9_]', '_', parsed.query)
        slug = f"{slug}__{q}"
    return slug[:120]

def fetch_with_retry(url: str, session: requests.Session, max_retries: int = 4, delay: float = 1.0):
    for attempt in range(max_retries):
        try:
            time.sleep(delay)
            resp = session.get(url, headers=HEADERS, timeout=25, allow_redirects=True)
            if resp.status_code == 200:
                return resp
            elif resp.status_code in [429, 503, 502, 504]:
                wait_time = (2 ** attempt) * 2 + 1
                print(f"  [Status {resp.status_code}] Retrying in {wait_time}s for {url}")
                time.sleep(wait_time)
            elif resp.status_code == 404:
                return resp
            else:
                print(f"  [Status {resp.status_code}] for {url}")
                return resp
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            wait_time = (2 ** attempt) * 2 + 2
            print(f"  [ConnError: {e.__class__.__name__}] Retrying in {wait_time}s for {url}")
            time.sleep(wait_time)
        except Exception as e:
            print(f"  [Error: {e}] for {url}")
            return None
    return None

def download_asset(asset_url: str, session: requests.Session, asset_type: str = "image") -> str:
    """Download asset and return local relative path."""
    clean_url = clean_wayback_url(asset_url)
    parsed = urllib.parse.urlparse(clean_url)
    path = parsed.path
    if not path or path == "/":
        return ""
    
    # Choose base dir
    if asset_type == "css" or path.endswith(".css"):
        target_dir = CSS_DIR
        wayback_prefix = WAYBACK_CSS_PREFIX
    else:
        target_dir = IMAGES_DIR
        wayback_prefix = WAYBACK_IMG_PREFIX
        
    filename = os.path.basename(path)
    if not filename:
        return ""
        
    # Unquote URL filename (for greek characters in image filenames)
    filename = urllib.parse.unquote(filename)
    # Sanitize invalid Windows chars
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    
    # Subdirectory structure based on path
    subfolder = os.path.dirname(path).strip("/\\")
    subfolder = urllib.parse.unquote(subfolder)
    subfolder = re.sub(r'[\\*?:"<>|]', '_', subfolder).replace("/", os.sep)
    
    local_dir = os.path.join(target_dir, subfolder)
    os.makedirs(local_dir, exist_ok=True)
    local_filepath = os.path.join(local_dir, filename)
    
    if os.path.exists(local_filepath) and os.path.getsize(local_filepath) > 0:
        return os.path.relpath(local_filepath, DATA_DIR)
        
    # Fetch asset
    fetch_url = f"{wayback_prefix}{clean_url}"
    try:
        time.sleep(0.3)
        resp = session.get(fetch_url, headers=HEADERS, timeout=20)
        if resp.status_code == 200 and resp.content:
            with open(local_filepath, "wb") as f:
                f.write(resp.content)
            print(f"    [Asset Saved] {filename} ({len(resp.content)} bytes)")
            return os.path.relpath(local_filepath, DATA_DIR)
        else:
            print(f"    [Asset Fail {resp.status_code}] {clean_url}")
    except Exception as e:
        print(f"    [Asset Error] {e} on {clean_url}")
        
    return ""

def extract_page_data(html: str, page_url: str):
    soup = BeautifulSoup(html, "html.parser")
    
    # Title
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    
    # Meta tags
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if desc_tag:
        meta_desc = desc_tag.get("content", "").strip()
        
    meta_keywords = ""
    kw_tag = soup.find("meta", attrs={"name": "keywords"})
    if kw_tag:
        meta_keywords = kw_tag.get("content", "").strip()
        
    # Headings
    headings = []
    for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        htext = h.get_text(strip=True)
        if htext:
            headings.append({"level": h.name, "text": htext})
            
    # Breadcrumbs
    breadcrumbs = []
    bc = soup.find("ul", class_=re.compile(r"breadcrumb", re.I))
    if bc:
        for li in bc.find_all("li"):
            t = li.get_text(strip=True)
            if t:
                breadcrumbs.append(t)
                
    # Main content identification
    main_content_tag = None
    # Check for specific Joomla / YOOtheme containers
    if "viografiko" in page_url or "therapeftiki-proseggisi" in page_url or "prosopikes" in page_url or "syxnes" in page_url:
        main_content_tag = soup.find("article") or soup.find("main") or soup.find(class_="tm-content")
    elif "item/" in page_url:
        main_content_tag = soup.find(class_=re.compile(r"itemBody|itemView|k2Container")) or soup.find("article") or soup.find("main")
    elif page_url.rstrip("/").endswith("/el") or page_url.rstrip("/").endswith("onehealingpath.gr"):
        # Homepage has slider + main
        main_content_tag = soup.find("div", class_=re.compile(r"tm-middle")) or soup.find("main")
    
    if not main_content_tag:
        main_content_tag = soup.find("article") or soup.find("main") or soup.find(class_=re.compile(r"tm-content|tm-middle|content"))
        
    clean_html = str(main_content_tag) if main_content_tag else ""
    clean_markdown = md(clean_html) if clean_html else ""
    
    # Internal links
    internal_links = set()
    external_links = set()
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        norm = normalize_internal_url(href, page_url)
        if norm:
            internal_links.add(norm)
        elif href.startswith("http://") or href.startswith("https://"):
            if "web.archive.org" not in href:
                external_links.add(href)
            else:
                # clean wayback
                c = clean_wayback_url(href)
                if "onehealingpath.gr" in c:
                    norm_c = normalize_internal_url(c, page_url)
                    if norm_c:
                        internal_links.add(norm_c)
                else:
                    external_links.add(c)
                    
    # Images
    images = set()
    for img in soup.find_all("img", src=True):
        src = img.get("src")
        if src.startswith("data:"):
            continue
        cleaned_src = clean_wayback_url(src)
        full_img_url = urllib.parse.urljoin(BASE_TARGET, cleaned_src)
        if "onehealingpath.gr" in full_img_url:
            images.add(full_img_url)
            
    # CSS
    css_files = set()
    for link in soup.find_all("link", rel=lambda r: r and "stylesheet" in r):
        href = link.get("href")
        if href:
            cleaned_href = clean_wayback_url(href)
            full_css_url = urllib.parse.urljoin(BASE_TARGET, cleaned_href)
            if "onehealingpath.gr" in full_css_url:
                css_files.add(full_css_url)
                
    return {
        "title": title,
        "meta_description": meta_desc,
        "meta_keywords": meta_keywords,
        "breadcrumbs": breadcrumbs,
        "headings": headings,
        "clean_html": clean_html,
        "markdown": clean_markdown,
        "internal_links": sorted(list(internal_links)),
        "external_links": sorted(list(external_links)),
        "images": sorted(list(images)),
        "css_files": sorted(list(css_files))
    }

print("Crawler module ready.")
