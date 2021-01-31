"""
Get more information on a template
"""
import argparse


def run(args):
    """
    Run the command.
    :param args: Arguments given to the command
    """
    return 2


def parse(prog, args):
    """
    Parse all the arguments given to the command.
    :param prog: Name of the program
    :param args: Arguments given to the command
    """
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        "template",
        help="template to display (see `project templates` for an exhaustive list)",
    )
    return parser.parse_args(args)
