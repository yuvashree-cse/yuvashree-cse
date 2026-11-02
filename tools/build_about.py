from pathlib import Path
import base64
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = ROOT / "about-life.svg"
OUTPUT = ROOT / "about-life-ready.svg"

IMAGE = ROOT / "assets/images/pointing.png"
OPTIMIZED_IMAGE = ROOT / "assets/images/pointing-about.png"

FONTS = {
    "__SPACE_REGULAR__": ROOT / "assets/fonts/SpaceGrotesk-Regular.woff2",
    "__SPACE_BOLD__": ROOT / "assets/fonts/SpaceGrotesk-Bold.woff2",
    "__MONO_REGULAR__": ROOT / "assets/fonts/JetBrainsMono-Regular.woff2",
}


def encode_file(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def optimize_image():
    with Image.open(IMAGE) as img:
        img = img.convert("RGBA")
        img.thumbnail((900, 900), Image.Resampling.LANCZOS)
        img.save(OPTIMIZED_IMAGE, "PNG", optimize=True)


def build():
    for path in [TEMPLATE, IMAGE, *FONTS.values()]:
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")

    optimize_image()

    svg = TEMPLATE.read_text(encoding="utf-8")

    image_data = encode_file(OPTIMIZED_IMAGE)
    image_uri = f"data:image/png;base64,{image_data}"

    svg = svg.replace("__POINTING_IMAGE__", image_uri)

    for placeholder, font_path in FONTS.items():
        svg = svg.replace(placeholder, encode_file(font_path))
        print(f"Embedded {font_path.name}")

    if "__" in svg:
        raise ValueError("A placeholder was not replaced.")

    OUTPUT.write_text(svg, encoding="utf-8")

    print("\nAbout section generated!")
    print(f"Output: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    build()