import pandas as pd
from loguru import logger


def format_top_keywords(df: pd.DataFrame, top_n: int) -> list[dict]:
    """
    Formats the top N keywords or noun chunks from a DataFrame into a list of dictionaries.

    Args:
        df (pd.DataFrame): The DataFrame containing keyword/noun chunk analysis.
                           Expected to have 'keyword' and 'density' columns.
        top_n (int): The number of top keywords/noun chunks to format.

    Returns:
        list[dict]: A list of dictionaries, each representing a keyword/noun chunk
                    with 'keyword', 'density', and 'frequency'.
    """
    if df.empty:
        return []

    top_keywords = df.head(top_n)
    formatted_results = []

    for _index, row in top_keywords.iterrows():
        density_col = "WordDensity" if "WordDensity" in row else "NounChunkDensity"
        frequency_col = "WordFrequency" if "WordFrequency" in row else "NounChunkFrequency"
        formatted_results.append({"keyword": row.name, "density": row[density_col], "frequency": row[frequency_col]})
    return formatted_results


def _log_formatted_keywords(formatted_list: list[dict], top_n: int) -> None:
    """
    Displays a formatted list of top keywords/noun chunks using the logger.

    Args:
        formatted_list (list[dict]): A list of dictionaries, each representing a keyword/noun chunk.
        top_n (int): The number of top keywords/noun chunks being displayed.
    """
    if not formatted_list:
        logger.info("No data to display for keywords.")
        return

    logger.info(f"\n--- Top {top_n} Keywords/Noun Chunks ---")
    for item in formatted_list:
        logger.info(f"Keyword: {item['keyword']}, Density: {item['density']:.4f}, Frequency: {item['frequency']}")
    logger.info("--------------------------------------")


def display_top_keywords(df: pd.DataFrame, top_n: int) -> None:
    """
    Formats and displays the top N keywords or noun chunks from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing keyword/noun chunk analysis.
                           Expected to have 'keyword' and 'density' columns.
        top_n (int): The number of top keywords/noun chunks to display.
    """
    formatted_data = format_top_keywords(df, top_n)
    _log_formatted_keywords(formatted_data, top_n)
