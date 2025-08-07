from unittest.mock import MagicMock, patch

from kratio.utils.timing import timed


def test_timed_decorator_logs_execution_time():
    """
    Test that the `timed` decorator logs the execution time of a function.
    """
    # Arrange
    mock_logger = MagicMock()

    @timed("test_function")
    def sample_function(x, y):
        return x + y

    # Act
    with patch("kratio.utils.timing.logger", mock_logger):
        result = sample_function(1, 2)

    # Assert
    assert result == 3
    mock_logger.info.assert_called_once()
    call_args, _ = mock_logger.info.call_args
    assert "Time spent test_function" in call_args[0]
