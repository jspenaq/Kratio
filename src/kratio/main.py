import argparse
from pathlib import Path

from loguru import logger

from kratio.analyzer import analyze_text_noun_chunks, analyze_text_words
from kratio.constants import ANALYSIS_TYPE_NOUN_CHUNKS, ANALYSIS_TYPE_WORDS
from kratio.file_handler import read_text_file
from kratio.utils import display_top_keywords
from kratio.visualizer import visualize_top_keywords


def main() -> None:
    """
    Main function to run the Kratio keyword density analyzer.
    """
    # Configure loguru to log to a file
    logger.add("logs/kratio.log", rotation="5 MB", level="INFO")

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Analyze keyword density in a text file.")
    parser.add_argument("file_path", type=str, help="The path to the text file.")
    parser.add_argument(
        "--analysis_type",
        type=str,
        default=ANALYSIS_TYPE_WORDS,
        choices=[ANALYSIS_TYPE_WORDS, ANALYSIS_TYPE_NOUN_CHUNKS],
        help=(
            f"The type of analysis to perform ("
            f"{ANALYSIS_TYPE_WORDS} or {ANALYSIS_TYPE_NOUN_CHUNKS}, "
            f"default: {ANALYSIS_TYPE_WORDS})."
        ),
    )
    parser.add_argument(
        "--top_n",
        type=int,
        default=10,
        help="The number of top keywords/noun chunks to display (default: 10).",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path to dump the DataFrame (CSV or JSON format).",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Read the text file
    text = read_text_file(args.file_path)

    if text:
        # Analyze the text using a ternary operator as suggested by ruff SIM108
        df = analyze_text_words(text) if args.analysis_type == ANALYSIS_TYPE_WORDS else analyze_text_noun_chunks(text)

        display_top_keywords(df, args.top_n)
        # Visualize the top keywords
        visualize_top_keywords(df, args.top_n, args.analysis_type)

        # Dump DataFrame to file if --output is specified
        if args.output:
            output_path = args.output
            file_extension = Path(output_path).suffix.lower()
            # The keyword/noun chunk is in the DataFrame's index
            if file_extension == ".csv":
                df.to_csv(output_path, index=True)
                logger.info(f"DataFrame successfully dumped to {output_path} (CSV format).")
            elif file_extension == ".json":
                df.to_json(output_path, orient="records", indent=4)
                logger.info(f"DataFrame successfully dumped to {output_path} (JSON format).")
            else:
                logger.error(f"Unsupported output format: {file_extension}. Please use .csv or .json.")


if __name__ == "__main__":
    main()
