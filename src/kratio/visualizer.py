import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from kratio.constants import ANALYSIS_TYPE_WORDS


def visualize_top_keywords(df: pd.DataFrame, top_n: int = 10, analysis_type: str = ANALYSIS_TYPE_WORDS) -> None:
    """
    Generates a bar chart visualization of the top N keywords/noun chunks and their densities.

    Args:
        df (pandas.DataFrame): A DataFrame with word frequencies and keyword densities.
        top_n (int): The number of top keywords to display.
        analysis_type (str): Type of analysis ('words' or 'noun_chunks').
    """
    top_keywords = df.head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(y=top_keywords.index, x="Density", data=top_keywords, orient="h", ax=ax)
    ax.tick_params(axis="y", rotation=0)
    ax.set_xlabel("Density (%)")
    if analysis_type == ANALYSIS_TYPE_WORDS:
        ax.set_ylabel("Keyword")
        ax.set_title(f"Top {top_n} Keywords")
    else:
        ax.set_ylabel("Noun Chunk")
        ax.set_title(f"Top {top_n} Noun Chunks")
    plt.tight_layout()
    sns.despine(left=True)
    plt.show()
