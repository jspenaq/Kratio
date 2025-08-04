import argparse
import os

from kratio.analyzer import analyze_text_noun_chunks, analyze_text_words
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
        choices=["words", "noun_chunks"],
        help="The type of analysis to perform (words or noun chunks, default: words).",
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
        df = analyze_text_words(text) if args.analysis_type == "words" else analyze_text_noun_chunks(text)

        display_top_keywords(df, args.top_n)
        # Visualize the top keywords
        visualize_top_keywords(df, args.top_n, args.analysis_type)

        # Dump DataFrame to file if --output is specified
        if args.output:
            output_path = args.output
            file_extension = os.path.splitext(output_path)[1].lower()
            # The keyword/noun chunk is in the DataFrame's index
            if file_extension == ".csv":
                df.to_csv(output_path, index=True)
                print(f"DataFrame successfully dumped to {output_path} (CSV format).")
            elif file_extension == ".json":
                df.to_json(output_path, orient="records", indent=4)
                print(f"DataFrame successfully dumped to {output_path} (JSON format).")
            else:
                print(f"Unsupported output format: {file_extension}. Please use .csv or .json.")


if __name__ == "__main__":
    main()
