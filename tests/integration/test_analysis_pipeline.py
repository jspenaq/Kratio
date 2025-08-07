import tempfile
from argparse import Namespace
from pathlib import Path

import pandas as pd

from kratio.cli.controller import KratioController
from kratio.constants import ANALYSIS_TYPE_NOUN_CHUNKS, ANALYSIS_TYPE_WORDS
from kratio.io.serializer import Serializer


def test_complete_analysis_pipeline():
    # Arrange
    # Create a temporary text file with sample content
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as temp_file:
        temp_file.write("This is a sample text for testing. This text contains keywords and noun chunks.")
        temp_file_path = temp_file.name

    # Create a temporary output file for serialization
    temp_output_path = Path(temp_file_path).parent / "output.csv"

    # Create a mock args object similar to what would be parsed from CLI
    args = Namespace(
        path=temp_file_path,
        analysis_type=ANALYSIS_TYPE_WORDS,
        top_n=5,
        output=str(temp_output_path),
        save_plot=None,
        no_visualization=True,
        format="csv",
        silent=True,
    )
    serializer = Serializer()
    controller = KratioController(serializer=serializer)

    try:
        # Act
        controller.run_analysis(args)

        # Assert
        # Verify the output file was created
        assert temp_output_path.exists()

        # Verify the content of the output file
        df = pd.read_csv(temp_output_path)
        assert not df.empty
        assert "WordFrequency" in df.columns
        assert "WordDensity" in df.columns

        # Test with noun chunks analysis
        args.analysis_type = ANALYSIS_TYPE_NOUN_CHUNKS
        args.output = str(temp_output_path).replace(".csv", "_noun.csv")
        controller.run_analysis(args)

        # Verify noun chunks output
        noun_output_path = Path(args.output)
        assert noun_output_path.exists()
        df_noun = pd.read_csv(noun_output_path)
        assert not df_noun.empty
        assert "NounChunkFrequency" in df_noun.columns
        assert "NounChunkDensity" in df_noun.columns

    finally:
        # Clean up temporary files
        if Path(temp_file_path).exists():
            Path(temp_file_path).unlink()
        if temp_output_path.exists():
            temp_output_path.unlink()
        noun_output_path = Path(str(temp_output_path).replace(".csv", "_noun.csv"))
        if noun_output_path.exists():
            noun_output_path.unlink()
