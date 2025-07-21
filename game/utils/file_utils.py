from datetime import UTC, datetime, tzinfo
from pathlib import Path

from game.models.global_stats import GlobalStats


def archive_file(
    file_path: str,
    history_path: str,
    tz: tzinfo = UTC,
) -> None:
    """Archive a file by moving it to a history directory with a timestamp.

    Create the history directory if it doesn't exist.
    """
    file = Path(file_path)
    history_dir = Path(history_path)

    if file.exists():
        history_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(tz=tz).strftime("%Y%m%d_%H%M%S")

        name = file.stem
        ext = file.suffix
        new_file_name = f"{name}_{timestamp}{ext}"
        new_file_path = history_dir / new_file_name
        file.rename(new_file_path)


def update_board_svg_file(svg_content: str, base_board_path: str) -> None:
    """Manage the saving and rotation of board SVG files.

    It reads the current board number, increments it, deletes the old file,
    and saves the new SVG content to the new numbered file.
    """
    board_dir = Path(base_board_path).parent
    board_base_name = "board"  # Assuming the files are named board0.svg, board1.svg, etc.

    # Get the previous and new board numbers
    old_board_number = GlobalStats.get_current_board_number()
    new_board_number = GlobalStats.increment_board_number()

    # Construct old and new file paths
    old_file_path = board_dir / f"{board_base_name}{old_board_number}.svg"
    new_file_path = board_dir / f"{board_base_name}{new_board_number}.svg"

    # Ensure directory exists
    board_dir.mkdir(parents=True, exist_ok=True)

    # Delete the old file if it exists
    if old_file_path.exists():
        old_file_path.unlink()
        print(f"Deleted old board file: {old_file_path}")

    # Write the new SVG content
    new_file_path.write_text(svg_content)
    print(f"Board view exported to {new_file_path}")
