from unittest.mock import patch

import pandas as pd
import pytest

from src.kratio.io.serializer import Serializer


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Pytest fixture to create a sample DataFrame for testing.

    Returns:
        pd.DataFrame: A sample DataFrame with test data
    """
    return pd.DataFrame({"id": [1, 2, 3], "name": ["Alpha", "Beta", "Gamma"], "value": [10.5, 20.3, 30.1]})


@pytest.fixture
def serializer() -> Serializer:
    """
    Pytest fixture to create a Serializer instance.

    Returns:
        Serializer: A Serializer instance for testing
    """
    return Serializer()


def test_serialize_to_csv(sample_df, serializer):
    """Test that DataFrame is correctly serialized to CSV format."""
    # Arrange
    output_path = "test_output.csv"

    # Act & Assert
    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv, patch("loguru.logger.info") as mock_logger_info:
        serializer.serialize(sample_df, output_path)

        # Assert that to_csv was called with the correct parameters
        mock_to_csv.assert_called_once_with(output_path, index=True)

        # Assert that the correct log message was generated
        mock_logger_info.assert_called_once_with(f"DataFrame successfully dumped to {output_path} (CSV format).")


def test_serialize_to_json(sample_df, serializer):
    """Test that DataFrame is correctly serialized to JSON format."""
    # Arrange
    output_path = "test_output.json"

    # Act & Assert
    with patch.object(pd.DataFrame, "to_json") as mock_to_json, patch("loguru.logger.info") as mock_logger_info:
        serializer.serialize(sample_df, output_path)

        # Assert that to_json was called with the correct parameters
        mock_to_json.assert_called_once_with(output_path, orient="records", indent=4)

        # Assert that the correct log message was generated
        mock_logger_info.assert_called_once_with(f"DataFrame successfully dumped to {output_path} (JSON format).")


def test_serialize_unsupported_format(sample_df, serializer):
    """Test that an error is logged when an unsupported format is provided."""
    # Arrange
    output_path = "test_output.xlsx"  # Unsupported format

    # Act & Assert
    with patch("loguru.logger.error") as mock_logger_error:
        serializer.serialize(sample_df, output_path)

        # Assert that the error was logged
        mock_logger_error.assert_called_once_with("Unsupported output format: .xlsx. Please use .csv or .json.")


def test_serialize_with_uppercase_extension(sample_df, serializer):
    """Test that file extension case is handled correctly."""
    # Arrange
    output_path = "test_output.CSV"  # Uppercase extension

    # Act & Assert
    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv, patch("loguru.logger.info") as mock_logger_info:
        serializer.serialize(sample_df, output_path)

        # Assert that to_csv was called despite the uppercase extension
        mock_to_csv.assert_called_once_with(output_path, index=True)

        # Assert that the correct log message was generated
        mock_logger_info.assert_called_once_with(f"DataFrame successfully dumped to {output_path} (CSV format).")
