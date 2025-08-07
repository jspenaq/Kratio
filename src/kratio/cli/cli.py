import sys
import time
from pathlib import Path

from loguru import logger

from kratio.cli.cli_parser import parse_arguments
from kratio.cli.controller import KratioController
from kratio.exceptions import FileProcessingError, FileReadError, OutputDirectoryError
from kratio.io.serializer import Serializer
from kratio.utils.logging_config import setup_logging
from kratio.utils.watch import FileWatcher


def main() -> None:
    """
    Main function to run the Kratio keyword density analyzer.
    Acts as the composition root for the application.
    """
    try:
        args = parse_arguments()
        # Set logging level based on debug flag
        log_level = "DEBUG" if hasattr(args, "debug") and args.debug else "INFO"
        setup_logging(silent=args.silent, level=log_level)

        serializer = Serializer()
        controller = KratioController(serializer=serializer)

        if args.watch:
            # In watch mode, automatically disable visualization unless explicitly enabled
            if not hasattr(args, "watch_with_visualization") or not args.watch_with_visualization:
                args.no_visualization = True

            logger.info(f"Starting watch mode for {args.path}")
            logger.debug(f"Watch mode arguments: {vars(args)}")

            # Create a file watcher
            watcher = FileWatcher()

            # Define callback function for file changes
            def on_file_change(file_path: Path) -> None:
                logger.info(f"Re-analyzing {file_path}")
                # Create a copy of args with the updated path
                import copy

                file_args = copy.deepcopy(args)
                file_args.path = str(file_path)
                # Ensure watch flag is set in the copied args
                file_args.watch = True
                logger.debug(f"File change callback with path: {file_path}")
                try:
                    controller.run_analysis(file_args)
                except FileReadError as e:
                    logger.error(f"Error reading file during re-analysis: {e}")
                    logger.info("Continuing to watch for changes...")
                except FileProcessingError as e:
                    logger.error(f"Error processing file during re-analysis: {e}")
                    logger.info("Continuing to watch for changes...")
                except OutputDirectoryError as e:
                    logger.error(f"Output directory error during re-analysis: {e}")
                    logger.info("Continuing to watch for changes...")
                except Exception as e:
                    logger.error(f"Unexpected error during re-analysis: {e}")
                    logger.info("Continuing to watch for changes...")

            try:
                # Start watching the specified path
                watcher.start_watching(args.path, on_file_change)

                # Run initial analysis
                try:
                    controller.run_analysis(args)
                except (FileReadError, FileProcessingError, OutputDirectoryError) as e:
                    logger.error(f"Error during initial analysis: {e}")
                    logger.info("Continuing to watch for changes...")

                # Keep the main thread alive
                logger.info("Watching for changes. Press Ctrl+C to stop.")
                logger.info("When you modify the file, it will be automatically re-analyzed.")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    raise  # Re-raise to be caught by outer try/except

            except FileNotFoundError as e:
                logger.error(f"Watch error: {e}")
                logger.error("Cannot start watch mode on a non-existent path.")
                sys.exit(4)  # Specific exit code for watch mode errors
            except KeyboardInterrupt:
                logger.info("Watch mode interrupted by user.")
                watcher.stop_watching()
                sys.exit(130)  # Exit code for KeyboardInterrupt
            except Exception as e:
                logger.exception(f"Unexpected error in watch mode: {e}")
                watcher.stop_watching()
                sys.exit(5)  # Specific exit code for unexpected watch mode errors
        else:
            # Normal mode - run once and exit
            controller.run_analysis(args)
            sys.exit(0)  # Exit successfully
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user.")
        sys.exit(130)  # Exit code for KeyboardInterrupt
    except FileReadError as e:
        logger.error(f"Error reading file: {e}")
        sys.exit(1)  # Specific exit code for file read errors
    except FileProcessingError as e:
        logger.error(f"Error processing file: {e}")
        sys.exit(2)  # Specific exit code for file processing errors
    except OutputDirectoryError as e:
        logger.error(f"Output directory error: {e}")
        sys.exit(3)  # Specific exit code for output directory errors
    except Exception:
        logger.exception("An unexpected error occurred:")  # Logs the exception with stack trace
        sys.exit(99)  # Generic exit code for unexpected errors


if __name__ == "__main__":
    main()
