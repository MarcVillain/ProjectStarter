import os
import sys

import yaml


def yaml_load(file_path):
    """
    Load (read) a Yaml file content.
    :param file_path: Path to the file to read
    :returns: Dictionary matching the Yaml file's content
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def yaml_dump(content, stream=sys.stdout):
    """
    Dump (write) a Yaml content to stream.
    :param content: Yaml string
    :param stream: Stream to dump the Yaml string to
    """
    yaml.dump(content, stream=stream, default_flow_style=False)
