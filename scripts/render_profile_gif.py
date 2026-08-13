#!/usr/bin/env python3
"""Render the small dark/light terminal animations used in the profile README."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SIZE = 260
STAGES = (
    ("UNDERSTAND", "find the real failure mode"),
    ("MODEL", "map constraints & trade-offs"),
    ("OBSERVE", "make behavior visible"),
    ("TEST", "challenge assumptions"),
    ("SHIP", "measure, learn, refine"),
)


THEMES = {
    "dark": {
        "page": "#0d1117",
        "panel": "#161b22",
        "border": "#30363d",
        "text": "#f0f6fc",
        "muted": "#8b949e",
        "accent": "#58a6ff",
        "active": "#3fb950",
        "cursor": "#d29922",
    },
    "light": {
        "page": "#ffffff",
        "panel": "#f6f8fa",
        "border": "#d0d7de",
        "text": "#1f2328",
        "muted": "#656d76",
        "accent": "#0969da",
        "active": "#1a7f37",
        "cursor": "#9a6700",
    },
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


FONT_10 = font(10)
FONT_11 = font(11)
FONT_14 = font(14, bold=True)
FONT_18 = font(18, bold=True)


def centered_x(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=face)
    return (SIZE - (box[2] - box[0])) // 2


def packet_position(stage: int, transition: float) -> tuple[float, float]:
    nodes = (46, 88, 130, 172, 214)
    if transition <= 0:
        return float(nodes[stage]), 181.0
    if stage < len(nodes) - 1:
        start, end = nodes[stage], nodes[stage + 1]
        return start + (end - start) * transition, 181.0
    x = nodes[-1] + (nodes[0] - nodes[-1]) * transition
    y = 181 + 36 * math.sin(math.pi * transition)
    return x, y


def render_frame(theme: dict[str, str], stage: int, tick: int) -> Image.Image:
    image = Image.new("RGB", (SIZE, SIZE), theme["page"])
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((12, 18, 248, 234), radius=15, fill=theme["panel"], outline=theme["border"], width=2)
    draw.line((13, 50, 247, 50), fill=theme["border"], width=1)
    for x, color in ((29, "#ff5f57"), (45, "#febc2e"), (61, "#28c840")):
        draw.ellipse((x - 4, 30, x + 4, 38), fill=color)
    draw.text((78, 27), "kutay@build:~", font=FONT_10, fill=theme["muted"])
    draw.text((215, 27), "KG", font=FONT_10, fill=theme["accent"])

    draw.text((28, 69), "$ engineering-loop", font=FONT_11, fill=theme["muted"])
    stage_number = f"0{stage + 1}"
    draw.text((28, 99), stage_number, font=FONT_14, fill=theme["accent"])
    draw.text((58, 96), STAGES[stage][0], font=FONT_18, fill=theme["text"])
    if (tick // 4) % 2 == 0:
        title_box = draw.textbbox((58, 96), STAGES[stage][0], font=FONT_18)
        cursor_x = title_box[2] + 4
        draw.rectangle((cursor_x, 100, cursor_x + 7, 116), fill=theme["cursor"])

    detail = STAGES[stage][1]
    draw.text((centered_x(draw, detail, FONT_11), 135), detail, font=FONT_11, fill=theme["muted"])

    nodes = (46, 88, 130, 172, 214)
    draw.line((nodes[0], 181, nodes[-1], 181), fill=theme["border"], width=2)
    for index, x in enumerate(nodes):
        color = theme["active"] if index == stage else theme["border"]
        radius = 6 if index == stage else 4
        draw.ellipse((x - radius, 181 - radius, x + radius, 181 + radius), fill=color)
        draw.text((x - 3, 194), str(index + 1), font=FONT_10, fill=theme["muted"])

    transition = max(0.0, (tick - 10) / 3)
    packet_x, packet_y = packet_position(stage, min(transition, 1.0))
    draw.ellipse((packet_x - 3, packet_y - 3, packet_x + 3, packet_y + 3), fill=theme["accent"])

    draw.text((28, 218), "evidence in", font=FONT_10, fill=theme["muted"])
    draw.text((164, 218), "confidence out", font=FONT_10, fill=theme["active"])
    draw.line((102, 224, 154, 224), fill=theme["border"], width=1)
    draw.polygon(((154, 221), (160, 224), (154, 227)), fill=theme["border"])
    return image


def render(theme_name: str) -> None:
    theme = THEMES[theme_name]
    frames = [
        render_frame(theme, stage, tick)
        for stage in range(len(STAGES))
        for tick in range(14)
    ]
    output = ASSETS / f"engineering-loop-{theme_name}.gif"
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for theme_name in THEMES:
        render(theme_name)


if __name__ == "__main__":
    main()
