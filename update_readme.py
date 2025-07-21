import json
from pathlib import Path

from game.config import GAME_FILE_PATH, USER_STATS_PATH

# TAGS
CUSTOM_START_TAG_RECENT_MOVES = "<!--START_RECENT_MOVES_TABLE-->"
CUSTOM_END_TAG_RECENT_MOVES = "<!--END_RECENT_MOVES_TABLE-->"

CUSTOM_START_TAG_TOP_SCORERS = "<!--START_TOP_SCORERS_TABLE-->"
CUSTOM_END_TAG_TOP_SCORERS = "<!--END_TOP_SCORERS_TABLE-->"


# Paths to data files
user_stats_path = Path(USER_STATS_PATH)
game_file_path = Path(GAME_FILE_PATH)


def generate_recent_moves_table() -> str:
    """Generate the markdown table for recent moves.

    Returns:
        str: The markdown table output.

    """
    table_header = "| Username | Score Earned |\n|---|---|\n"
    table_rows = []

    try:
        with game_file_path.open("r") as f:
            game_data = json.load(f)
        history = game_data.get("history", [])

        # Get the last few moves, e.g., last 5
        recent_moves = history[-5:]  # Adjust number of recent moves as desired

        for move in reversed(recent_moves):  # Show most recent first
            username = move.get("username", "N/A")
            score = move.get("score", 0)
            username_link = f"[@{username}](https://github.com/{username})"
            table_rows.append(f"| {username_link} | +{score} |")
    except (FileNotFoundError, json.JSONDecodeError):
        table_rows.append("| No recent moves yet. | - |")

    return table_header + "\n".join(table_rows)


def generate_top_scorers_table() -> str:
    """Generate the markdown table for top 5 highest scorers.

    Returns:
        str: The markdown table output.

    """
    table_header = "| Rank | Username | Total Score |\n|---|---|---|\n"
    table_rows = []

    try:
        with user_stats_path.open("r") as f:
            user_stats = json.load(f)

        # Sort users by total_score in descending order
        sorted_users = sorted(user_stats.items(), key=lambda item: item[1].get("total_score", 0), reverse=True)

        # Get top 5
        top_5 = sorted_users[:5]

        for i, (username, stats) in enumerate(top_5):
            total_score = stats.get("total_score", 0)
            username_link = f"[@{username}](https://github.com/{username})"
            table_rows.append(f"| {i + 1} | {username_link} | {total_score} |")

    except (FileNotFoundError, json.JSONDecodeError):
        table_rows.append("| No top scorers yet. | - | - |")

    return table_header + "\n".join(table_rows)


def update_readme(readme_path: str = "README.md") -> None:
    """Update the README.md file with the generated tables."""
    readme_content = Path(readme_path).read_text()

    # Update Recent Moves Table
    recent_moves_table = generate_recent_moves_table()

    start_tag_recent = CUSTOM_START_TAG_RECENT_MOVES
    end_tag_recent = CUSTOM_END_TAG_RECENT_MOVES
    if start_tag_recent in readme_content and end_tag_recent in readme_content:
        # Split and reassemble content around the tags
        parts = readme_content.split(start_tag_recent)
        before_tag = parts[0]
        after_tag = (
            parts[1].split(end_tag_recent)[1] if len(parts) > 1 else ""
        )  # Handle case where end tag might not be found after start

        readme_content = before_tag + start_tag_recent + "\n" + recent_moves_table + "\n" + end_tag_recent + after_tag

    # Update Top Scorers Table
    top_scorers_table = generate_top_scorers_table()

    start_tag_top = CUSTOM_START_TAG_TOP_SCORERS
    end_tag_top = CUSTOM_END_TAG_TOP_SCORERS
    if start_tag_top in readme_content and end_tag_top in readme_content:
        # Split and reassemble content around the tags
        parts = readme_content.split(start_tag_top)
        before_tag = parts[0]
        after_tag = parts[1].split(end_tag_top)[1] if len(parts) > 1 else ""

        readme_content = before_tag + start_tag_top + "\n" + top_scorers_table + "\n" + end_tag_top + after_tag

    Path(readme_path).write_text(readme_content)
    print("README.md updated successfully.")


if __name__ == "__main__":
    update_readme()
