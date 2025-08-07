from pathlib import Path
from unittest.mock import MagicMock

import pytest

from kratio.exceptions import FileReadError
from kratio.io.file_handler import _read_text, read_text_file


def test_read_text_file_success(tmp_path):
    """
    Tests that read_text_file successfully reads content from an existing file.
    """
    file_content = "This is a test file content."
    test_file = tmp_path / "test_success.txt"
    test_file.write_text(file_content, encoding="utf-8")

    result = read_text_file(test_file)
    assert result == file_content


def test_read_text_file_not_found():
    """
    Tests that read_text_file handles FileNotFoundError correctly by raising FileReadError.
    """
    non_existent_file = Path("non_existent_file.txt")
    with pytest.raises(FileReadError) as excinfo:
        read_text_file(non_existent_file)
    assert "File not found at" in str(excinfo.value)


def test_read_text_file_other_exception(monkeypatch):
    """
    Tests that read_text_file handles other exceptions during file reading by raising FileReadError.
    """
    mock_file_path = Path("mock_file.txt")

    # Create a MagicMock instance that will raise an OSError when called
    mock_open = MagicMock(side_effect=OSError("Permission denied"))

    # Use monkeypatch to replace Path.open with our mock_open object
    monkeypatch.setattr(Path, "open", mock_open)

    with pytest.raises(FileReadError) as excinfo:
        read_text_file(mock_file_path)
    assert "An error occurred while reading the file: Permission denied" in str(excinfo.value)
    mock_open.assert_called_once()


def test_read_text_pure_raises_file_not_found():
    """
    Tests that _read_text raises FileReadError for a non-existent file.
    """
    non_existent_file = Path("non_existent_file.txt")
    with pytest.raises(FileReadError) as excinfo:
        _read_text(non_existent_file)
    assert "File not found" in str(excinfo.value)


def test_read_text_pure_raises_other_exception(monkeypatch):
    """
    Tests that _read_text raises FileReadError for other exceptions during file reading.
    """
    mock_file_path = Path("mock_file.txt")

    # Create a MagicMock instance that will raise an OSError when called
    mock_open = MagicMock(side_effect=OSError("Permission denied"))

    # Use monkeypatch to replace Path.open with our mock_open object
    monkeypatch.setattr(Path, "open", mock_open)

    with pytest.raises(FileReadError) as excinfo:
        _read_text(mock_file_path)
    assert "An error occurred while reading the file: Permission denied" in str(excinfo.value)
    mock_open.assert_called_once()
