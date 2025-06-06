import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_top_keywords(df: pd.DataFrame, top_n: int = 10) -> None:
    """
    Generates a bar chart visualization of the top N keywords and their densities.

    Args:
        df (pandas.DataFrame): A DataFrame with word frequencies and keyword densities.
        top_n (int): The number of top keywords to display.
    """
    top_keywords = df.head(top_n)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_keywords.index, y="Density", data=top_keywords)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Keyword")
    plt.ylabel("Keyword Density (%)")
    plt.title(f"Top {top_n} Keywords")
    plt.tight_layout()
    plt.show()
