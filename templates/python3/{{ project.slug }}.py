{% if options.cli %}import argparse{% endif %}
{% if options.logging %}import logging{% endif %}
{% if options.logging %}import sys{% endif %}
{% if options.logging %}
logger = logging.getLogger("{{ project.slug }}")


def setup_logging(verbose, silent):
    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)

    if not silent:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        logger.addHandler(stream_handler)
{% endif %}

def main(args):
    print("Running project {{ project.slug }}")

{% if options.cli %}
def parse_command_line(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Set logging level to DEBUG.")
    parser.add_argument("-s", "--silent", action="store_true", help="Remove logging in STDOUT.")
    return parser.parse_args(argv[1:])
{% endif %}

if __name__ == "__main__":
    {% if options.cli %}args = parse_command_line(sys.argv){% else %}args = []{% endif %}
    main(args)

