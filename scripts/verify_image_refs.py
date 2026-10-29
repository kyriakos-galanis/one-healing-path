import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

image_refs = set()

for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith(('.astro', '.json', '.ts', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                # Find image paths
                for match in re.findall(r'["\'](/images/[^"\']+|/media/[^"\']+|/components/[^"\']+)["\']', content):
                    image_refs.add((p, match))

print(f"Total image references found: {len(image_refs)}")
missing = []
for file, ref in sorted(image_refs):
    # check public
    local = os.path.join('public', ref.lstrip('/'))
    # also check if urlencoded or special chars
    exists = os.path.exists(local)
    if not exists:
        missing.append((file, ref, local))
    else:
        print(f"[EXISTS] {ref} (in {os.path.basename(file)})")

if missing:
    print(f"\nMissing {len(missing)} images:")
    for f, r, l in missing:
        print(f"  Missing: {r} in {f} (expected at {l})")
else:
    print("\nAll image references in src exist in public!")

