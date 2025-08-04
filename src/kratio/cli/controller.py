from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

from kratio.constants import ANALYSIS_TYPE_WORDS
from kratio.core.analyzer import analyze_text_noun_chunks, analyze_text_words
from kratio.io.file_handler import read_text_file
from kratio.io.serializer import Serializer
from kratio.utils.utils import display_top_keywords
from kratio.visualization.visualizer import (
    display_plot,
    persist_plot,
    visualize_top_keywords,
)


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
        text = read_text_file(args.file_path)

        if text:
            df = (
                analyze_text_words(text)
                if args.analysis_type == ANALYSIS_TYPE_WORDS
                else analyze_text_noun_chunks(text)
            )

            # Display results based on format, unless silent mode is active
            if not args.silent:
                display_top_keywords(df, args.top_n, args.format)
            else:
                # If silent, but output file is specified, still serialize
                if args.output:
                    self.serializer.serialize(df, args.output)
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
                    persist_plot(fig, args.save_plot)
                else:
                    display_plot(fig)

            if args.output:
                self.serializer.serialize(df, args.output)
