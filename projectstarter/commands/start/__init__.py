"""
Generate a project from a template
"""
import argparse
import os
import re
import subprocess

import jinja2
import yaml
from slugify import slugify

from projectstarter import config
from projectstarter.utils import templates
from projectstarter.utils import files, logger


def _parse_command(command, data):
    """
    Parse a single string command using the given data.
    :param command: Command to parse
    :param data: Data to give to the parser
    :return: List of extracted commands
    """
    logger.debug(f"parsing command: {type(command)}: {command}")
    commands = []

    # Parse a list of commands
    if isinstance(command, list):
        for cmd in command:
            commands += _parse_command(cmd, data)
    elif command[0] == "[":
        commands += _parse_command(yaml.load(command, Loader=yaml.FullLoader), data)

    # Parse a Jinja2 formatted command
    elif ("{{" in command and "}}" in command) or (
            "{%" in command and "%}" in command
    ):
        try:
            command_str = templates.parse_string(command, data)
            commands += _parse_command(command_str, data)
        except jinja2.exceptions.UndefinedError as e:
            # In case the value is undefined, it means the command
            # should not be executed
            logger.debug(f"jijna2 undefined error: {e}")
            pass

    # Parse a regular command
    else:
        commands.append(command)

    return commands


def parse_commands(data):
    """
    Parse the data["commands"] using the data.
    :param data: The data to use
    :return: The parsed data
    """
    parsed_commands = []
    for command in data.get("commands", []):
        parsed_commands += _parse_command(command, data)
    return parsed_commands


def _retrieve_options(patterns, options_tree):
    """
    Recursive iteration on nested options. If an option matches one of
    the given names, it is added to the list of returned options.
    :param patterns: List of the options patterns to look for (separated with config.options_sep if nested)
    :param options_tree: The options dictionary tree
    :return: Dictionary of key/value options that matched the given names. None on error.
    """
    # Names example:
    # [foo, foo:bar]

    # Options dictionary tree example:
    # {
    # options: {
    #   foo: {
    #     options: {
    #       bar: { ... }
    #     }
    #   }
    # }

    # Stop recursion
    if len(patterns) == 0:
        return {}

    options = {}

    # For each option
    for name, value in options_tree.get("options", {}).items():
        # For each pattern
        for pattern in patterns:
            try:
                if config.options_sep not in pattern:
                    # Handle simple option
                    if re.match(pattern, name):
                        # No need for nested options on match
                        if "options" in value.keys():
                            value.pop("options")
                        # Add option in options list
                        options[name] = value
                else:
                    # Handle nested option
                    if re.match(pattern.split(config.options_sep)[0], name):
                        # Move patterns one option forward
                        new_patterns = [
                            re.sub(r"^.*?" + config.options_sep, "", p)
                            for p in patterns
                            if config.options_sep in p
                        ]
                        # Get nested options
                        new_options = _retrieve_options(new_patterns, value)
                        if new_options is None:
                            return None
                        # Prefix keys with current name
                        new_options = {
                            f"{name}": v
                            for k, v in new_options.items()
                        }
                        # Add new items to resulting options
                        options = {**options, **new_options}
            except re.error as e:
                logger.error(f"option pattern '{pattern}' is invalid: {e}")
                return None

    return options


def run(args):
    """
    Run the command.
    :param args: Arguments given to the command
    """
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
        logger.error("The template folder is missing its metadata file.")
        return 1

    # Keep only requested options
    if "options" in template_metadata:
        options = _retrieve_options(args.options, template_metadata)
        if options is None:
            return 1

        # Display unmatched options
        option_has_not_matched = False
        for option in args.options:
            if option.split(config.options_sep)[0] not in options.keys():
                option_has_not_matched = True
                logger.error(f"Option pattern '{option}' did not match anything.")
        if option_has_not_matched:
            return 1

        template_metadata["options"] = options

    # Complete parse data
    data = {**data, **template_metadata}
    logger.debug(f"Data: {data}")

    # Parse commands
    commands = parse_commands(data)
    logger.debug(f"Commands: {commands}")

    # Create destination folder
    if files.mkdir(output_path) is False:
        if not args.force:
            logger.error(
                "Destination folder already exists. You can force its removal with the --force option."
            )
            return 1
        logger.warning(f"Force option set: removing folder '{output_path}'")
        files.rm(output_path)
        if files.mkdir(output_path) is False:
            logger.error("Something went wrong when trying to create destination folder.")
            return 1

    # List files to copy over
    files_to_copy = template_metadata.get("files", [])
    for option, value in template_metadata.get("options", {}).items():
        files_to_copy += value.get("files", [])
    logger.debug(f"Files to copy: {files_to_copy}")

    # Expand folders
    paths_to_copy = {}
    for file in files_to_copy:
        template_folder = os.path.join(config.templates_folder, args.template)
        path = os.path.join(template_folder, file)
        if os.path.isdir(path):
            for path in files.all_in(path):
                dest_path = path.replace(f"{template_folder}", output_path)
                paths_to_copy[path] = templates.parse_string(dest_path, data).replace(
                    ".j2", ""
                )
        else:
            dest_path = path.replace(f"{template_folder}", output_path)
            paths_to_copy[path] = templates.parse_string(dest_path, data).replace(
                ".j2", ""
            )
    logger.debug(f"Paths to copy: {paths_to_copy}")

    # Parse and copy files to destination
    logger.info(f"Creating project '{project_name}'")
    for src, dst in paths_to_copy.items():
        # Retrieve destination folder
        logger.debug(src, "-->", dst)
        # Ensure destination folder exists
        files.mkdir(os.path.dirname(dst), ignore_errors=True)
        # Parse content
        content = templates.parse(src, data)
        # Write to file
        with open(dst, "w") as f:
            f.write(content)

    # Execute chained commands in output folder
    for command in commands:
        logger.info(f"Running command '{command}'")
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=output_path,
            shell=True,
        ) as p:
            try:
                stdout, stderr = p.communicate()
                logger.debug(stdout.decode("utf-8"))
                ret_val = p.returncode
                if ret_val != 0:
                    logger.error(f"Commands execution failed with error code {ret_val}")
                    logger.error(stderr)
            except:
                p.kill()
                return 1

    # Success message
    logger.info(f"Project created at '{output_path}'")
    logger.info(f"Run `grep -R FIXME '{output_path}'` to complete the setup")


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
        help=f"options to activate (nested options are accessible by using the '{config.options_sep}' separator)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="erase destination directory if it exists",
    )
    return parser.parse_args(args)
