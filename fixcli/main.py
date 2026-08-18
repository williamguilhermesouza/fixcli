import argparse

from fixcli.application import Application
from fixcli.config import Config

def main():
    args = parse_args()
    config = Config(args.mode, args.verbose, args.config)
    application = Application(config)
    application.start()

def parse_args():
    parser = argparse.ArgumentParser(
        prog="FixCli",
        description="Fix Protocol Cli tool. Use it to spawn fix initiators (clients) or acceptors (servers)",
    )

    subparser = parser.add_subparsers(dest="mode", required=True)

    initiator_parser = subparser.add_parser("initiator", help="Create a fix initiator")
    acceptor_parser = subparser.add_parser(
        "acceptor", help="Create a fix acceptor (default)"
    )

    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=str,
        help="Path to session configuration file",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
