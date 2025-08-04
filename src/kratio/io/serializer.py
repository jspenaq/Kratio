from pathlib import Path

import pandas as pd
from loguru import logger


class Serializer:
    """
    Handles serialization of Pandas DataFrames to various formats.
    """

    def serialize(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Serializes a DataFrame to the specified output path based on file extension.

        Args:
            df (pd.DataFrame): The DataFrame to serialize.
            output_path (str): The path to the output file (e.g., "output.csv", "output.json").
        """
        file_extension = Path(output_path).suffix.lower()

        if file_extension == ".csv":
            df.to_csv(output_path, index=True)
            logger.info(f"DataFrame successfully dumped to {output_path} (CSV format).")
        elif file_extension == ".json":
            df.to_json(output_path, orient="records", indent=4)
            logger.info(f"DataFrame successfully dumped to {output_path} (JSON format).")
        else:
            logger.error(f"Unsupported output format: {file_extension}. Please use .csv or .json.")
