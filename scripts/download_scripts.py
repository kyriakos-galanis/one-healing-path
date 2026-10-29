import os
import sys
import urllib.request
import urllib.parse
import ssl

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

scripts_to_download = [
    '/media/jui/js/jquery.min.js',
    '/media/jui/js/jquery-noconflict.js',
    '/media/jui/js/jquery-migrate.min.js',
    '/media/jui/js/bootstrap.min.js',
    '/cache/widgetkit/widgetkit-2795e87c.js',
    '/templates/saffron/warp/vendor/uikit/js/uikit.js',
    '/templates/saffron/warp/vendor/uikit/js/components/slideshow.js',
    '/templates/saffron/warp/vendor/uikit/js/components/slideshow-fx.js',
    '/templates/saffron/warp/vendor/uikit/js/components/sticky.js',
    '/templates/saffron/warp/vendor/uikit/js/components/grid.js',
    '/templates/saffron/js/core.js',
    '/templates/saffron/js/theme.js',
    '/templates/saffron/apple_touch_icon.png',
]

for s in scripts_to_download:
    url = 'https://www.onehealing.gr' + s
    local_path = os.path.join('public', s.lstrip('/').replace('/', os.sep))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"[OK] {s} ({len(data)} bytes) -> {local_path}")
    except Exception as e:
        print(f"[ERROR] {s}: {e}")

print("Done downloading scripts and icons.")
