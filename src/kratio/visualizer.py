import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_top_keywords(df: pd.DataFrame, top_n: int = 10, analysis_type: str = "words") -> None:
    """
    Generates a bar chart visualization of the top N keywords/noun chunks and their densities.

    Args:
        df (pandas.DataFrame): A DataFrame with word frequencies and keyword densities.
        top_n (int): The number of top keywords to display.
        analysis_type (str): Type of analysis ('words' or 'noun_chunks').
    """
    top_keywords = df.head(top_n)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_keywords.index, y="Density", data=top_keywords)
    plt.xticks(rotation=45, ha="right")
    # Move ylabel inside the conditional block and make it specific
    if analysis_type == "words":
        plt.xlabel("Keyword")
        plt.ylabel("Keyword Density (%)")
        plt.title(f"Top {top_n} Keywords")
    else:
        plt.xlabel("Noun Chunk")
        plt.ylabel("Noun Chunk Density (%)")  # Added for consistency, assuming future tests
        plt.title(f"Top {top_n} Noun Chunks")
    plt.tight_layout()
    plt.show()
