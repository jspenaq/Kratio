import argparse

from kratio.analyzer import analyze_text
from kratio.file_handler import read_text_file
from kratio.visualizer import visualize_top_keywords


def main() -> None:
    """
    Main function to run the Kratio keyword density analyzer.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Analyze keyword density in a text file.")
    parser.add_argument("file_path", type=str, help="The path to the text file.")
    parser.add_argument(
        "--top_n",
        type=int,
        default=10,
        help="The number of top keywords to display (default: 10).",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Read the text file
    text = read_text_file(args.file_path)

    if text:
        # Analyze the text
        df = analyze_text(text)

        # Visualize the top keywords
        visualize_top_keywords(df, args.top_n)


if __name__ == "__main__":
    main()
