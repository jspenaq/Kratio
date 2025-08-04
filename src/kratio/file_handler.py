from pathlib import Path


def read_text_file(file_path: Path | str) -> str | None:
    """
    Reads a text file and returns its content as a string.

    Args:
        file_path (Path | str): The path to the text file.

    Returns:
        str: The content of the text file.
    """
    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        with file_path.open(encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error: An error occurred while reading the file: {e}")
        return None
