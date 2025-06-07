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
    sns.barplot(y=top_keywords.index, x="Density", data=top_keywords, orient='h')
    plt.yticks(rotation=0)
    plt.xlabel("Density (%)")
    # Move ylabel inside the conditional block and make it specific
    if analysis_type == "words":
        plt.ylabel("Keyword")
        plt.title(f"Top {top_n} Keywords")
    else:
        plt.ylabel("Noun Chunk")
        plt.title(f"Top {top_n} Noun Chunks")
    plt.tight_layout()
    plt.show()
