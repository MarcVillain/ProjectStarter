import subprocess

import jinja2

from projectstarter.utils import logger, templates, io


def parse_commands(data):
    """
    Parse the "commands" fields by propagating them from the leaves to the root of the data tree.
    :param data: The data tree to use
    :return: None. The data is edited in place.
    """
    commands = None

    for k, v in data.items():
        # Propagate the commands from the leaves to the root
        if isinstance(v, dict):
            parse_commands(v)

        # Retrieve the commands field
        if k == "commands":
            commands = v

    # If we have a commands field, parse it with the current context
    if commands is not None:
        parsed_commands = []

        for command in commands:
            logger.debug(f"parsing command: {command}")
            try:
                out = templates.parse_string(command, data)

                # Since the above returns a string, we need to parse it
                # if it is a list (starting with [ and ending with ])
                if out[0] == "[" and out[-1] == "]":
                    parsed_commands += io.yaml_load_str(out)
                else:
                    parsed_commands.append(out)

            except jinja2.exceptions.UndefinedError as e:
                # In case the value is undefined, it means the command
                # should not be executed
                logger.debug(f"jinja2 undefined error: {e}")
                pass

        data["commands"] = parsed_commands


def run_commands(commands, working_directory):
    """
    Run the given list of commands in the given folder.
    :param commands: List of commands to execute
    :param working_directory: Path to the folder where the commands should be executed
    :return: 0 on success, 1 on error.
    """
    for command in commands:
        logger.info(f"Running command '{command}'")
        with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=working_directory,
                shell=True,
        ) as p:
            try:
                stdout, stderr = p.communicate()
                logger.debug(stdout.decode("utf-8"))
                ret_val = p.returncode
                if ret_val != 0:
                    logger.error(f"Commands execution failed with error code {ret_val}")
                    logger.error(stderr)
            except Exception as e:
                p.kill()
                raise e
