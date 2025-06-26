# Realistic Handwriting Renderer with Procedural Smudge and Pen Pressure
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# =========================
#       USER INPUT
# =========================

def get_text():
    if input("Use default text? (y/n): ").strip().lower() == "y":
        return (
            "This is a realistic handwriting renderer using a custom font. "
            "It includes randomization, effects, smudges, and text wrapping. "
            "Sure! Here’s some random text The curious cat leapt gracefully over the weathered fence, its emerald eyes gleaming in the fading twilight. Nearby, the old oak tree whispered secrets carried by the evening breeze, while distant stars began to twinkle softly in the velvet sky. Somewhere far away, a clock chimed midnight, marking the start of an uncharted adventure."
        ) * 1
    else:
        return input("Enter custom text: ")

# =========================
#       SETTINGS
# =========================

font_path = "Orlandofon-Regular.ttf"
words_per_line = 10
dpi = 300
page_width, page_height = int(8.27 * dpi), int(11.69 * dpi)  # A4 @ 300 dpi
line_spacing = 120
margin_x = 150
margin_y = 150

# === Effects (scale 1–5) ===
blur_strength = 2
shading_strength = 2
crinkle_strength = 1
pen_thickness = 2

# =========================
#       FUNCTIONS
# =========================

def create_lined_background():
    img = Image.new("RGB", (page_width, page_height), "white")
    draw = ImageDraw.Draw(img)
    for y in range(margin_y, page_height - margin_y, line_spacing):
        draw.line((margin_x, y + 40, page_width - margin_x, y + 40), fill=(200, 200, 200), width=1)
    draw.line((margin_x + 40, margin_y, margin_x + 40, page_height - margin_y), fill=(180, 0, 0), width=2)
    return img

def wrap_text(text, words_per_line):
    words = text.split()
    return [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]

def get_supported_chars(font):
    return {chr(c) for c in range(32, 127) if font.getmask(chr(c)).getbbox()}

def generate_smudge(width, height):
    smudge = Image.new("L", (width, height), 0)
    for _ in range(random.randint(3, 8)):
        x0 = random.randint(0, width)
        y0 = random.randint(0, height)
        x1 = x0 + random.randint(10, 50)
        y1 = y0 + random.randint(1, 10)
        draw = ImageDraw.Draw(smudge)
        draw.ellipse([x0, y0, x1, y1], fill=random.randint(100, 180))
    smudge = smudge.filter(ImageFilter.GaussianBlur(3))
    return smudge

def render_page(lines, font_path, base_font_size):
    img = create_lined_background()
    draw = ImageDraw.Draw(img)
    y = margin_y

    font_base = ImageFont.truetype(font_path, base_font_size)
    supported_chars = get_supported_chars(font_base)

    for line in lines:
        x = margin_x + 60
        font_size = base_font_size + random.randint(-2, 2)

        for word in line.split():
            for char in word:
                if char not in supported_chars:
                    continue

                size_jitter = random.uniform(0.95, 1.05) * (1 + pen_thickness * 0.03)
                f = ImageFont.truetype(font_path, int(font_size * size_jitter))
                angle = random.uniform(-2, 2)
                y_offset = random.randint(-3, 3)

                # Create character image
                char_img = Image.new("L", (100, 100), 0)
                draw_char = ImageDraw.Draw(char_img)

                # Simulate pen pressure
                pressure = random.uniform(0.6, 1.0)
                draw_char.text((0, 0), char, font=f, fill=int(255 * pressure))

                # Apply smudging
                blur_radius = random.uniform(0.6, 1.5)
                char_img = char_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                smudge_layer = char_img.copy().filter(ImageFilter.GaussianBlur(radius=1.2))
                smudge_layer = ImageChops.offset(smudge_layer, random.randint(-1, 1), random.randint(-1, 1))
                combined = ImageChops.lighter(char_img, smudge_layer)

                # Rotate and paste
                rotated = combined.rotate(angle, resample=Image.BICUBIC, expand=1)
                mask = rotated
                black_char = Image.new("RGB", mask.size, (0, 0, 0))
                img.paste(black_char, (int(x), int(y + y_offset)), mask)

                spacing = random.randint(5, 10)
                x += f.getlength(char) + spacing

            x += random.randint(20, 30)  # Word spacing

        if random.random() < 0.4:
            smudge = generate_smudge(80, 20)
            smudge_rgba = Image.new("RGBA", smudge.size)
            smudge_rgba.putalpha(smudge)
            smudge_colored = Image.new("RGBA", smudge.size, (0, 0, 0, 0))
            smudge_colored = Image.alpha_composite(smudge_colored, smudge_rgba)
            smudge_colored = smudge_colored.rotate(random.uniform(-10, 10))
            img.paste(smudge_colored, (int(x), int(y + 15)), smudge_colored)

        y += line_spacing

    return img

def apply_effects(img):
    np_img = np.array(img)

    if shading_strength > 0:
        noise = np.random.normal(0, shading_strength * 1.2, np_img.shape).astype(np.int16)
        np_img = np.clip(np_img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    if crinkle_strength > 0:
        for i in range(np_img.shape[0]):
            offset = int(np.sin(i / 25.0) * crinkle_strength)
            np_img[i] = np.roll(np_img[i], offset, axis=0)

    img = Image.fromarray(np_img)

    if blur_strength > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur_strength))

    return img

# =========================
#         MAIN
# =========================

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    text = get_text()
    lines = wrap_text(text, words_per_line)
    lines_per_page = (page_height - 2 * margin_y) // line_spacing
    pages = [lines[i:i + lines_per_page] for i in range(0, len(lines), lines_per_page)]

    for i, page_lines in enumerate(pages):
        page = render_page(page_lines, font_path, base_font_size=85)
        page = apply_effects(page)
        page.save(f"output/handwritten_page_{i+1}.png")

    print(f"\n✅ {len(pages)} page(s) rendered to 'output/' with realistic handwriting and ink smudging.")
