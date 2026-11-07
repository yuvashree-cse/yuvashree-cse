from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = ROOT / "connect.svg"
OUTPUT = ROOT / "connect-ready.svg"

FONTS = {
    "__SPACE_REGULAR__": ROOT / "assets/fonts/SpaceGrotesk-Regular.woff2",
    "__SPACE_BOLD__": ROOT / "assets/fonts/SpaceGrotesk-Bold.woff2",
    "__MONO_REGULAR__": ROOT / "assets/fonts/JetBrainsMono-Regular.woff2",
}

def encode_file(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build():
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Missing template: {TEMPLATE}")

    svg = TEMPLATE.read_text(encoding="utf-8")

    for placeholder, font_path in FONTS.items():
        if not font_path.exists():
            raise FileNotFoundError(f"Missing font: {font_path}")

        svg = svg.replace(placeholder, encode_file(font_path))
        print(f"Embedded: {font_path.name}")

    remaining = [
        placeholder for placeholder in FONTS
        if placeholder in svg
    ]

    if remaining:
        raise ValueError(f"Unreplaced placeholders: {remaining}")

    OUTPUT.write_text(svg, encoding="utf-8")

    print("\nContact SVG generated successfully!")
    print(f"Output: {OUTPUT}")
    print(f"File size: {OUTPUT.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    build()