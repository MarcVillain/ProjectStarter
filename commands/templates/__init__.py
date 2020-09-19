"""
List all the available templates.
"""
import argparse
import re

from utils import templates as tmplts, logger


def run(args):
    templates = tmplts.all()

    max_template_name_len = max(len(name) for name in templates.keys()) + 4

    logger.info("The available templates are:")
    for name, data in templates.items():
        description = data.get("description", "").lower().strip()

        # Apply search filter
        if args.filter and not (re.match(args.filter, name) or re.match(args.filter, description)):
            continue

        name_log = name.ljust(max_template_name_len)
        description_log = description or "-"
        logger.info(f"{name_log}{description_log}", prefix="  ")


def parse(prog, args):
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        "-f",
        "--filter",
        metavar="PATTERN",
        help="filter templates based on pattern matching name or description",
    )
    return parser.parse_args(args)
