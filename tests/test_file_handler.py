from pathlib import Path
from unittest.mock import MagicMock

from src.kratio.file_handler import read_text_file


def test_read_text_file_success(tmp_path):
    """
    Tests that read_text_file successfully reads content from an existing file.
    """
    file_content = "This is a test file content."
    test_file = tmp_path / "test_success.txt"
    test_file.write_text(file_content, encoding="utf-8")

    result = read_text_file(test_file)
    assert result == file_content


def test_read_text_file_not_found(capsys):
    """
    Tests that read_text_file handles FileNotFoundError correctly.
    """
    non_existent_file = Path("non_existent_file.txt")
    result = read_text_file(non_existent_file)

    assert result is None
    captured = capsys.readouterr()
    assert f"Error: File not found at {non_existent_file}" in captured.out


def test_read_text_file_other_exception(monkeypatch, capsys):
    """
    Tests that read_text_file handles other exceptions during file reading using MagicMock.
    """
    mock_file_path = Path("mock_file.txt")

    # Create a MagicMock instance that will raise an OSError when called
    mock_open = MagicMock(side_effect=OSError("Permission denied"))

    # Use monkeypatch to replace Path.open with our mock_open object
    monkeypatch.setattr(Path, "open", mock_open)

    result = read_text_file(mock_file_path)

    assert result is None
    captured = capsys.readouterr()
    assert "Error: An error occurred while reading the file: Permission denied" in captured.out

    # Optionally, verify that Path.open was called with the correct arguments
    mock_open.assert_called_once_with(mock_file_path, encoding="utf-8")
