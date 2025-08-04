import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from kratio.constants import ANALYSIS_TYPE_WORDS


def _get_plot_metadata(analysis_type: str, top_n: int) -> dict:
    """
    Determines the appropriate y-axis label and plot title based on the analysis type.
    """
    if analysis_type == ANALYSIS_TYPE_WORDS:
        return {
            "ylabel": "Keyword",
            "title": f"Top {top_n} Keywords",
        }
    return {
        "ylabel": "Noun Chunk",
        "title": f"Top {top_n} Noun Chunks",
    }


def visualize_top_keywords(
    df: pd.DataFrame,
    top_n: int = 10,
    analysis_type: str = ANALYSIS_TYPE_WORDS,
) -> Figure:
    """
    Generates a bar chart visualization of the top N keywords/noun chunks and their densities.

    Args:
        df (pandas.DataFrame): A DataFrame with word frequencies and keyword densities.
        top_n (int): The number of top keywords to display.
        analysis_type (str): Type of analysis ('words' or 'noun_chunks').

    Returns:
        matplotlib.figure.Figure: The matplotlib Figure object containing the plot.
    """
    top_keywords = df.head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    density_col = "WordDensity" if analysis_type == ANALYSIS_TYPE_WORDS else "NounChunkDensity"
    sns.barplot(y=top_keywords.index, x=density_col, data=top_keywords, orient="h", ax=ax)
    ax.tick_params(axis="y", rotation=0)
    ax.set_xlabel("Density (%)")

    metadata = _get_plot_metadata(analysis_type, top_n)
    ax.set_ylabel(metadata["ylabel"])
    ax.set_title(metadata["title"])

    plt.tight_layout()
    sns.despine(left=True)
    return fig


def display_plot(fig: Figure) -> None:
    """
    Displays a matplotlib Figure.

    Args:
        fig (matplotlib.figure.Figure): The Figure object to display.
    """
    plt.show()


def persist_plot(fig: Figure, save_path: str) -> None:
    """
    Saves a matplotlib Figure to a specified path.

    Args:
        fig (matplotlib.figure.Figure): The Figure object to save.
        save_path (str): The file path to save the figure to.
    """
    fig.savefig(save_path)
