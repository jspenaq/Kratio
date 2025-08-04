import pandas as pd
from loguru import logger


def display_top_keywords(df: pd.DataFrame, top_n: int) -> None:
    """
    Displays the top N keywords or noun chunks from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing keyword/noun chunk analysis.
                          Expected to have 'keyword' and 'density' columns.
        top_n (int): The number of top keywords/noun chunks to display.
    """
    if df.empty:
        logger.info("No data to display for keywords.")
        return

    top_keywords = df.head(top_n)

    logger.info(f"\n--- Top {top_n} Keywords/Noun Chunks ---")
    for _index, row in top_keywords.iterrows():
        # The keyword/noun chunk is in the DataFrame's index
        density_col = "WordDensity" if "WordDensity" in row else "NounChunkDensity"
        frequency_col = "WordFrequency" if "WordFrequency" in row else "NounChunkFrequency"
        logger.info(f"Keyword: {row.name}, Density: {row[density_col]:.4f}, Frequency: {row[frequency_col]}")
    logger.info("--------------------------------------")
