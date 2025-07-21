BOARD_SIZE: int = 4

# Game State
GAME_FILE_PATH: str = "data/state/game.json"
ARCHIVE_GAME_HISTORY_PATH: str = "data/state/history"

# Board Images
BOARD_FILE_PATH: str = "data/board/board.svg"
ARCHIVE_BOARD_HISTORY_PATH: str = "data/board/history"

# Stats Paths
USER_STATS_PATH: str = "data/stats/users.json"
GLOBAL_STATS_FILE_PATH: str = "data/stats/global_stats.json"

# SVG Rendering Constants
SVG_TILE_SIZE = 100
SVG_BORDER_RADIUS = 8
SVG_GAP = 10
SVG_SCORE_HEIGHT = 60

# FONT
SVG_FONT_SIZE = 42
SVG_FONT_FILE = "assets/fonts/MartianMono-Bold.ttf"
SVG_FONT_FAMILY = "Martian Mono"

# VANILLA COLORS
SVG_BACKGROUND_COLOR = "#a6a6a6"
SVG_EMPTY_TILE_COLOR = "#c9c9c9"
SVG_TEXT_COLOR_LIGHT = "#fefbf7"
SVG_TEXT_COLOR_DARK = "#383834"
SVG_TILE_COLORS = {
    0: SVG_EMPTY_TILE_COLOR,
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf73",
    256: "#edcc62",
    512: "#edc850",
    1024: "#eec745",
    2048: "#eec434",
}
SVG_FALLBACK_TILE_COLORS = "#3c3a32"


# BLUE COLORS
SVG_BACKGROUND_COLOR = "#0F3743"
SVG_EMPTY_TILE_COLOR = "#275e71"
SVG_TEXT_COLOR_LIGHT = "#f9f6f2"
SVG_TEXT_COLOR_DARK = "#1B1B19"
SVG_TILE_COLORS = {
    0: SVG_EMPTY_TILE_COLOR,
    2: "#b2dbdd",
    4: "#afdcde",
    8: "#5ac4c2",
    16: "#00adb1",
    32: "#008a96",
    64: "#00747e",
    128: "#0073a1",
    256: "#0072bc",
    512: "#0083cd",
    1024: "#2d5e9f",
    2048: "#2c5597",
    4096: "#264678",
    8192: "#233E6B",
    16384: "#132139",
    32768: "#0D1728",
}
SVG_FALLBACK_TILE_COLORS = "#08101D"
