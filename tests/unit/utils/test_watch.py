"""
Unit tests for the watch module.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from kratio.utils.watch import FileWatcher, KratioEventHandler


def test_kratio_event_handler_init():
    """Test initialization of KratioEventHandler."""
    # Arrange
    callback = MagicMock()
    supported_extensions = [".txt", ".md"]
    target_path = Path("test.txt")

    # Act
    handler = KratioEventHandler(callback, supported_extensions, target_path)

    # Assert
    assert handler.callback == callback
    assert handler.supported_extensions == supported_extensions
    assert handler.target_path == target_path
    assert handler.last_processed_time == 0
    assert handler.debounce_seconds > 0


def test_kratio_event_handler_on_modified_directory_event():
    """Test that directory modification events are ignored."""
    # Arrange
    callback = MagicMock()
    handler = KratioEventHandler(callback)
    event = MagicMock()
    event.is_directory = True

    # Act
    handler.on_modified(event)

    # Assert
    callback.assert_not_called()


def test_kratio_event_handler_on_modified_debounce():
    """Test debouncing of rapid events."""
    # Arrange
    callback = MagicMock()
    handler = KratioEventHandler(callback)
    handler.debounce_seconds = 1.0  # Set a longer debounce for testing

    event = MagicMock()
    event.is_directory = False
    event.src_path = "test.txt"

    # Act - Call twice in rapid succession
    handler.on_modified(event)
    first_time = handler.last_processed_time
    handler.on_modified(event)

    # Assert - Second call should be debounced
    assert callback.call_count == 1
    assert handler.last_processed_time == first_time


def test_kratio_event_handler_on_modified_target_file():
    """Test that only target file events are processed when target is specified."""
    # Arrange
    callback = MagicMock()
    target_path = Path("target.txt")
    handler = KratioEventHandler(callback, target_path=target_path)

    # Event for target file
    target_event = MagicMock()
    target_event.is_directory = False
    target_event.src_path = str(target_path)

    # Event for non-target file
    other_event = MagicMock()
    other_event.is_directory = False
    other_event.src_path = "other.txt"

    # Act
    handler.on_modified(target_event)
    handler.on_modified(other_event)

    # Assert - Only target file should trigger callback
    assert callback.call_count == 1
    callback.assert_called_with(target_path)


def test_kratio_event_handler_on_modified_file_extension():
    """Test that only files with supported extensions are processed."""
    # Arrange
    callback = MagicMock()
    supported_extensions = [".txt"]
    handler = KratioEventHandler(callback, supported_extensions)

    # Event for supported file
    supported_event = MagicMock()
    supported_event.is_directory = False
    supported_event.src_path = "test.txt"

    # Event for unsupported file
    unsupported_event = MagicMock()
    unsupported_event.is_directory = False
    unsupported_event.src_path = "test.pdf"

    # Act
    handler.on_modified(supported_event)
    handler.on_modified(unsupported_event)

    # Assert - Only supported file should trigger callback
    assert callback.call_count == 1
    callback.assert_called_with(Path("test.txt"))


def test_file_watcher_init():
    """Test initialization of FileWatcher."""
    # Act
    watcher = FileWatcher()

    # Assert
    assert watcher.observer is None
    assert watcher.handler is None
    assert watcher.watching is False


@patch("kratio.utils.watch.Observer")
def test_file_watcher_start_watching_file(mock_observer_class):
    """Test starting to watch a file."""
    # Arrange
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer

    callback = MagicMock()

    with patch("kratio.utils.watch.is_directory", return_value=False), patch("pathlib.Path.exists", return_value=True):
        # Act
        watcher = FileWatcher()
        watcher.start_watching("test.txt", callback)

        # Assert
        assert watcher.watching is True
        assert watcher.observer == mock_observer
        assert isinstance(watcher.handler, KratioEventHandler)
        mock_observer.schedule.assert_called_once()
        mock_observer.start.assert_called_once()


@patch("kratio.utils.watch.Observer")
def test_file_watcher_start_watching_directory(mock_observer_class):
    """Test starting to watch a directory."""
    # Arrange
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer

    callback = MagicMock()

    with patch("kratio.utils.watch.is_directory", return_value=True), patch("pathlib.Path.exists", return_value=True):
        # Act
        watcher = FileWatcher()
        watcher.start_watching("test_dir", callback)

        # Assert
        assert watcher.watching is True
        assert watcher.observer == mock_observer
        assert isinstance(watcher.handler, KratioEventHandler)
        mock_observer.schedule.assert_called_once()
        # Check that recursive=True was passed for directory watching
        _, kwargs = mock_observer.schedule.call_args
        assert kwargs.get("recursive") is True
        mock_observer.start.assert_called_once()


@patch("kratio.utils.watch.Observer")
def test_file_watcher_start_watching_nonexistent_path(mock_observer_class):
    """Test that watching a nonexistent path raises FileNotFoundError."""
    # Arrange
    callback = MagicMock()

    with patch("pathlib.Path.exists", return_value=False):
        # Act & Assert
        watcher = FileWatcher()
        with pytest.raises(FileNotFoundError):
            watcher.start_watching("nonexistent", callback)

        # Observer should not be created
        mock_observer_class.assert_not_called()


@patch("kratio.utils.watch.Observer")
def test_file_watcher_stop_watching(mock_observer_class):
    """Test stopping the file watcher."""
    # Arrange
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer

    callback = MagicMock()

    with patch("kratio.utils.watch.is_directory", return_value=True), patch("pathlib.Path.exists", return_value=True):
        # Act
        watcher = FileWatcher()
        watcher.start_watching("test_dir", callback)
        watcher.stop_watching()

        # Assert
        assert watcher.watching is False
        mock_observer.stop.assert_called_once()
        mock_observer.join.assert_called_once()


@patch("kratio.utils.watch.Observer")
def test_file_watcher_cleanup_on_del(mock_observer_class):
    """Test that resources are cleaned up when the watcher is deleted."""
    # Arrange
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer

    callback = MagicMock()

    with patch("kratio.utils.watch.is_directory", return_value=True), patch("pathlib.Path.exists", return_value=True):
        # Act
        watcher = FileWatcher()
        watcher.start_watching("test_dir", callback)
        # Simulate deletion
        watcher.__del__()

        # Assert
        mock_observer.stop.assert_called_once()
        mock_observer.join.assert_called_once()
