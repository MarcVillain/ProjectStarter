"""
Generate a project from a template.
"""
import argparse
import os
import subprocess

import yaml
from slugify import slugify

import config
from utils import templates, logger, files, io


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
    template_metadata = templates.metadata(args.template, data)
    if template_metadata is None:
        return

    # Keep only requested options
    if "options" in template_metadata:
        template_metadata["options"] = {k: v for k, v in template_metadata["options"].items() if k in args.options}

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
                subfile = path.replace(f"{template_folder}{os.path.sep}", "")
                paths_to_copy[subfile] = path
        else:
            paths_to_copy[file] = path
    logger.debug(f"Paths to copy: {paths_to_copy}")

    # Complete parse data
    data = {**data, **template_metadata}

    # Parse and copy files to destination
    for path_relative, src in paths_to_copy.items():
        # Retrieve destination folder
        dst = os.path.join(output_path, path_relative)
        dst = templates.parse_string(dst, data)
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
            commands += _parse_command(templates.parse_string(command, data))
        else:
            commands.append(command)
        return commands

    commands = []
    for command in data.get("commands", []):
        commands += _parse_command(command)

    # Execute chained commands in output folder
    for command in commands:
        logger.info(f"Running command '{command}'")
        with subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=output_path, shell=True
        ) as p:
            try:
                _, stderr = p.communicate()
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
