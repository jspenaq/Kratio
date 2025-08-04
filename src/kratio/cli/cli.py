from kratio.cli.cli_parser import parse_arguments
from kratio.cli.controller import KratioController
from kratio.io.serializer import Serializer
from kratio.utils.logging_config import setup_logging


def main() -> None:
    """
    Main function to run the Kratio keyword density analyzer.
    Acts as the composition root for the application.
    """
    args = parse_arguments()
    setup_logging(silent=args.silent)

    serializer = Serializer()
    controller = KratioController(serializer=serializer)

    controller.run_analysis(args)


if __name__ == "__main__":
    main()
