from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Import the function to be tested
from kratio.visualization.visualizer import (
    persist_plot,
    visualize_top_keywords,
)


@pytest.fixture
def mock_plot_modules():
    """
    Mocks matplotlib.pyplot and seaborn functions, and kratio.visualization.visualizer
    functions to prevent actual plotting and allow verification of calls.
    """
    # Use patch as a context manager for multiple mocks
    with (
        patch("matplotlib.pyplot.subplots") as mock_subplots,
        patch("seaborn.barplot") as mock_barplot,
        patch("matplotlib.pyplot.tight_layout") as mock_tight_layout,
        patch("kratio.visualization.visualizer.display_plot") as mock_display_plot,
        patch("kratio.visualization.visualizer.persist_plot") as mock_persist_plot,
    ):
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        yield {
            "subplots": mock_subplots,
            "figure": mock_fig,
            "ax": mock_ax,
            "barplot": mock_barplot,
            "tight_layout": mock_tight_layout,
            "display_plot": mock_display_plot,
            "persist_plot": mock_persist_plot,
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
    fig = visualize_top_keywords(df)

    # Assert
    mock_plot_modules["subplots"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    # Verify arguments passed to sns.barplot
    args, kwargs = mock_plot_modules["barplot"].call_args
    # The 'y' argument to seaborn.barplot is a pandas Index, not a Series.
    pd.testing.assert_index_equal(kwargs["y"], expected_top_keywords.index)
    assert kwargs["x"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], expected_top_keywords)
    assert kwargs["orient"] == "h"
    assert kwargs["ax"] == mock_plot_modules["ax"]

    mock_plot_modules["ax"].tick_params.assert_called_once_with(axis="y", rotation=0)
    mock_plot_modules["ax"].set_xlabel.assert_called_once_with("Density (%)")
    mock_plot_modules["ax"].set_ylabel.assert_called_once_with("Keyword")
    mock_plot_modules["ax"].set_title.assert_called_once_with(f"Top {top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["display_plot"].assert_called_once_with(fig)


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
    fig = visualize_top_keywords(df)

    # Assert
    mock_plot_modules["subplots"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    args, kwargs = mock_plot_modules["barplot"].call_args
    pd.testing.assert_index_equal(kwargs["y"], expected_top_keywords.index)
    assert kwargs["x"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], expected_top_keywords)
    assert kwargs["orient"] == "h"
    assert kwargs["ax"] == mock_plot_modules["ax"]

    mock_plot_modules["ax"].tick_params.assert_called_once_with(axis="y", rotation=0)
    mock_plot_modules["ax"].set_xlabel.assert_called_once_with("Density (%)")
    mock_plot_modules["ax"].set_ylabel.assert_called_once_with("Keyword")
    mock_plot_modules["ax"].set_title.assert_called_once_with(f"Top {top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["display_plot"].assert_called_once_with(fig)


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
    fig = visualize_top_keywords(df)

    # Assert
    mock_plot_modules["subplots"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    args, kwargs = mock_plot_modules["barplot"].call_args
    pd.testing.assert_index_equal(kwargs["y"], df.index)
    assert kwargs["x"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], df)
    assert kwargs["orient"] == "h"
    assert kwargs["ax"] == mock_plot_modules["ax"]

    mock_plot_modules["ax"].tick_params.assert_called_once_with(axis="y", rotation=0)
    mock_plot_modules["ax"].set_xlabel.assert_called_once_with("Density (%)")
    mock_plot_modules["ax"].set_ylabel.assert_called_once_with("Keyword")
    mock_plot_modules["ax"].set_title.assert_called_once_with(f"Top {top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["display_plot"].assert_called_once_with(fig)


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
    fig = visualize_top_keywords(df, top_n=custom_top_n)

    # Assert
    mock_plot_modules["subplots"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    args, kwargs = mock_plot_modules["barplot"].call_args
    pd.testing.assert_index_equal(kwargs["y"], expected_top_keywords.index)
    assert kwargs["x"] == "Density"
    pd.testing.assert_frame_equal(kwargs["data"], expected_top_keywords)
    assert kwargs["orient"] == "h"
    assert kwargs["ax"] == mock_plot_modules["ax"]

    mock_plot_modules["ax"].tick_params.assert_called_once_with(axis="y", rotation=0)
    mock_plot_modules["ax"].set_xlabel.assert_called_once_with("Density (%)")
    mock_plot_modules["ax"].set_ylabel.assert_called_once_with("Keyword")
    mock_plot_modules["ax"].set_title.assert_called_once_with(f"Top {custom_top_n} Keywords")
    mock_plot_modules["tight_layout"].assert_called_once()
    mock_plot_modules["display_plot"].assert_called_once_with(fig)


def test_visualize_top_keywords_save_path(mock_plot_modules):
    """
    Arrange: Create a sample DataFrame and a mock save_path.
    Act: Call visualize_top_keywords and then persist_plot.
    Assert: Verify that persist_plot is called with the figure and save_path.
    """
    # Arrange
    df = create_sample_dataframe(num_rows=15)
    save_path = "/tmp/test_plot.png"

    # Act
    fig = visualize_top_keywords(df)
    persist_plot(fig, save_path)

    # Assert
    mock_plot_modules["persist_plot"].assert_called_once_with(fig, save_path)
    # Ensure display_plot was NOT called
    mock_plot_modules["display_plot"].assert_not_called()
