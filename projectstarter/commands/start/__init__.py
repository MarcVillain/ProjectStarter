"""
Generate a project from a template.
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


def run(args):
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
    template_metadata = templates.metadata(args.template, data)
    if template_metadata is None:
        return

    # Keep only requested options
    if "options" in template_metadata:
        template_metadata["options"] = {
            k: v
            for k, v in template_metadata["options"].items()
            if any(True for option in args.options if re.match(option, k))
        }

    # Complete parse data
    data = {**data, **template_metadata}
    logger.debug(f"Data: {data}")

    # Create destination folder
    if files.mkdir(output_path) is False:
        if not args.force:
            return
        logger.warning(f"Force option set: remove folder '{output_path}'")
        files.rm(output_path)

    # List files to copy over
    files_to_copy = template_metadata["files"]
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
                paths_to_copy[path] = templates.parse_string(dest_path, data).replace(".j2", "")
        else:
            dest_path = path.replace(f"{template_folder}", output_path)
            paths_to_copy[path] = templates.parse_string(dest_path, data).replace(".j2", "")
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

    # Retrieve list of commands to run
    def _parse_command(command):
        commands = []
        if isinstance(command, list):
            for cmd in command:
                commands += _parse_command(cmd)
        elif command[0] == "[":
            commands += _parse_command(yaml.load(command, Loader=yaml.FullLoader))
        elif "{{" in command and "}}" in command:
            try:
                commands += _parse_command(templates.parse_string(command, data))
            except jinja2.exceptions.UndefinedError:
                # In case the value is undefined, it means the command
                # should not be executed
                pass
        else:
            commands.append(command)
        return commands

    commands = []
    for command in data.get("commands", []):
        commands += _parse_command(command)

    # Execute chained commands in output folder
    for command in commands:
        logger.info(f"Running command '{command}' in project")
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=output_path, shell=True
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
                raise

    # Success message
    logger.info(f"Project created at '{output_path}'")


def parse(prog, args):
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument("template", help="template to use (see 'project templates' for an exhaustive list)")
    parser.add_argument("output", help="destination folder")
    parser.add_argument("-o", "--options", metavar="OPTION", nargs="*", default=[], help="options to activate")
    parser.add_argument("-f", "--force", action="store_true", help="erase destination directory if it exists")
    return parser.parse_args(args)
