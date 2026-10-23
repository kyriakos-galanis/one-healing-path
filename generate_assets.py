import os
from PIL import Image, ImageDraw, ImageFont

def make_gradient(width, height, color1, color2, label, subtitle=""):
    img = Image.new("RGBA", (width, height), color1)
    draw = ImageDraw.Draw(img)
    # Simple linear interpolation gradient
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    # Border
    draw.rectangle([0, 0, width-1, height-1], outline=(119, 71, 55, 120), width=2)

    # Decorative circle/motif
    center_x, center_y = width // 2, height // 2
    r_circle = min(width, height) // 5
    if r_circle > 15:
        draw.ellipse([center_x - r_circle, center_y - r_circle - 15,
                      center_x + r_circle, center_y + r_circle - 15],
                     outline=(163, 233, 236, 100), width=3)

    # Draw text if possible
    try:
        font = ImageFont.truetype("arial.ttf", max(16, min(width // 20, 28)))
        subfont = ImageFont.truetype("arial.ttf", max(12, min(width // 30, 16)))
    except:
        font = ImageFont.load_default()
        subfont = ImageFont.load_default()

    draw.text((width // 2, height // 2 + 10), label, fill=(255, 255, 255, 240), anchor="mm", font=font)
    if subtitle:
        draw.text((width // 2, height // 2 + 40), subtitle, fill=(163, 233, 236, 220), anchor="mm", font=subfont)

    return img

def create_logo(width=280, height=130):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Logo emblem (spiral / circle symbol)
    draw.ellipse([20, 30, 80, 90], outline=(119, 71, 55, 255), width=4)
    draw.ellipse([32, 42, 68, 78], fill=(163, 233, 236, 200), outline=(119, 71, 55, 180), width=2)
    draw.ellipse([44, 54, 56, 66], fill=(119, 71, 55, 255))

    try:
        font_title = ImageFont.truetype("georgia.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 11)
        font_doc = ImageFont.truetype("arial.ttf", 10)
    except:
        font_title = font_sub = font_doc = ImageFont.load_default()

    draw.text((95, 35), "One Healing", fill=(119, 71, 55, 255), font=font_title)
    draw.text((97, 68), "ONE WITH THE MULTIPLE COSMOS", fill=(130, 100, 90, 220), font=font_sub)
    draw.text((97, 85), "Dr. Panagiotis Gkinis MD, cAc", fill=(70, 80, 85, 200), font=font_doc)
    return img

# Assets to generate
ASSETS = {
    # Logos
    "public/images/logo/One_Healing___Logo___mirror___transparent_background1.png": (280, 130, "logo"),
    "public/images/logo/logo.png": (280, 130, "logo"),
    "public/images/logo/OneHealingPath___Logo-2_copy.png": (180, 80, "logo"),
    "public/images/OneHealingPath___Logo-1.png": (280, 130, "logo"),
    
    # Hero slides
    "public/images/home.jpg": (1200, 600, "One Healing", "Health • Body • Mind", (70, 80, 85), (119, 71, 55)),
    "public/images/slide2.jpg": (1200, 600, "Balance Method", "Dr. Tan Acupuncture", (50, 75, 80), (80, 110, 115)),
    "public/images/slide3.jpg": (1200, 600, "Trauma-Informed Psychotherapy", "Mind-Body Integration", (80, 65, 60), (120, 85, 75)),
    
    # Doctor portrait & therapeutic pages
    "public/images/trxt.png": (400, 600, "Dr. Panagiotis Gkinis", "MD, cAc - Psychiatrist & Acupuncturist", (80, 85, 90), (119, 71, 55)),
    "public/images/seagulls.jpg": (1200, 500, "Psychiatry & Evidence-Based Medicine", "One Healing Path", (70, 90, 100), (120, 140, 150)),
    "public/images/Li_Gan2.JPG": (800, 500, "Balance Method (Li Gan, Jian Ying)", "Acupuncture 1, 2, 3", (90, 75, 70), (140, 95, 80)),
    "public/images/healing-sheng.jpg": (600, 350, "Trauma-Informed Therapy", "One Healing Practice", (75, 85, 80), (110, 125, 115)),
    
    # Articles
    "public/images/Chen_Xiaowang.jpg": (800, 500, "Chen Xiaowang", "Tai Chi Chuan Lineage", (70, 85, 75), (105, 125, 110)),
    "public/images/me_laoshu_crop.JPG": (800, 500, "Personal Practice", "Tai Chi Chuan Path", (80, 75, 70), (120, 110, 100)),
    "public/images/interstitium.jpg": (800, 500, "Interstitium", "Medicine & Meridians", (60, 75, 85), (90, 115, 130)),
    "public/images/velonismos_farmaka.jpg": (800, 500, "Acupuncture or Medication?", "Complementary Medicine", (85, 70, 60), (125, 95, 80)),
    "public/images/slide2.JPG": (1200, 600, "Balance Method", "Dr. Tan Acupuncture", (50, 75, 80), (80, 110, 115)),
    "public/images/P7125265.JPG": (800, 500, "Alexithymia", "Emotion & Mind-Body Connection", (70, 75, 85), (100, 110, 120)),
    "public/images/P7270094_αντίγραφο.JPG": (800, 500, "Psychological Trauma", "Modern Revolutionary Insights", (85, 70, 75), (125, 90, 95)),
    "public/images/P5111555_copy.jpg": (800, 500, "Tai Chi Chuan", "A Martial Art in the Service of Medicine", (65, 80, 75), (95, 115, 105)),
    "public/images/P8102711_copy.JPG": (800, 500, "Personal Experience", "Journey with Tai Chi Chuan", (75, 70, 65), (115, 105, 95)),
    
    # K2 cached article images
    "public/media/k2/items/cache/d61d44254608dd06ccdd2ff02982d14d_L.jpg": (874, 490, "Interstitium", "Eastern Medicine & Modern Anatomy", (60, 75, 85), (90, 115, 130)),
    "public/media/k2/items/cache/d61d44254608dd06ccdd2ff02982d14d_XL.jpg": (1200, 675, "Interstitium", "Eastern Medicine & Modern Anatomy", (60, 75, 85), (90, 115, 130)),
    "public/media/k2/items/cache/d61d44254608dd06ccdd2ff02982d14d_M.jpg": (600, 340, "Interstitium", "Eastern Medicine & Modern Anatomy", (60, 75, 85), (90, 115, 130)),
    "public/media/k2/items/cache/d61d44254608dd06ccdd2ff02982d14d_Generic.jpg": (600, 340, "Interstitium", "Eastern Medicine & Modern Anatomy", (60, 75, 85), (90, 115, 130)),
    
    "public/media/k2/items/cache/9caa2793658f3cc387f216157300b1ce_L.jpg": (874, 490, "Acupuncture or Medication?", "A Trap Question", (85, 70, 60), (125, 95, 80)),
    "public/media/k2/items/cache/9caa2793658f3cc387f216157300b1ce_XL.jpg": (1200, 675, "Acupuncture or Medication?", "A Trap Question", (85, 70, 60), (125, 95, 80)),
    "public/media/k2/items/cache/9caa2793658f3cc387f216157300b1ce_M.jpg": (600, 340, "Acupuncture or Medication?", "A Trap Question", (85, 70, 60), (125, 95, 80)),
    "public/media/k2/items/cache/9caa2793658f3cc387f216157300b1ce_Generic.jpg": (600, 340, "Acupuncture or Medication?", "A Trap Question", (85, 70, 60), (125, 95, 80)),
    
    # Icons & user avatars
    "public/media/contacts/images/con_address.png": (24, 24, "icon"),
    "public/media/contacts/images/emailButton.png": (24, 24, "icon"),
    "public/components/com_k2/images/placeholder/user.png": (100, 100, "avatar"),
}

for path, info in ASSETS.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if info[2] == "logo":
        img = create_logo(info[0], info[1])
        img.save(path)
    elif info[2] == "icon":
        img = Image.new("RGBA", (24, 24), (119, 71, 55, 200))
        img.save(path)
    elif info[2] == "avatar":
        img = Image.new("RGBA", (100, 100), (163, 233, 236, 150))
        draw = ImageDraw.Draw(img)
        draw.ellipse([15, 15, 85, 85], fill=(119, 71, 55, 220))
        img.save(path)
    else:
        w, h, label, sub, c1, c2 = info
        img = make_gradient(w, h, c1, c2, label, sub)
        if path.endswith(".png"):
            img.save(path)
        else:
            img.convert("RGB").save(path, quality=90)

print(f"Generated {len(ASSETS)} placeholder assets in public/")
