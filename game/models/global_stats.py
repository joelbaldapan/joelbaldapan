import json
from pathlib import Path

from game.config import BOARD_SIZE, GLOBAL_STATS_FILE_PATH


class GlobalStats:
    @staticmethod
    def update_on_move(current_game_total_score: int, current_board_state: list[list[int]], username: str) -> None:
        stats = GlobalStats._load_stats()

        # Increment total_moves
        stats["total_moves"] += 1

        # Update high_score
        stats["high_score"] = max(stats["high_score"], current_game_total_score)

        # Calculate and update largest_tile
        current_largest_tile = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                current_largest_tile = max(current_largest_tile, current_board_state[r][c])

        stats["largest_tile"] = max(stats["largest_tile"], current_largest_tile)

        # Update unique_users
        if username not in stats["known_users"]:
            stats["known_users"].append(username)
            stats["unique_users"] = len(stats["known_users"])

        GlobalStats._save_stats(stats)

    @staticmethod
    def update_on_game_end() -> None:
        stats = GlobalStats._load_stats()
        stats["games_finished"] += 1
        GlobalStats._save_stats(stats)

    # Private methods below

    @staticmethod
    def _load_stats() -> dict:
        """Load global stats from file.

        Returns:
            dict: The stats. Gives default if file doesn't exist or is corrupted.

        """
        stats_path = Path(GLOBAL_STATS_FILE_PATH)
        default_stats = {
            "high_score": 0,
            "games_finished": 0,
            "largest_tile": 0,
            "total_moves": 0,
            "unique_users": 0,
            "known_users": [],
        }

        stats_path.parent.mkdir(parents=True, exist_ok=True)

        if stats_path.exists():
            with stats_path.open("r") as file:
                try:
                    loaded_stats = json.load(file)
                    default_stats.update(loaded_stats)  # Update with existing data
                except json.JSONDecodeError:
                    print(f"Warning: {GLOBAL_STATS_FILE_PATH} is empty or corrupted. Initializing with default stats.")
                    # default_stats already has default values
        return default_stats

    @staticmethod
    def _save_stats(stats: dict) -> None:
        """Save global stats to file."""
        stats_path = Path(GLOBAL_STATS_FILE_PATH)
        with stats_path.open("w") as file:
            json.dump(stats, file, indent=2)
