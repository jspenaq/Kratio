import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

from kratio.constants import ANALYSIS_TYPE_WORDS, SUPPORTED_EXTENSIONS
from kratio.core.analyzer import analyze_text_noun_chunks, analyze_text_words
from kratio.exceptions import FileProcessingError, FileReadError, OutputDirectoryError
from kratio.io.file_handler import (
    get_files_from_directory,
    is_directory,
    read_text_file,
)
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

    def _process_file(self, file_path: Path, args: "argparse.Namespace") -> None:
        """
        Processes a single file for keyword density analysis.
        """
        try:
            text = read_text_file(file_path)
            df = (
                analyze_text_words(text)
                if args.analysis_type == ANALYSIS_TYPE_WORDS
                else analyze_text_noun_chunks(text)
            )

            if not args.silent:
                display_top_keywords(df, args.top_n, args.format)

            if args.output:
                _validate_output_path(args.output)
                self.serializer.serialize(df, args.output)

            if not args.no_visualization:
                fig = visualize_top_keywords(df, args.top_n, args.analysis_type)
                if args.save_plot:
                    _validate_output_path(args.save_plot)
                    persist_plot(fig, args.save_plot)
                else:
                    display_plot(fig)

        except FileReadError as e:
            raise FileProcessingError(f"Error reading file {file_path}: {e}") from e

    def run_analysis(self, args: "argparse.Namespace") -> None:
        """
        Runs the keyword density analysis based on parsed arguments.
        """
        if is_directory(args.path):
            files = get_files_from_directory(args.path, SUPPORTED_EXTENSIONS)
            if not files:
                raise FileProcessingError(f"No supported files found in directory '{args.path}'.")
            for file in files:
                self._process_file(file, args)
        else:
            self._process_file(Path(args.path), args)
