from pathlib import Path

from kratio.exceptions import FileReadError


def is_directory(path: str) -> bool:
    """
    Checks if a given path is a directory.
    """
    return Path(path).is_dir()


def get_files_from_directory(directory_path: str, supported_extensions: list[str]) -> list[Path]:
    """
    Scans a directory and returns a list of files with supported extensions.
    """
    return [p for p in Path(directory_path).rglob("*") if p.is_file() and p.suffix in supported_extensions]


def _read_text(file_path: Path | str) -> str:
    """
    Reads a text file and returns its content as a string.
    Raises FileReadError on failure.
    """
    if is_directory(str(file_path)):
        raise FileReadError(f"Path '{file_path}' is a directory, not a file.")

    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        with file_path.open(encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileReadError(f"File not found at {file_path}") from e
    except Exception as e:
        raise FileReadError(f"An error occurred while reading the file: {e}") from e


def read_text_file(file_path: Path | str) -> str:
    """
    Reads a text file and returns its content as a string.

    Args:
        file_path (Path | str): The path to the text file.

    Returns:
        str: The content of the text file.
    """
    return _read_text(file_path)
