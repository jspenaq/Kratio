import sys

from loguru import logger

from kratio.cli.cli_parser import parse_arguments
from kratio.cli.controller import KratioController
from kratio.exceptions import FileProcessingError, FileReadError, OutputDirectoryError
from kratio.io.serializer import Serializer
from kratio.utils.logging_config import setup_logging


def main() -> None:
    """
    Main function to run the Kratio keyword density analyzer.
    Acts as the composition root for the application.
    """
    try:
        args = parse_arguments()
        setup_logging(silent=args.silent)

        serializer = Serializer()
        controller = KratioController(serializer=serializer)

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
