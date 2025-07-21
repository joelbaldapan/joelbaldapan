from typing import Literal

from game.config import (
    ARCHIVE_BOARD_HISTORY_PATH,
    ARCHIVE_GAME_HISTORY_PATH,
    BOARD_FILE_PATH,
    BOARD_SIZE,
    GAME_FILE_PATH,
)
from game.models.game_board import GameBoard
from game.models.global_stats import GlobalStats
from game.models.user_stats import UserStats
from game.utils.file_utils import archive_file
from game.views.view import BoardRenderer

VALID_DIRECTIONS = ("up", "down", "left", "right")
Direction = Literal["up", "down", "left", "right"]


class GameController:
    def __init__(self, username: str = "joelbaldapan", move: str | None = None) -> None:
        self.username = username
        self.renderer = BoardRenderer()
        self.board = GameBoard.load(GAME_FILE_PATH)
        if move in VALID_DIRECTIONS:
            self.move: Direction = move

    def reset(self) -> None:
        """Reset the board: backs up the current file, creates a new board, and saves it."""
        # Archive current board if it exists
        if self.board:
            self._archive()

        board = GameBoard()
        board.add_random_tile()
        board.add_random_tile()
        board.save(GAME_FILE_PATH, username=self.username)

        self.board = board  # Update the controller's board instance
        self.renderer.render_to_svg(self.board.board, self.board.total_score)
        print(f"New board saved to {GAME_FILE_PATH} (size: {BOARD_SIZE}x{BOARD_SIZE})")

    def run(self) -> None:
        moved = self.board.move(self.move)

        if moved:
            self.board.add_random_tile()
            self.board.save(GAME_FILE_PATH, username=self.username)

            # Update global stats
            GlobalStats.update_on_move(self.board.total_score, self.board.board, self.username)

            # Update user stats
            if self.username:
                UserStats.update(self.username, self.board.score)
        else:
            print(f"\nInvalid move ({self.move}). Board didn't change.")

        self.renderer.render(self.board.board, self.board.total_score)
        self.renderer.render_to_svg(self.board.board, self.board.total_score)

        if self.board.is_game_over():
            self.end()

    def end(self) -> None:
        print("\nGame Over! Final score:", self.board.total_score)

        # Update global stats that change only on game end
        GlobalStats.update_on_game_end()
        print("Global stats updated.")

        # Reset the board for a new game and render it
        self.reset()
        print("New game started.")

    # Private methods below
    def _archive(self) -> None:
        # Archive game state
        archive_file(GAME_FILE_PATH, ARCHIVE_GAME_HISTORY_PATH)
        print(f"Final game state archived to {ARCHIVE_GAME_HISTORY_PATH}")

        # Archive board
        archive_file(BOARD_FILE_PATH, ARCHIVE_BOARD_HISTORY_PATH)
        print(f"Final board image archived to {ARCHIVE_BOARD_HISTORY_PATH}")
