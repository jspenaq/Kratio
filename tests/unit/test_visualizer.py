from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from kratio.constants import ANALYSIS_TYPE_NOUN_CHUNKS, ANALYSIS_TYPE_WORDS
from kratio.visualization.visualizer import (
    display_plot,
    persist_plot,
    visualize_top_keywords,
)


@pytest.fixture
def mock_plot_modules():
    with patch("matplotlib.pyplot.subplots") as mock_subplots, patch(
        "seaborn.barplot"
    ) as mock_barplot, patch(
        "matplotlib.pyplot.tight_layout"
    ) as mock_tight_layout, patch(
        "matplotlib.pyplot.show"
    ) as mock_show:
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        yield {
            "subplots": mock_subplots,
            "figure": mock_fig,
            "ax": mock_ax,
            "barplot": mock_barplot,
            "tight_layout": mock_tight_layout,
            "show": mock_show,
        }


def create_sample_dataframe(analysis_type, num_rows=10):
    if analysis_type == ANALYSIS_TYPE_WORDS:
        density_col = "WordDensity"
        index_name = "Keyword"
        index_prefix = "keyword"
    else:
        density_col = "NounChunkDensity"
        index_name = "Noun Chunk"
        index_prefix = "noun_chunk"

    data = {
        "Frequency": [i * 10 for i in range(num_rows, 0, -1)],
        density_col: [i * 5.0 for i in range(num_rows, 0, -1)],
    }
    index = [f"{index_prefix}_{i}" for i in range(num_rows, 0, -1)]
    return pd.DataFrame(data, index=pd.Index(index, name=index_name))


@pytest.mark.parametrize(
    "analysis_type, density_col, expected_ylabel, expected_title_keyword",
    [
        (ANALYSIS_TYPE_WORDS, "WordDensity", "Keyword", "Keywords"),
        (
            ANALYSIS_TYPE_NOUN_CHUNKS,
            "NounChunkDensity",
            "Noun Chunk",
            "Noun Chunks",
        ),
    ],
)
def test_visualize_top_keywords(
    mock_plot_modules,
    analysis_type,
    density_col,
    expected_ylabel,
    expected_title_keyword,
):
    df = create_sample_dataframe(analysis_type, num_rows=15)
    top_n = 10
    expected_top = df.head(top_n)

    visualize_top_keywords(df, top_n=top_n, analysis_type=analysis_type)

    mock_plot_modules["subplots"].assert_called_once_with(figsize=(12, 6))
    mock_plot_modules["barplot"].assert_called_once()
    _, kwargs = mock_plot_modules["barplot"].call_args
    pd.testing.assert_index_equal(kwargs["y"], expected_top.index)
    assert kwargs["x"] == density_col
    pd.testing.assert_frame_equal(kwargs["data"], expected_top)

    mock_ax = mock_plot_modules["ax"]
    mock_ax.set_ylabel.assert_called_once_with(expected_ylabel)
    mock_ax.set_title.assert_called_once_with(f"Top {top_n} {expected_title_keyword}")


def test_display_plot(mock_plot_modules):
    mock_fig = MagicMock()
    display_plot(mock_fig)
    mock_plot_modules["show"].assert_called_once()


def test_persist_plot():
    mock_fig = MagicMock()
    save_path = "/tmp/test_plot.png"
    persist_plot(mock_fig, save_path)
    mock_fig.savefig.assert_called_once_with(save_path)
