import os
import shutil
from collections import OrderedDict

import jinja2
import yaml

import config
from utils import io, logger


def _prepare_jenv(jenv):
    jenv.globals["which"] = shutil.which


def parse_string(string, data):
    jenv = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(string)
    _prepare_jenv(jenv)
    return jenv.render(**data)


def parse_yaml(yaml_string, data):
    parsed_yaml = parse_string(yaml_string, data)
    return yaml.load(parsed_yaml, Loader=yaml.FullLoader)


def parse(path, data):
    logger.debug(f"Parsing '{path}'")
    loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(path))

    jenv = jinja2.Environment(loader=loader)
    _prepare_jenv(jenv)

    template = jenv.get_template(os.path.basename(path))
    return template.render(**data)


def metadata(name, data=None):
    if data is None:
        data = {}

    metadata_path = os.path.join(config.templates_folder, name, "metadata.yml")

    template_metadata = io.yaml_load(metadata_path)
    if template_metadata is None:
        logger.warning(f"template '{name}' missing or empty 'metadata.yml' file")
        return None

    return template_metadata


def all():
    templates = {}
    for template in os.listdir(config.templates_folder):
        template_metadata = metadata(template)
        if template_metadata is not None:
            templates[template] = template_metadata

    # Order by template name (keys)
    templates = OrderedDict(sorted(templates.items()))

    return templates
