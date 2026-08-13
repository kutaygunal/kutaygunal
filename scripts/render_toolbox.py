#!/usr/bin/env python3
"""Render the theme-aware toolbox terminal used in the profile README."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH = 960
HEIGHT = 292
SCALE = 2

THEMES = {
    "dark": {
        "page": "#0d1117",
        "panel": "#0b0f14",
        "chrome": "#161b22",
        "border": "#30363d",
        "text": "#c9d1d9",
        "muted": "#8b949e",
        "blue": "#58a6ff",
        "green": "#3fb950",
    },
    "light": {
        "page": "#ffffff",
        "panel": "#f6f8fa",
        "chrome": "#eaeef2",
        "border": "#d0d7de",
        "text": "#24292f",
        "muted": "#656d76",
        "blue": "#0969da",
        "green": "#1a7f37",
    },
}

ROWS = (
    ("build", "--systems", "Rust  ·  C++17/20  ·  C  ·  CUDA"),
    ("train", "--local", "Python  ·  PyTorch  ·  computer vision  ·  local LLMs"),
    ("ship", "--native", "Qt  ·  SwiftUI  ·  C#/.NET  ·  FastAPI"),
    ("verify", "--hard", "CI/CD  ·  fuzzing  ·  differential testing  ·  benchmarks"),
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf"),
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        ),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size * SCALE)
    return ImageFont.load_default()


FONT_SMALL = font(12)
FONT_BODY = font(15)
FONT_BODY_BOLD = font(15, bold=True)


def pt(value: int) -> int:
    return value * SCALE


def render(theme_name: str) -> None:
    theme = THEMES[theme_name]
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), theme["page"])
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (pt(1), pt(1), pt(WIDTH - 2), pt(HEIGHT - 2)),
        radius=pt(10),
        fill=theme["panel"],
        outline=theme["border"],
        width=pt(1),
    )
    draw.rounded_rectangle(
        (pt(2), pt(2), pt(WIDTH - 3), pt(47)),
        radius=pt(9),
        fill=theme["chrome"],
    )
    draw.rectangle((pt(2), pt(38), pt(WIDTH - 3), pt(47)), fill=theme["chrome"])
    draw.line((pt(2), pt(47), pt(WIDTH - 3), pt(47)), fill=theme["border"], width=pt(1))

    for x, color in ((22, "#ff5f57"), (40, "#febc2e"), (58, "#28c840")):
        draw.ellipse((pt(x - 5), pt(19), pt(x + 5), pt(29)), fill=color)
    draw.text((pt(82), pt(15)), "kutay@build:~/toolbox", font=FONT_SMALL, fill=theme["muted"])
    draw.text((pt(886), pt(15)), "KG", font=FONT_SMALL, fill=theme["blue"])

    y = 72
    for command, flag, output in ROWS:
        draw.text((pt(28), pt(y)), "$", font=FONT_BODY_BOLD, fill=theme["green"])
        draw.text((pt(50), pt(y)), command, font=FONT_BODY_BOLD, fill=theme["blue"])
        command_width = draw.textlength(command, font=FONT_BODY_BOLD) / SCALE
        draw.text((pt(int(58 + command_width)), pt(y)), flag, font=FONT_BODY, fill=theme["muted"])
        draw.text((pt(285), pt(y)), output, font=FONT_BODY, fill=theme["text"])
        y += 41

    draw.line((pt(28), pt(237), pt(930), pt(237)), fill=theme["border"], width=pt(1))
    draw.text((pt(28), pt(253)), "deploy targets", font=FONT_SMALL, fill=theme["muted"])
    draw.text(
        (pt(165), pt(253)),
        "devtools / aerospace / silicon / healthcare",
        font=FONT_SMALL,
        fill=theme["text"],
    )
    draw.text((pt(897), pt(253)), "OK", font=FONT_SMALL, fill=theme["green"])

    output = ASSETS / f"toolbox-terminal-{theme_name}.png"
    image.save(output, optimize=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for theme_name in THEMES:
        render(theme_name)


if __name__ == "__main__":
    main()
