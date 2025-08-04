import argparse

from kratio.analyzer import analyze_text_sentences, analyze_text_words
from kratio.file_handler import read_text_file
from kratio.utils import display_top_keywords
from kratio.visualizer import visualize_top_keywords


def main() -> None:
    """
    Main function to run the Kratio keyword density analyzer.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Analyze keyword density in a text file.")
    parser.add_argument("file_path", type=str, help="The path to the text file.")
    parser.add_argument(
        "--analysis_type",
        type=str,
        default="words",
        choices=["words", "sentences"],
        help="The type of analysis to perform (words or sentences, default: words).",
    )
    parser.add_argument(
        "--top_n",
        type=int,
        default=10,
        help="The number of top keywords/noun chunks to display (default: 10).",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Read the text file
    text = read_text_file(args.file_path)

    if text:
        # Analyze the text using a ternary operator as suggested by ruff SIM108
        df = analyze_text_words(text) if args.analysis_type == "words" else analyze_text_sentences(text)

        display_top_keywords(df, args.top_n)
        # Visualize the top keywords
        visualize_top_keywords(df, args.top_n, args.analysis_type)


if __name__ == "__main__":
    main()
