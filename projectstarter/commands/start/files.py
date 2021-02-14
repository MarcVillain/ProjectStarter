import os

from projectstarter import config
from projectstarter.utils import logger, files, templates


def _create_destination_folder(path, force=False):
    """
    Create a folder at the given path.
    :param path: Path of the folder to create
    :param force: Should the folder be removed if it already exists
    """
    # Try to create the folder
    if files.mkdir(path) is False:
        # On fail, if not force, display an error message
        if not force:
            logger.error(
                "Destination folder already exists. You can force its removal with the --force option."
            )
            raise Exception("Destination folder already exists")

        # Else, remove the old folder and create a new one
        logger.warning(f"Force option set: removing folder '{path}'")
        files.rm(path)

        if files.mkdir(path) is False:
            logger.error("Something went wrong when trying to create destination folder.")
            raise Exception("Something went wrong")


def copy_template_files(template_name, data, output_path):
    """
    Copy the template's files to the output folder path
    and replace its content with the provided data.
    :param template_name: The name of the template to copy from
    :param data: The data to use for Jinja2 completion
    :param output_path: The output folder path
    """
    _create_destination_folder(output_path)

    # List files to copy over
    files_to_copy = data.get("files", [])
    for option, value in data.get("options", {}).items():
        files_to_copy += value.get("files", [])
    logger.debug(f"Files to copy: {files_to_copy}")

    # Expand folders paths
    paths_to_copy = {}
    for file in files_to_copy:
        template_folder = os.path.join(config.templates_folder, template_name)
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
