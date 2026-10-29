import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scraped_data/live_pages_raw/el.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('tm-sliderbar')
end = text.find('tm-middle')

print("Length between tm-sliderbar and tm-middle:", end - start)
print(text[start:end])
