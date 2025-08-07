import pandas as pd
import pytest

from src.kratio.utils.data_utils import normalize_to_dataframe


def test_normalize_to_dataframe_empty_counts():
    """
    Test case for when total_items is 0, ensuring an empty DataFrame is returned
    with correct columns and index name.
    """
    counts = pd.Series(dtype=int)
    total_items = 0
    index_name = "TestIndex"
    column_prefix = "Test"

    df = normalize_to_dataframe(counts, total_items, index_name, column_prefix)

    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == ["TestFrequency", "TestDensity"]
    assert df.index.name == index_name


def test_normalize_to_dataframe_with_data():
    """
    Test case for when total_items is not 0, ensuring correct frequency and density
    calculations and DataFrame structure.
    """
    counts = pd.Series({"a": 10, "b": 20, "c": 30})
    total_items = 60
    index_name = "Word"
    column_prefix = "Word"

    df = normalize_to_dataframe(counts, total_items, index_name, column_prefix)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["WordFrequency", "WordDensity"]
    assert df.index.name == index_name

    # Verify calculations
    assert df.loc["a", "WordFrequency"] == 10
    assert df.loc["a", "WordDensity"] == pytest.approx(16.666666666666664)
    assert df.loc["b", "WordFrequency"] == 20
    assert df.loc["b", "WordDensity"] == pytest.approx(33.33333333333333)
    assert df.loc["c", "WordFrequency"] == 30
    assert df.loc["c", "WordDensity"] == pytest.approx(50.0)

    # Verify sorting
    assert list(df.index) == ["c", "b", "a"]
