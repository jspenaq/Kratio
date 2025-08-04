import pandas as pd

from kratio.core.analyzers import WordAnalyzer, NounChunkAnalyzer

def analyze_text_words(text: str) -> pd.DataFrame:
    """
    Analyzes the given text and returns a DataFrame with word frequencies and keyword densities.

    Args:
        text (str): The text to analyze.

    Returns:
        pandas.DataFrame: A DataFrame with word frequencies and keyword densities.
    """
    analyzer = WordAnalyzer()
    return analyzer.analyze(text)


def analyze_text_noun_chunks(text: str) -> pd.DataFrame:
    """
    Analyzes the given text and returns a DataFrame with noun chunk frequencies and densities.

    Args:
        text (str): The text to analyze.

    Returns:
        pandas.DataFrame: A DataFrame with noun chunk frequencies and densities.
    """
    analyzer = NounChunkAnalyzer()
    return analyzer.analyze(text)
