import time

import pandas as pd
import spacy
from loguru import logger

# Load the English language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.exception(
        "Downloading spaCy model 'en_core_web_sm' failed. "
        "Please run 'python -m spacy download en_core_web_sm' to download it manually.",
    )
    # Exit the program or handle the error appropriately
    exit(1)


def analyze_text_words(text: str) -> pd.DataFrame:
    """
    Analyzes the given text and returns a DataFrame with word frequencies and keyword densities.

    Args:
        text (str): The text to analyze.

    Returns:
        pandas.DataFrame: A DataFrame with word frequencies and keyword densities.
    """
    start_time = time.perf_counter()
    # Process the text with spaCy
    doc = nlp(text)

    # Create a list of words, removing stop words, punctuation, and tokens without sense
    words = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.lemma_.strip()]
    end_time = time.perf_counter()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    logger.info(f"Time spent analyzing words: {duration:.2f} ms")

    # Calculate word frequencies
    word_counts = pd.Series(words).value_counts()

    # Calculate keyword densities
    total_words = len(words)

    # Handle the case where there are no relevant words to avoid ZeroDivisionError
    if total_words == 0:
        # Return an empty DataFrame with the correct column types and index name
        empty_df = pd.DataFrame({"Frequency": pd.Series(dtype=int), "Density": pd.Series(dtype=float)})
        empty_df.index.name = "Keyword"
        return empty_df

    word_densities = word_counts / total_words * 100

    # Create a DataFrame
    df = pd.DataFrame({"Frequency": word_counts, "Density": word_densities})
    df.index.name = "Keyword"
    return df.sort_values("Frequency", ascending=False)


def analyze_text_noun_chunks(text: str) -> pd.DataFrame:
    """
    Analyzes the given text and returns a DataFrame with noun chunk frequencies and densities.

    Args:
        text (str): The text to analyze.

    Returns:
        pandas.DataFrame: A DataFrame with noun chunk frequencies and densities.
    """
    start_time = time.perf_counter()
    # Process the text with spaCy
    doc = nlp(text)

    # Create a list of noun chunks, removing stop words, punctuation, and tokens without sense
    noun_chunks = [
        chunk.text.lower()
        for chunk in doc.noun_chunks
        if not chunk.root.is_stop and not chunk.root.is_punct and chunk.text.strip()
    ]
    end_time = time.perf_counter()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    logger.info(f"Time spent analyzing noun chunks: {duration:.2f} ms")

    # Calculate noun chunk frequencies
    noun_counts = pd.Series(noun_chunks).value_counts()

    # Calculate noun chunk densities
    total_chunks = len(noun_chunks)

    # Handle the case where there are no relevant chunks to avoid ZeroDivisionError
    if total_chunks == 0:
        # Return an empty DataFrame with the correct column types and index name
        empty_df = pd.DataFrame({"Frequency": pd.Series(dtype=int), "Density": pd.Series(dtype=float)})
        empty_df.index.name = "Noun Chunk"
        return empty_df

    noun_densities = noun_counts / total_chunks * 100

    # Create a DataFrame
    df = pd.DataFrame({"Frequency": noun_counts, "Density": noun_densities})
    df.index.name = "Noun Chunk"
    return df.sort_values("Frequency", ascending=False)
