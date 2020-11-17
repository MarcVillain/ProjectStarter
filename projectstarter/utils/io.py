import os

import yaml


def yaml_load(file_path):
    """
    Load (read) a Yaml file content.
    :param file_path: Path to the file to read
    :returns: Dictionnary matching the Yaml file's content
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
