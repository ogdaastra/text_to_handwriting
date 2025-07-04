# text_to_handwriting
An incredibly advanced but surprisingly easy to set up custom to your own handwriting text to handwriting tool.

## Features

- Custom handwriting font support (.ttf)
- Realistic A4 lined paper rendering
- Handwriting effects:
  - Random pen pressure
  - Ink pooling at stroke ends
  - Per-character blur
  - Line smudges
  - Shading and distortion
  - Ghosting simulation
- Word wrapping with variable spacing
- Paper texture integration

---

## Requirements

- Python 3.8 or newer
- Pillow
- NumPy

Install dependencies:

```bash
pip install pillow numpy
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/realistic-handwriting.git
cd realistic-handwriting
```

### 2. Create Your Own Handwriting Font

You can use [Calligraphr](https://www.calligraphr.com/) to create a font based on your own handwriting:

1. Go to [https://www.calligraphr.com](https://www.calligraphr.com)
2. Create a free account and log in.
3. Click **"Templates"** → **"Minimal English"** or create a custom one.
4. Download the PDF template.
5. Print and fill out the characters using a black pen.
6. Scan the sheet or take a clear photo.
7. Upload your filled template back into Calligraphr.
8. Generate your font and download the `.ttf` file.
9. Save it as "custom_font.ttf"
10. Place the font file in this project's root directory.

Update this line in the script with your font:

```python
font_path = "custom_font.ttf"
```

### 3. [optional] Add a Paper Texture

Place a background texture image (e.g., `papertexture.jpg`) into the project. Update the texture path in the script if needed.

---

## Usage

Run the script:

```bash
python render_text.py
```

Choose default or custom text when prompted.
Output is saved in the `output/` directory as `.png` files.

---

## Configuration

Modify values in `render_text.py` to tweak rendering:

```python
words_per_line = 10
line_spacing = 120
base_font_size = 85
margin_x = 150
margin_y = 150

blur_strength = 2
shading_strength = 2
crinkle_strength = 1
pen_thickness = 2
```

---

## Advanced Effects

- **Pen Pressure:** Characters vary in opacity.
- **Ink Pooling:** Simulates darker, thicker ends of strokes.
- **Smudging:** Random smudges applied to some lines.
- **Ghosting:** Slight text repetition to mimic ink transfer.
- **Crinkle:** Slight wave distortion to simulate paper crumples.
- **Texture:** Overlays random region from a paper texture file.
- **Lift Pressure:** Mimics realistic pen down/up effects.

---

## Alternate Fonts

To switch styles dynamically, include multiple font files:

```python
font_path = random.choice(["Font1.ttf", "Font2.ttf", "Font3.ttf"])
```

---

## Directory Structure

```
.
├── render_text.py
├── YourFontName.ttf
├── papertexture.jpg
├── output/
└── README.md
```


## License

This project is released under the MIT License. You are free to use and adapt the code for personal or commercial use.

---

