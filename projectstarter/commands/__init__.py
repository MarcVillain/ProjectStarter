import argparse
import importlib
import math
import pkgutil
import sys

import projectstarter
from projectstarter._version import __version__
from projectstarter.utils import logger


def _extract_commands():
    """
    Get list of commands from 'commands' module.
    :returns: List of string of command's name
    """
    module_names = [
        module.name for module in pkgutil.iter_modules(projectstarter.commands.__path__)
    ]
    commands = {}
    for module_name in module_names:
        module = importlib.import_module(f"projectstarter.commands.{module_name}")
        if module.__doc__ is not None:
            commands[module_name] = {
                "description": module.__doc__.strip().lower(),
                "func_parse": module.__getattribute__("parse"),
                "func_run": module.__getattribute__("run"),
            }
    return commands


def _build_usage_and_desc(commands):
    """
    Generate usage string.
    :param commands: List of available commands
    :returns: Tuple(usage string, description string)
    """
    # Build usage
    usage = "project [-h] [-v] [-V] <command> [options]"

    # Build description
    description = "Generate project templates."
    if len(commands) > 0:
        description += "\n\navailable commands:"
        command_max_len = 4 * math.ceil(len(max(commands.keys(), key=len)) / 4)
        for command_name, command in commands.items():
            command_name = command_name.ljust(command_max_len)
            command_desc = command["description"]
            description += f"\n    {command_name}{command_desc}"

    return usage, description


def parse():
    """
    Parse tous les arguments passés au CLI.
    """
    # Get CLI information
    commands = _extract_commands()
    usage, description = _build_usage_and_desc(commands)

    # Build parser
    parser = argparse.ArgumentParser(
        usage=usage,
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="set logging level to DEBUG",
    )
    parser.add_argument("command", help="command to run")

    # Parse arguments
    first_not_option_arg_pos = len(sys.argv)
    for i, arg in enumerate(sys.argv[1:]):
        if arg[0] != "-":
            first_not_option_arg_pos = i + 2
            break

    args = parser.parse_args(sys.argv[1:first_not_option_arg_pos])

    # Set logging level
    logger.setup(args.verbose)

    # Check if command is valid
    if args.command not in commands:
        logger.info(
            f"project: '{args.command}' is not a project starter command. See 'project --help'."
        )
        return 1

    # Dispatch command call
    cmd_args = commands[args.command]["func_parse"](
        f"{sys.argv[0]} {args.command}", sys.argv[first_not_option_arg_pos:]
    )
    return commands[args.command]["func_run"](cmd_args)
