import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

from kratio.constants import ANALYSIS_TYPE_WORDS
from kratio.core.analyzer import analyze_text_noun_chunks, analyze_text_words
from kratio.exceptions import FileProcessingError, OutputDirectoryError
from kratio.io.file_handler import read_text_file
from kratio.io.serializer import Serializer
from kratio.utils.utils import display_top_keywords
from kratio.visualization.visualizer import (
    display_plot,
    persist_plot,
    visualize_top_keywords,
)


def _validate_output_path(file_path: str | Path) -> None:
    """
    Validates if the parent directory of the given file path exists and is writable.
    If the directory does not exist, it attempts to create it.
    Raises OutputDirectoryError if validation or creation fails.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    output_dir = file_path.parent
    if output_dir:  # Only check if there's a parent directory specified
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise OutputDirectoryError(f"Could not create output directory '{output_dir}': {e}") from e
        if not os.access(output_dir, os.W_OK):
            raise OutputDirectoryError(f"Output directory '{output_dir}' is not writable.")


class KratioController:
    """
    Orchestrates the analysis, presentation, and serialization of keyword density.
    """

    def __init__(self, serializer: Serializer) -> None:
        self.serializer = serializer

    def run_analysis(self, args: "argparse.Namespace") -> None:
        """
        Runs the keyword density analysis based on parsed arguments.

        Args:
            args: An argparse.Namespace object containing the parsed arguments.
        """
        text = read_text_file(args.file_path)  # FileReadError will propagate from here

        df = analyze_text_words(text) if args.analysis_type == ANALYSIS_TYPE_WORDS else analyze_text_noun_chunks(text)

        # Display results based on format, unless silent mode is active
        if not args.silent:
            display_top_keywords(df, args.top_n, args.format)
        else:
            # If silent, but output file is specified, still serialize
            if args.output:
                try:
                    _validate_output_path(args.output)
                    self.serializer.serialize(df, args.output)
                except (OSError, OutputDirectoryError) as e:
                    raise FileProcessingError(f"Error serializing output to {args.output}: {e}") from e
            # If silent and no output file, still log formatted keywords for internal use/debugging
            # without printing to console. This ensures data is processed even if not displayed.
            else:
                # This will prevent any console output from display_top_keywords
                # but still allow the data to be processed and potentially logged internally.
                # We need to ensure that _log_formatted_keywords is not called if silent is true
                # and no output file is specified.
                # The current implementation of display_top_keywords already handles this.
                pass

        if not args.no_visualization:
            fig = visualize_top_keywords(df, args.top_n, args.analysis_type)
            if args.save_plot:
                try:
                    _validate_output_path(args.save_plot)
                    persist_plot(fig, args.save_plot)
                except (OSError, OutputDirectoryError) as e:
                    raise FileProcessingError(f"Error saving plot to {args.save_plot}: {e}") from e
            else:
                display_plot(fig)

        if (
            args.output and not args.silent
        ):  # Only serialize if output is specified and not in silent mode (already handled above for silent mode)
            try:
                _validate_output_path(args.output)
                self.serializer.serialize(df, args.output)
            except (OSError, OutputDirectoryError) as e:
                raise FileProcessingError(f"Error serializing output to {args.output}: {e}") from e
