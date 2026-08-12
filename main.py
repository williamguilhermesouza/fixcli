import logging
import argparse
import sys

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        handlers=[logging.FileHandler("fixcli.log"), logging.StreamHandler(sys.stdout)],
        format="%(levelname)s %(asctime)s %(message)s",
        level=logging.DEBUG,
    )

    parser = argparse.ArgumentParser(
        description="Fix Protocol Cli tool. Use it to spawn fix initiators (clients) or acceptors (servers)"
    )
    parser.add_argument(
        "-i", "--initiator", action="store_true", help="Create a fix initiator"
    )
    parser.add_argument(
        "-a", "--acceptor", action="store_true", help="Create a fix acceptor (default)"
    )
    parser.add_argument(
        "-c", "--config", type=str, help="Path to session configuration file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.info("Debug mode enabled")


if __name__ == "__main__":
    main()
