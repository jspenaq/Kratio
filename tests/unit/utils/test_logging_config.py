import sys
from unittest.mock import patch

from kratio.utils.logging_config import setup_logging


@patch("kratio.utils.logging_config.logger")
def test_setup_logging_default_parameters(mock_logger):
    """Test setup_logging with default parameters."""
    # Call the function with default parameters
    setup_logging()

    # Verify logger.remove was called
    mock_logger.remove.assert_called_once()

    # Verify stderr handler was added with INFO level
    mock_logger.add.assert_any_call(sys.stderr, level="INFO")

    # Verify file handler was added with rotation and INFO level
    mock_logger.add.assert_any_call("logs/kratio.log", rotation="5 MB", level="INFO")

    # Verify add was called exactly twice (stderr and file)
    assert mock_logger.add.call_count == 2


@patch("kratio.utils.logging_config.logger")
def test_setup_logging_custom_level(mock_logger):
    """Test setup_logging with custom log level."""
    # Call the function with custom log level
    setup_logging(level="DEBUG")

    # Verify logger.remove was called
    mock_logger.remove.assert_called_once()

    # Verify stderr handler was added with DEBUG level
    mock_logger.add.assert_any_call(sys.stderr, level="DEBUG")

    # Verify file handler was added with rotation and DEBUG level
    mock_logger.add.assert_any_call("logs/kratio.log", rotation="5 MB", level="DEBUG")

    # Verify add was called exactly twice (stderr and file)
    assert mock_logger.add.call_count == 2


@patch("kratio.utils.logging_config.logger")
def test_setup_logging_custom_file_path(mock_logger):
    """Test setup_logging with custom log file path."""
    # Call the function with custom log file path
    custom_path = "logs/custom.log"
    setup_logging(log_file_path=custom_path)

    # Verify logger.remove was called
    mock_logger.remove.assert_called_once()

    # Verify stderr handler was added with INFO level
    mock_logger.add.assert_any_call(sys.stderr, level="INFO")

    # Verify file handler was added with custom path, rotation and INFO level
    mock_logger.add.assert_any_call(custom_path, rotation="5 MB", level="INFO")

    # Verify add was called exactly twice (stderr and file)
    assert mock_logger.add.call_count == 2


@patch("kratio.utils.logging_config.logger")
def test_setup_logging_silent_mode(mock_logger):
    """Test setup_logging with silent mode enabled."""
    # Call the function with silent mode enabled
    setup_logging(silent=True)

    # Verify logger.remove was called
    mock_logger.remove.assert_called_once()

    # Verify stderr handler was NOT added (silent mode)
    # We can check this by ensuring add was called exactly once (only for file)
    assert mock_logger.add.call_count == 1

    # Verify file handler was added with rotation and INFO level
    mock_logger.add.assert_called_once_with("logs/kratio.log", rotation="5 MB", level="INFO")


@patch("kratio.utils.logging_config.logger")
def test_setup_logging_all_custom_parameters(mock_logger):
    """Test setup_logging with all custom parameters."""
    # Call the function with all custom parameters
    custom_path = "logs/custom.log"
    custom_level = "ERROR"
    setup_logging(log_file_path=custom_path, level=custom_level, silent=False)

    # Verify logger.remove was called
    mock_logger.remove.assert_called_once()

    # Verify stderr handler was added with custom level
    mock_logger.add.assert_any_call(sys.stderr, level=custom_level)

    # Verify file handler was added with custom path, rotation and custom level
    mock_logger.add.assert_any_call(custom_path, rotation="5 MB", level=custom_level)

    # Verify add was called exactly twice (stderr and file)
    assert mock_logger.add.call_count == 2
