import pandas as pd

def normalize_to_dataframe(counts: pd.Series, total_items: int, index_name: str, column_prefix: str) -> pd.DataFrame:
    """
    Normalizes counts to a DataFrame with frequencies and densities, handling empty inputs.

    Args:
        counts (pd.Series): Series of counts (e.g., word counts, noun chunk counts).
        total_items (int): Total number of items (e.g., total words, total noun chunks).
        index_name (str): Name for the DataFrame index (e.g., "Keyword", "Noun Chunk").
        column_prefix (str): Prefix for the "Frequency" and "Density" columns.

    Returns:
        pd.DataFrame: A DataFrame with frequencies and densities.
    """
    if total_items == 0:
        empty_df = pd.DataFrame({f"{column_prefix}Frequency": pd.Series(dtype=int), f"{column_prefix}Density": pd.Series(dtype=float)})
        empty_df.index.name = index_name
        return empty_df

    densities = counts / total_items * 100
    df = pd.DataFrame({f"{column_prefix}Frequency": counts, f"{column_prefix}Density": densities})
    df.index.name = index_name
    return df.sort_values(f"{column_prefix}Frequency", ascending=False)