from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from rpi_flashcards.display.base import PreparedCardFrame


def render_frame_to_png(frame: PreparedCardFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("L", (frame.width, frame.height), color=255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    y = 8
    draw.rectangle((0, 0, frame.width - 1, frame.height - 1), outline=0, width=1)
    draw.text((10, y), frame.title, font=font, fill=0)
    y += 16
    draw.text((10, y), frame.subtitle, font=font, fill=0)
    y += 14

    for line in frame.body_lines:
        draw.text((10, y), line, font=font, fill=0)
        y += 12
        if y > frame.height - 20:
            break

    draw.text((10, frame.height - 14), frame.footer, font=font, fill=0)
    image.convert("1").save(output_path)

