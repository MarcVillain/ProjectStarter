"""
Generate a project from a template
"""
import argparse
import os

from slugify import slugify

from projectstarter import config
from projectstarter.commands.start.commands import parse_commands, run_commands
from projectstarter.commands.start.files import copy_template_files
from projectstarter.commands.start.options import filter_options
from projectstarter.utils import templates
from projectstarter.utils import logger


def run(args):
    """
    Run the command.
    :param args: Arguments given to the command
    """
    # Init some useful variables
    output_path = os.path.abspath(args.output)
    project_name = os.path.basename(output_path)
    data = {
        "project": {
            "path": output_path,
            "name": project_name,
            "slug": slugify(project_name),
        },
    }

    # Load template metadata
    logger.info(f"Loading template '{args.template}'")
    template_metadata = templates.metadata(args.template)
    if template_metadata is None:
        return 1

    # Keep only requested options
    template_metadata["options"] = filter_options(args.options, template_metadata)
    if template_metadata["options"] is None:
        return 1

    # Complete data for future parsing
    data = {**data, **template_metadata}
    logger.debug(f"Data: {data}")

    # Parse commands
    parse_commands(data)
    commands = data["commands"]
    logger.debug(f"Commands: {commands}")

    logger.info(f"Creating project '{project_name}'")

    try:
        copy_template_files(args.template, data, output_path, args.force)
        run_commands(commands, output_path)
    except Exception as e:
        logger.error(e)
        return 1

    # Success message
    logger.info(f"Project created at '{output_path}'")
    logger.info(f"Run `grep -Ri FIXME '{output_path}'` to complete the setup")


def parse(prog, args):
    """
    Parse all the arguments given to the command.
    :param prog: Name of the program
    :param args: Arguments given to the command
    """
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        "template",
        help="template to use (see `project templates` for an exhaustive list)",
    )
    parser.add_argument("output", help="destination folder")
    parser.add_argument(
        "-o",
        "--options",
        metavar="OPTION",
        nargs="*",
        default=[],
        help=f"filter options to activate (nested options are accessible by using the '{config.options_sep}' separator)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="erase destination directory if it exists",
    )
    return parser.parse_args(args)
