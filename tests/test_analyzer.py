from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Import the function to be tested
from kratio.core.analyzer import analyze_text_words


# Helper class to create mock spaCy Token objects
class MockToken:
    """
    A simple mock object to simulate spaCy Token behavior needed for analyze_text_words.
    """

    def __init__(self, lemma: str, is_stop: bool = False, is_punct: bool = False) -> None:
        self.lemma_ = lemma
        self.is_stop = is_stop
        self.is_punct = is_punct


# Fixture to mock the globally loaded spaCy nlp object
# This fixture will replace 'src.kratio.analyzer.nlp' with a MagicMock
# for the duration of any test that uses it.
@pytest.fixture
def mock_nlp():
    """
    Mocks the spaCy nlp object used in analyzer.py to prevent actual model loading.
    """
    with patch("src.kratio.analyzer.nlp", new_callable=MagicMock) as mock_nlp_obj:
        yield mock_nlp_obj


def test_analyze_text_words_basic(mock_nlp):
    """
    Tests analyze_text_words with a basic sentence, ensuring correct word frequencies and densities.
    """
    # Arrange
    text = "This is a test sentence. Another test."

    # Configure the mock nlp object to return a mock Doc object
    # The mock Doc object will yield specific MockToken instances when iterated
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = [
        MockToken("this", is_stop=True),
        MockToken("be", is_stop=True),  # Lemma for 'is'
        MockToken("a", is_stop=True),
        MockToken("test", is_stop=False, is_punct=False),
        MockToken("sentence", is_stop=False, is_punct=False),
        MockToken(".", is_punct=True),
        MockToken("another", is_stop=False, is_punct=False),
        MockToken("test", is_stop=False, is_punct=False),
        MockToken(".", is_punct=True),
    ]
    mock_nlp.return_value = mock_doc  # When nlp(text) is called, return our mock_doc

    # Act
    df = analyze_text_words(text)

    # Assert
    expected_data = {
        "Frequency": {"test": 2, "sentence": 1, "another": 1},
        "Density": {"test": 50.0, "sentence": 25.0, "another": 25.0},
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.index.name = "Keyword"
    # Ensure the expected DataFrame is sorted the same way as the function's output
    expected_df = expected_df.sort_values("Frequency", ascending=False)

    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_empty_string(mock_nlp):
    """
    Tests analyze_text_words with an empty input string.
    """
    # Arrange
    text = ""
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = []  # Empty text should result in no tokens
    mock_nlp.return_value = mock_doc

    # Act
    df = analyze_text_words(text)

    # Assert
    # An empty DataFrame with the correct column types and index name
    expected_df = pd.DataFrame({"Frequency": pd.Series(dtype=int), "Density": pd.Series(dtype=float)})
    expected_df.index.name = "Keyword"
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_only_stopwords_punctuation(mock_nlp):
    """
    Tests analyze_text_words with text containing only stop words and punctuation.
    """
    # Arrange
    text = "This is a. The, and"
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = [
        MockToken("this", is_stop=True),
        MockToken("be", is_stop=True),
        MockToken("a", is_stop=True),
        MockToken(".", is_punct=True),
        MockToken("the", is_stop=True),
        MockToken(",", is_punct=True),
        MockToken("and", is_stop=True),
    ]
    mock_nlp.return_value = mock_doc

    # Act
    df = analyze_text_words(text)

    # Assert
    expected_df = pd.DataFrame({"Frequency": pd.Series(dtype=int), "Density": pd.Series(dtype=float)})
    expected_df.index.name = "Keyword"
    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_case_punctuation_lemmatization(mock_nlp):
    """
    Tests analyze_text_words's handling of mixed case, punctuation, and lemmatization.
    """
    # Arrange
    text = "Running, ran, RUNS. Apple, apples."
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = [
        MockToken("run", is_stop=False, is_punct=False),  # From "Running"
        MockToken(",", is_punct=True),
        MockToken("run", is_stop=False, is_punct=False),  # From "ran"
        MockToken(",", is_punct=True),
        MockToken("run", is_stop=False, is_punct=False),  # From "RUNS"
        MockToken(".", is_punct=True),
        MockToken("apple", is_stop=False, is_punct=False),  # From "Apple"
        MockToken(",", is_punct=True),
        MockToken("apple", is_stop=False, is_punct=False),  # From "apples"
        MockToken(".", is_punct=True),
    ]
    mock_nlp.return_value = mock_doc

    # Act
    df = analyze_text_words(text)

    # Assert
    expected_data = {
        "Frequency": {"run": 3, "apple": 2},
        "Density": {"run": 60.0, "apple": 40.0},
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.index.name = "Keyword"
    expected_df = expected_df.sort_values("Frequency", ascending=False)

    pd.testing.assert_frame_equal(df, expected_df)


def test_analyze_text_words_empty_lemma_after_strip(mock_nlp):
    """
    Tests analyze_text_words with tokens whose lemma becomes empty after stripping whitespace.
    These should be filtered out.
    """
    # Arrange
    text = "  \n\t"  # Text that might produce tokens with only whitespace lemmas
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = [
        MockToken(" ", is_stop=False, is_punct=False),  # Lemma is " ", strip() makes it ""
        MockToken("\n", is_stop=False, is_punct=False),  # Lemma is "\n", strip() makes it ""
    ]
    mock_nlp.return_value = mock_doc

    # Act
    df = analyze_text_words(text)

    # Assert
    expected_df = pd.DataFrame({"Frequency": pd.Series(dtype=int), "Density": pd.Series(dtype=float)})
    expected_df.index.name = "Keyword"
    pd.testing.assert_frame_equal(df, expected_df)
