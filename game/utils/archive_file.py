from datetime import UTC, datetime, tzinfo
from pathlib import Path


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
