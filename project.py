import argparse
import logging

logger = logging.getLogger("ProjectStarter")


def setup_logging(verbose, silent):
    log_level = logging.DEBUG if verbose else logging.INFO

    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")

    if not silent:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        logger.addHandler(stream_handler)


def main(args):
    print("Hello, World!")


def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Set logging level to DEBUG.")
    return parser.parse_args(argv[1:])


if __name__ == "__main__":
    args = parse_command_line(sys.argv)
    main(args)

