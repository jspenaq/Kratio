import json
import os
import tempfile
from pathlib import Path

import pandas as pd

from kratio.core.analyzer import analyze_text_words
from kratio.io.serializer import Serializer


def test_serialization_to_different_formats():
    # Arrange
    sample_text = "This is a sample text for testing serialization. This text contains multiple words for analysis."
    df = analyze_text_words(sample_text)

    serializer = Serializer()

    # Create temporary output files
    temp_dir = tempfile.gettempdir()
    csv_output_path = Path(temp_dir) / "output_test.csv"
    json_output_path = Path(temp_dir) / "output_test.json"

    try:
        # Act - CSV serialization
        serializer.serialize(df, str(csv_output_path))

        # Assert - CSV
        assert csv_output_path.exists()
        df_csv = pd.read_csv(csv_output_path)
        assert not df_csv.empty
        assert "WordFrequency" in df_csv.columns
        assert "WordDensity" in df_csv.columns

        # Act - JSON serialization
        serializer.serialize(df, str(json_output_path))

        # Assert - JSON
        assert json_output_path.exists()
        with open(json_output_path) as f:
            json_data = json.load(f)
        assert isinstance(json_data, list)
        assert len(json_data) > 0
        assert "WordFrequency" in json_data[0]
        assert "WordDensity" in json_data[0]

        # Test error handling for unsupported format
        unsupported_path = Path(temp_dir) / "output_test.xyz"
        serializer.serialize(df, str(unsupported_path))

    finally:
        # Clean up temporary files
        if csv_output_path.exists():
            os.unlink(csv_output_path)
        if json_output_path.exists():
            os.unlink(json_output_path)
