
from pathlib import Path
from fontTools.ttLib import TTFont

FONT_DIR = Path("assets/fonts")

FONT_DIR.mkdir(parents=True, exist_ok=True)

for font_path in FONT_DIR.glob("*.ttf"):
    font = TTFont(font_path)

    output_path = font_path.with_suffix(".woff2")

    font.flavor = "woff2"
    font.save(output_path)

    print(f"Converted: {font_path.name} -> {output_path.name}")

print("\nFont conversion completed!")