"""game.views.

This module provides rendering functionality for the 2048 game board, including console and SVG output.

Classes:
    BoardRenderer:
        Renders the game board and score to the console or exports it as an SVG file.

Attributes:
    BOARD_FILE_PATH (str): Path to save the SVG board file.
    BOARD_SIZE (int): Size of the game board (number of rows/columns).
    SVG_BACKGROUND_COLOR (str): Background color for the SVG board.
    SVG_BORDER_RADIUS (int): Border radius for SVG tiles.
    SVG_FALLBACK_TILE_COLORS (str): Default color for tiles not in SVG_TILE_COLORS.
    SVG_FONT_FAMILY (str): Font family for SVG text.
    SVG_FONT_FILE (str): Path to the font file for SVG embedding.
    SVG_FONT_SIZE (int): Base font size for SVG text.
    SVG_GAP (int): Gap between tiles in SVG.
    SVG_SCORE_HEIGHT (int): Height reserved for score display in SVG.
    SVG_TEXT_COLOR_DARK (str): Text color for low-value tiles.
    SVG_TEXT_COLOR_LIGHT (str): Text color for high-value tiles.
    SVG_TILE_COLORS (dict): Mapping of tile values to colors.
    SVG_TILE_SIZE (int): Size of each tile in SVG.

Example:
    renderer = BoardRenderer()
    renderer.render(board, score)
    renderer.render_to_svg(board, score)

"""
