import pandas as pd
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")


def analyze_text(text: str) -> pd.DataFrame:
    """
    Analyzes the given text and returns a DataFrame with word frequencies and keyword densities.

    Args:
        text (str): The text to analyze.

    Returns:
        pandas.DataFrame: A DataFrame with word frequencies and keyword densities.
    """
    # Process the text with spaCy
    doc = nlp(text)

    # Create a list of words, removing stop words, punctuation, and tokens without sense
    words = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.lemma_.strip()]

    # Calculate word frequencies
    word_counts = pd.Series(words).value_counts()

    # Calculate keyword densities
    total_words = len(words)
    word_densities = word_counts / total_words * 100

    # Create a DataFrame
    df = pd.DataFrame({"Frequency": word_counts, "Density": word_densities})
    df.index.name = "Keyword"
    return df.sort_values("Frequency", ascending=False)
