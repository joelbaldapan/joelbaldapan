import base64
import math
from pathlib import Path

from game.config import (
    BOARD_FILE_PATH,
    BOARD_SIZE,
    SVG_BACKGROUND_COLOR,
    SVG_BORDER_RADIUS,
    SVG_FALLBACK_TILE_COLORS,
    SVG_FONT_FAMILY,
    SVG_FONT_FILE,
    SVG_FONT_SIZE,
    SVG_GAP,
    SVG_SCORE_HEIGHT,
    SVG_TEXT_COLOR_DARK,
    SVG_TEXT_COLOR_LIGHT,
    SVG_TILE_COLORS,
    SVG_TILE_SIZE,
)


class BoardRenderer:
    def render(self, board: list[list[int]], score: int) -> None:
        """Render the game board to the console."""
        border = BOARD_SIZE * 7
        print("\n" + "=" * border)
        print(f" SCORE: {score}")
        print("=" * border)

        for row in board:
            rendered_row = " | ".join(f"{num or '':^4}" for num in row)
            print(f"| {rendered_row} |")
            print("-" * border)

    def render_to_svg(self, board: list[list[int]], score: int) -> None:
        """Render the game board as an SVG file."""
        width = BOARD_SIZE * SVG_TILE_SIZE + (BOARD_SIZE + 1) * SVG_GAP
        height = BOARD_SIZE * SVG_TILE_SIZE + (BOARD_SIZE + 1) * SVG_GAP + SVG_SCORE_HEIGHT

        svg_elements = []

        # Open SVG tag
        svg_elements.append(
            f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        )

        # Font embedding via <defs> inside <svg>
        current_font_family = "Arial, sans-serif"  # Fallback
        if SVG_FONT_FILE:
            try:
                font_data = base64.b64encode(Path(SVG_FONT_FILE).read_bytes()).decode("utf-8")
                svg_elements.extend([
                    "<defs>",
                    (
                        '<style type="text/css">'
                        f'@font-face {{ font-family: "{SVG_FONT_FAMILY}"; '
                        f'src: url("data:font/ttf;base64,{font_data}") format("truetype"); }}'
                        "</style>"
                    ),
                    "</defs>",
                ])
                current_font_family = SVG_FONT_FAMILY
            except FileNotFoundError:
                print(f"Warning: Font file not found at {SVG_FONT_FILE}. Using default font.")

        # Background and Score text
        svg_elements.extend([
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="{SVG_BACKGROUND_COLOR}"/>',
            (
                f'<text x="{width / 2}" y="{SVG_SCORE_HEIGHT / 2 + SVG_FONT_SIZE / 3}" '
                f'font-family="{current_font_family}" font-size="{SVG_FONT_SIZE * 0.7}" fill="{SVG_TEXT_COLOR_LIGHT}" '
                f'text-anchor="middle">Score: {score}</text>'
            ),
        ])

        # Draw tiles
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x = c * SVG_TILE_SIZE + (c + 1) * SVG_GAP
                y = r * SVG_TILE_SIZE + (r + 1) * SVG_GAP + SVG_SCORE_HEIGHT
                tile_value = board[r][c]
                tile_color = SVG_TILE_COLORS.get(tile_value, SVG_FALLBACK_TILE_COLORS)
                text_color = SVG_TEXT_COLOR_DARK if tile_value in {2, 4} else SVG_TEXT_COLOR_LIGHT

                # Tile rectangle
                svg_elements.append(
                    f'<rect x="{x}" y="{y}" width="{SVG_TILE_SIZE}" height="{SVG_TILE_SIZE}" '
                    f'rx="{SVG_BORDER_RADIUS}" ry="{SVG_BORDER_RADIUS}" fill="{tile_color}"/>',
                )

                # Tile number
                if tile_value != 0:
                    n_exp = math.floor(math.log10(tile_value))
                    n_exp = max(2, n_exp)
                    reduction_factor = 0.8 - (n_exp - 2) * 0.1
                    reduction_factor = max(0.2, reduction_factor)

                    current_font_size = SVG_FONT_SIZE * reduction_factor

                    svg_elements.append(
                        f'<text x="{x + SVG_TILE_SIZE / 2}" '
                        f'y="{y + SVG_TILE_SIZE / 2 + current_font_size / 3}" '
                        f'font-family="{current_font_family}" font-size="{current_font_size}" '
                        f'fill="{text_color}" text-anchor="middle">{tile_value}</text>',
                    )

        svg_elements.append("</svg>")

        path = Path(BOARD_FILE_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(svg_elements))
        print(f"Board view exported to {BOARD_FILE_PATH}")
