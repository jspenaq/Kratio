import argparse

from kratio.constants import ANALYSIS_TYPE_NOUN_CHUNKS, ANALYSIS_TYPE_WORDS


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the Kratio keyword density analyzer.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Analyze keyword density in a text file or directory.")
    parser.add_argument(
        "path",
        type=str,
        help="The path to the text file or directory to analyze.",
    )
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
    parser.add_argument(
        "--save-plot",
        type=str,
        help="Path to save the visualization plot (e.g., path.png).",
    )
    parser.add_argument(
        "--no-visualization",
        action="store_true",
        help="Disable visualization output.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="table",
        choices=["json", "csv", "table"],
        help="Output format for the analysis results (json, csv, or table, default: table).",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress all non-essential output, including logging messages.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Monitor the file or directory and re-run analysis on every change.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging for troubleshooting.",
    )
    return parser.parse_args()
