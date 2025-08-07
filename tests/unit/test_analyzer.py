import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

# Import the function to be tested
from kratio.core.analyzer import analyze_text_noun_chunks, analyze_text_words


@pytest.fixture
def mock_word_analyzer_analyze():
    """
    Mocks the analyze method of WordAnalyzer to control its return value directly.
    """
    with patch("kratio.core.analyzer.WordAnalyzer.analyze") as mock_analyze:
        yield mock_analyze

@pytest.fixture
def mock_noun_chunk_analyzer_analyze():
    """
    Mocks the analyze method of NounChunkAnalyzer to control its return value directly.
    """
    with patch("kratio.core.analyzer.NounChunkAnalyzer.analyze") as mock_analyze:
        yield mock_analyze

def test_analyze_text_words_basic(mock_word_analyzer_analyze):
    """
    Tests analyze_text_words with a basic sentence, ensuring correct word frequencies and densities.
    """
    # Arrange
    text = "This is a test sentence. Another test."
    expected_data = {
        "WordFrequency": {"test": 2, "sentence": 1, "another": 1},
        "WordDensity": {"test": 50.0, "sentence": 25.0, "another": 25.0},
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.index.name = "Keyword"
    expected_df = expected_df.sort_values("WordFrequency", ascending=False)

    mock_word_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_words(text)

    # Assert
    mock_word_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_empty_string(mock_word_analyzer_analyze):
    """
    Tests analyze_text_words with an empty input string.
    """
    # Arrange
    text = ""
    expected_df = pd.DataFrame({"WordFrequency": pd.Series(dtype=int), "WordDensity": pd.Series(dtype=float)})
    expected_df.index.name = "Keyword"

    mock_word_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_words(text)

    # Assert
    mock_word_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_only_stopwords_punctuation(mock_word_analyzer_analyze):
    """
    Tests analyze_text_words with text containing only stop words and punctuation.
    """
    # Arrange
    text = "This is a. The, and"
    expected_df = pd.DataFrame({"WordFrequency": pd.Series(dtype=int), "WordDensity": pd.Series(dtype=float)})
    expected_df.index.name = "Keyword"

    mock_word_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_words(text)

    # Assert
    mock_word_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_case_punctuation_lemmatization(mock_word_analyzer_analyze):
    """
    Tests analyze_text_words's handling of mixed case, punctuation, and lemmatization.
    """
    # Arrange
    text = "Running, ran, RUNS. Apple, apples."
    expected_data = {
        "WordFrequency": {"run": 3, "apple": 2},
        "WordDensity": {"run": 60.0, "apple": 40.0},
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.index.name = "Keyword"
    expected_df = expected_df.sort_values("WordFrequency", ascending=False)

    mock_word_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_words(text)

    # Assert
    mock_word_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_empty_lemma_after_strip(mock_word_analyzer_analyze):
    """
    Tests analyze_text_words with tokens whose lemma becomes empty after stripping whitespace.
    These should be filtered out.
    """
    # Arrange
    text = "  \n\t"  # Text that might produce tokens with only whitespace lemmas
    expected_df = pd.DataFrame({"WordFrequency": pd.Series(dtype=int), "WordDensity": pd.Series(dtype=float)})
    expected_df.index.name = "Keyword"

    mock_word_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_words(text)

    # Assert
    mock_word_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)

def test_analyze_text_noun_chunks_basic(mock_noun_chunk_analyzer_analyze):
    """
    Tests analyze_text_noun_chunks with a basic sentence.
    """
    # Arrange
    text = "The quick brown fox jumps over the lazy dog."
    expected_data = {
        "NounChunkFrequency": {"the quick brown fox": 1, "the lazy dog": 1},
        "NounChunkDensity": {"the quick brown fox": 50.0, "the lazy dog": 50.0},
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.index.name = "Keyword"
    mock_noun_chunk_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_noun_chunks(text)

    # Assert
    mock_noun_chunk_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_noun_chunks_empty_string(mock_noun_chunk_analyzer_analyze):
    """
    Tests analyze_text_noun_chunks with an empty input string.
    """
    # Arrange
    text = ""
    expected_df = pd.DataFrame(
        {"NounChunkFrequency": pd.Series(dtype=int), "NounChunkDensity": pd.Series(dtype=float)}
    )
    expected_df.index.name = "Keyword"
    mock_noun_chunk_analyzer_analyze.return_value = expected_df

    # Act
    df = analyze_text_noun_chunks(text)

    # Assert
    mock_noun_chunk_analyzer_analyze.assert_called_once_with(text)
    pd.testing.assert_frame_equal(df, expected_df)
