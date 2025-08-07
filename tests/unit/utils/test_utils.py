import json
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest
from tabulate import tabulate

from kratio.utils.utils import (
    display_top_keywords,
    format_top_keywords,
    _log_formatted_keywords,
)


@pytest.fixture
def sample_word_df():
    """Create a sample DataFrame with word analysis data."""
    data = {
        "WordDensity": [0.05, 0.04, 0.03, 0.02, 0.01],
        "WordFrequency": [10, 8, 6, 4, 2],
    }
    return pd.DataFrame(data, index=["word1", "word2", "word3", "word4", "word5"])


@pytest.fixture
def sample_noun_chunk_df():
    """Create a sample DataFrame with noun chunk analysis data."""
    data = {
        "NounChunkDensity": [0.06, 0.05, 0.04, 0.03, 0.02],
        "NounChunkFrequency": [12, 10, 8, 6, 4],
    }
    return pd.DataFrame(data, index=["chunk1", "chunk2", "chunk3", "chunk4", "chunk5"])


@pytest.fixture
def empty_df():
    """Create an empty DataFrame."""
    return pd.DataFrame()


def test_format_top_keywords_with_word_df(sample_word_df):
    """Test format_top_keywords with word analysis DataFrame."""
    result = format_top_keywords(sample_word_df, 3)
    
    assert len(result) == 3
    assert result[0]["keyword"] == "word1"
    assert result[0]["density"] == 0.05
    assert result[0]["frequency"] == 10
    assert result[2]["keyword"] == "word3"


def test_format_top_keywords_with_noun_chunk_df(sample_noun_chunk_df):
    """Test format_top_keywords with noun chunk analysis DataFrame."""
    result = format_top_keywords(sample_noun_chunk_df, 3)
    
    assert len(result) == 3
    assert result[0]["keyword"] == "chunk1"
    assert result[0]["density"] == 0.06
    assert result[0]["frequency"] == 12
    assert result[2]["keyword"] == "chunk3"


def test_format_top_keywords_with_empty_df(empty_df):
    """Test format_top_keywords with an empty DataFrame."""
    result = format_top_keywords(empty_df, 3)
    
    assert result == []


def test_format_top_keywords_with_top_n_greater_than_df_size(sample_word_df):
    """Test format_top_keywords when top_n is greater than DataFrame size."""
    result = format_top_keywords(sample_word_df, 10)
    
    assert len(result) == 5  # Should return all rows, not more than available


def test_format_top_keywords_with_top_n_zero(sample_word_df):
    """Test format_top_keywords with top_n=0."""
    result = format_top_keywords(sample_word_df, 0)
    
    assert result == []


@patch("kratio.utils.utils.logger")
def test_log_formatted_keywords_with_data(mock_logger):
    """Test _log_formatted_keywords with valid data."""
    formatted_list = [
        {"keyword": "word1", "density": 0.05, "frequency": 10},
        {"keyword": "word2", "density": 0.04, "frequency": 8},
    ]
    
    _log_formatted_keywords(formatted_list, 2)
    
    # Check logger calls
    assert mock_logger.info.call_count == 4  # Header + 2 items + footer
    mock_logger.info.assert_any_call("\n--- Top 2 Keywords/Noun Chunks ---")
    mock_logger.info.assert_any_call("Keyword: word1, Density: 0.0500, Frequency: 10")
    mock_logger.info.assert_any_call("Keyword: word2, Density: 0.0400, Frequency: 8")
    mock_logger.info.assert_any_call("--------------------------------------")


@patch("kratio.utils.utils.logger")
def test_log_formatted_keywords_with_empty_list(mock_logger):
    """Test _log_formatted_keywords with an empty list."""
    _log_formatted_keywords([], 5)
    
    mock_logger.info.assert_called_once_with("No data to display for keywords.")


@patch("kratio.utils.utils.print")
def test_display_top_keywords_json_format(mock_print, sample_word_df):
    """Test display_top_keywords with JSON format."""
    display_top_keywords(sample_word_df, 2, "json")
    
    # Get the argument passed to print
    printed_output = mock_print.call_args[0][0]
    
    # Parse the JSON output and verify
    parsed_json = json.loads(printed_output)
    assert len(parsed_json) == 2
    assert parsed_json[0]["keyword"] == "word1"
    assert parsed_json[1]["keyword"] == "word2"


@patch("kratio.utils.utils.print")
def test_display_top_keywords_csv_format(mock_print, sample_word_df):
    """Test display_top_keywords with CSV format."""
    display_top_keywords(sample_word_df, 2, "csv")
    
    # Get the argument passed to print
    printed_output = mock_print.call_args[0][0]
    
    # Verify CSV output contains expected headers and data
    assert "keyword,density,frequency" in printed_output
    assert "word1" in printed_output
    assert "word2" in printed_output


@patch("kratio.utils.utils.print")
@patch("kratio.utils.utils.tabulate")
def test_display_top_keywords_table_format(mock_tabulate, mock_print, sample_word_df):
    """Test display_top_keywords with table format."""
    mock_tabulate.return_value = "Mocked Table Output"
    
    display_top_keywords(sample_word_df, 2, "table")
    
    # Verify tabulate was called with correct arguments
    mock_tabulate.assert_called_once()
    args, kwargs = mock_tabulate.call_args
    assert len(args[0]) == 2  # First argument should be list of 2 items
    assert kwargs["headers"] == "keys"
    assert kwargs["tablefmt"] == "grid"
    
    # Verify print was called with tabulate's output
    mock_print.assert_called_once_with("Mocked Table Output")


@patch("kratio.utils.utils.print")
def test_display_top_keywords_with_empty_df(mock_print, empty_df):
    """Test display_top_keywords with an empty DataFrame."""
    display_top_keywords(empty_df, 5, "json")
    
    mock_print.assert_called_once_with("No data to display for keywords.")


@patch("kratio.utils.utils._log_formatted_keywords")
def test_display_top_keywords_unknown_format(mock_log_formatted, sample_word_df):
    """Test display_top_keywords with an unknown format type."""
    display_top_keywords(sample_word_df, 3, "unknown_format")
    
    # Verify fallback to logging function
    mock_log_formatted.assert_called_once()
    args = mock_log_formatted.call_args[0]
    assert len(args[0]) == 3  # First argument should be formatted list with 3 items
    assert args[1] == 3  # Second argument should be top_n=3


@patch("kratio.utils.utils.print")
def test_display_top_keywords_default_format(mock_print, sample_word_df):
    """Test display_top_keywords with default format (table)."""
    display_top_keywords(sample_word_df, 2)
    
    # Verify print was called (with tabulate output)
    mock_print.assert_called_once()