"""
Get more information on a template.
"""
import argparse


def run(args):
    """
    Run the info command.
    :param args: Arguments passés à la commande
    """
    return


def parse(prog, args):
    """
    Parse les arguments passés à la commande info
    :param prog: Nom du programme
    :param args: Arguments passés à la commande
    """
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    return parser.parse_args(args)
