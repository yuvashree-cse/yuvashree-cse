from pathlib import Path
import base64
from PIL import Image

# Project paths
ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = ROOT / "hero.svg"
OUTPUT = ROOT / "hero-ready.svg"

IMAGE = ROOT / "assets" / "images" / "waving.png"
OPTIMIZED_IMAGE = ROOT / "assets" / "images" / "waving-hero.png"

FONTS = {
    "__SPACE_REGULAR__": ROOT / "assets/fonts/SpaceGrotesk-Regular.woff2",
    "__SPACE_BOLD__": ROOT / "assets/fonts/SpaceGrotesk-Bold.woff2",
    "__MONO_REGULAR__": ROOT / "assets/fonts/JetBrainsMono-Regular.woff2",
}


def to_base64(file_path):
    """Convert a file into Base64 text."""
    return base64.b64encode(file_path.read_bytes()).decode("ascii")


def optimize_character():
    """Resize and optimize the character PNG."""
    with Image.open(IMAGE) as img:
        img = img.convert("RGBA")
        img.thumbnail((900, 900), Image.Resampling.LANCZOS)
        img.save(OPTIMIZED_IMAGE, format="PNG", optimize=True)

    print("Character image optimized.")


def build_svg():
    """Embed image and fonts into the SVG template."""

    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Missing SVG: {TEMPLATE}")

    if not IMAGE.exists():
        raise FileNotFoundError(f"Missing image: {IMAGE}")

    # Optimize the character image
    optimize_character()

    # Read SVG template
    svg = TEMPLATE.read_text(encoding="utf-8")

    # Embed character image
    image_data = to_base64(OPTIMIZED_IMAGE)
    image_uri = f"data:image/png;base64,{image_data}"

    svg = svg.replace("__WAVING_IMAGE__", image_uri)

    # Embed fonts
    for placeholder, font_path in FONTS.items():
        if not font_path.exists():
            raise FileNotFoundError(f"Missing font: {font_path}")

        font_data = to_base64(font_path)
        svg = svg.replace(placeholder, font_data)

        print(f"Embedded: {font_path.name}")

    # Verify no placeholders remain
    if "__" in svg:
        raise ValueError("Unreplaced placeholders remain in SVG.")

    # Write final SVG
    OUTPUT.write_text(svg, encoding="utf-8")

    print("\nHero SVG generated successfully!")
    print(f"Output: {OUTPUT}")
    print(f"File size: {OUTPUT.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    build_svg()