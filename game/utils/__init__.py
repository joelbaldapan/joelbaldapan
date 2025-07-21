"""Archive a file by moving it to a history directory with a timestamp.

Args:
    file_path (str): Path to the file to be archived.
    history_path (str): Path to the directory where the archived file will be stored.
    tz (tzinfo, optional): Timezone for the timestamp. Defaults to UTC.

Raises:
    FileNotFoundError: If the file specified by `file_path` does not exist.

Notes:
    - The history directory will be created if it does not exist.
    - The archived file will be renamed to include a timestamp in the format 'YYYYMMDD_HHMMSS'.

"""
