import os

import yaml


def yaml_load(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
