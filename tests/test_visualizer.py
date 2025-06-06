from unittest.mock import patch

import pandas as pd
import pytest

# Import the function to be tested
from src.kratio.visualizer import visualize_top_keywords


@pytest.fixture
def mock_plot_modules():
    """
    Mocks matplotlib.pyplot and seaborn functions to prevent actual plotting
    and allow verification of calls.
    """
    # Use patch as a context manager for multiple mocks
    with (
        patch("matplotlib.pyplot.figure") as mock_figure,
        patch("seaborn.barplot") as mock_barplot,
        patch("matplotlib.pyplot.xticks") as mock_xticks,
        patch("matplotlib.pyplot.xlabel") as mock_xlabel,
        patch("matplotlib.pyplot.ylabel") as mock_ylabel,
        patch("matplotlib.pyplot.title") as mock_title,
        patch("matplotlib.pyplot.tight_layout") as mock_tight_layout,
        patch("matplotlib.pyplot.show") as mock_show,
    ):
        # Yield the mocked objects so tests can access them for assertions
        yield {
            "figure": mock_figure,
            "barplot": mock_barplot,
            "xticks": mock_xticks,
            "xlabel": mock_xlabel,
            "ylabel": mock_ylabel,
            "title": mock_title,
            "tight_layout": mock_tight_layout,
            "show": mock_show,
        }


def create_sample_dataframe(num_rows: int = 10) -> pd.DataFrame:
    """Helper function to create a sample DataFrame for testing."""
    data = {
        "Frequency": [i * 10 for i in range(num_rows, 0, -1)],
        "Density": [i * 5.0 for i in range(num_rows, 0, -1)],
    }
    index = [f"keyword_{i}" for i in range(num_rows, 0, -1)]
    return pd.DataFrame(data, index=pd.Index(index, name="Keyword"))


def test_visualize_top_keywords_basic(mock_plot_modules):
    """
    Arrange: Create a sample DataFrame with more than default top_n keywords.
    Act: Call visualize_top_keywords with the DataFrame.
    Assert: Verify that plotting functions are called with expected arguments for top 10 keywords.
    """
    # Arrange
    df = create_sample_dataframe(num_rows=15)
    top_n = 10  # Default value for visualize_top_keywords
    expected_top_keywords = df.head(top_n)

    # Act
    visualize_top_keywords(df)

    # Assert
    mock_plot_modules["figure"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    # Verify arguments passed to sns.barplot
    args, kwargs = mock_plot_modules["barplot"].call_args
    # The 'x' argument to seaborn.barplot is a pandas Index, not a Series.
    # Use assert_index_equal for comparing Index objects.
    pd.testing.assert_index_equal(kwargs["x"], expected_top_keywords.index)
    assert kwargs["y"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], expected_top_keywords)

    mock_plot_modules["xticks"].assert_called_once_with(rotation=45, ha="right")
    mock_plot_modules["xlabel"].assert_called_once_with("Keyword")
    mock_plot_modules["ylabel"].assert_called_once_with("Keyword Density (%)")
    mock_plot_modules["title"].assert_called_once_with(f"Top {top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["show"].assert_called_once()


def test_visualize_top_keywords_fewer_than_top_n(mock_plot_modules):
    """
    Arrange: Create a sample DataFrame with fewer than default top_n keywords.
    Act: Call visualize_top_keywords with the DataFrame.
    Assert: Verify that plotting functions are called with all available keywords.
    """
    # Arrange
    df = create_sample_dataframe(num_rows=5)
    top_n = 10  # Default value for visualize_top_keywords
    expected_top_keywords = df  # All 5 keywords should be used

    # Act
    visualize_top_keywords(df)

    # Assert
    mock_plot_modules["figure"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    args, kwargs = mock_plot_modules["barplot"].call_args
    # The 'x' argument to seaborn.barplot is a pandas Index, not a Series.
    # Use assert_index_equal for comparing Index objects.
    pd.testing.assert_index_equal(kwargs["x"], expected_top_keywords.index)
    assert kwargs["y"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], expected_top_keywords)

    mock_plot_modules["xticks"].assert_called_once_with(rotation=45, ha="right")
    mock_plot_modules["xlabel"].assert_called_once_with("Keyword")
    mock_plot_modules["ylabel"].assert_called_once_with("Keyword Density (%)")
    mock_plot_modules["title"].assert_called_once_with(f"Top {top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["show"].assert_called_once()


def test_visualize_top_keywords_empty_dataframe(mock_plot_modules):
    """
    Arrange: Create an empty DataFrame.
    Act: Call visualize_top_keywords with the empty DataFrame.
    Assert: Verify that plotting functions are called, and barplot receives empty data.
    """
    # Arrange
    df = pd.DataFrame(columns=["Frequency", "Density"], index=pd.Index([], name="Keyword"))
    df["Frequency"] = df["Frequency"].astype(int)
    df["Density"] = df["Density"].astype(float)
    top_n = 10  # Default value

    # Act
    visualize_top_keywords(df)

    # Assert
    mock_plot_modules["figure"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    args, kwargs = mock_plot_modules["barplot"].call_args
    # For an empty DataFrame, x will be an empty Index, data will be an empty DataFrame
    # The 'x' argument to seaborn.barplot is a pandas Index, not a Series.
    # Use assert_index_equal for comparing Index objects.
    pd.testing.assert_index_equal(kwargs["x"], df.index)  # Should be the empty df's index
    assert kwargs["y"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], df)  # Should be the empty df passed in

    mock_plot_modules["xticks"].assert_called_once_with(rotation=45, ha="right")
    mock_plot_modules["xlabel"].assert_called_once_with("Keyword")
    mock_plot_modules["ylabel"].assert_called_once_with("Keyword Density (%)")
    mock_plot_modules["title"].assert_called_once_with(f"Top {top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["show"].assert_called_once()


def test_visualize_top_keywords_custom_top_n(mock_plot_modules):
    """
    Arrange: Create a sample DataFrame and specify a custom top_n value.
    Act: Call visualize_top_keywords with the DataFrame and custom top_n.
    Assert: Verify that plotting functions are called with expected arguments for the custom top_n.
    """
    # Arrange
    df = create_sample_dataframe(num_rows=20)
    custom_top_n = 5
    expected_top_keywords = df.head(custom_top_n)

    # Act
    visualize_top_keywords(df, top_n=custom_top_n)

    # Assert
    mock_plot_modules["figure"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    args, kwargs = mock_plot_modules["barplot"].call_args
    # The 'x' argument to seaborn.barplot is a pandas Index, not a Series.
    # Use assert_index_equal for comparing Index objects.
    pd.testing.assert_index_equal(kwargs["x"], expected_top_keywords.index)
    assert kwargs["y"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], expected_top_keywords)

    mock_plot_modules["xticks"].assert_called_once_with(rotation=45, ha="right")
    mock_plot_modules["xlabel"].assert_called_once_with("Keyword")
    mock_plot_modules["ylabel"].assert_called_once_with("Keyword Density (%)")
    mock_plot_modules["title"].assert_called_once_with(f"Top {custom_top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["show"].assert_called_once()
