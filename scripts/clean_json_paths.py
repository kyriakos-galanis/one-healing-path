import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

for fpath in ['src/data/pagesContent.json', 'src/data/siteData.json']:
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Clean string paths
    def clean_obj(obj):
        if isinstance(obj, dict):
            return {k: clean_obj(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_obj(v) for v in obj]
        elif isinstance(obj, str):
            if obj.startswith('/images/') and obj.endswith('\\'):
                return obj.rstrip('\\')
            if 'P7270094' in obj:
                # Also support normalized name
                pass
            return obj
        return obj

    cleaned = clean_obj(data)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    print(f"Cleaned {fpath}")

