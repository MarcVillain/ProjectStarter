import os
import shutil
from collections import OrderedDict

import jinja2
import yaml

from projectstarter import config
from projectstarter.utils import io, logger


def _prepare_jenv(jenv):
    """
    Set Jinja environment variables.
    :param jenv: Jinja's environment
    """
    jenv.globals["which"] = shutil.which


def parse_string(string, data):
    """
    Render Jinja environment from string.
    :param string: String to render
    :param data: The data to give to the renderer
    :returns: The rendered string
    """
    jenv = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(string)
    _prepare_jenv(jenv)
    return jenv.render(**data)


def parse_yaml(yaml_string, data):
    """
    Render Jinja environment from Yaml string.
    :param yaml_string: Yaml string to render
    :param data: The data to give to the renderer
    :returns: The yaml dictionary after render
    """
    parsed_yaml = parse_string(yaml_string, data)
    return yaml.load(parsed_yaml, Loader=yaml.FullLoader)


def parse(path, data):
    """
    Parse the given file with the given data.
    :param path: Path to the file to parse
    :param data: Data to use when parsing
    :returns: Rendered Jinja template
    """
    logger.debug(f"Parsing '{path}'")
    loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(path))

    jenv = jinja2.Environment(loader=loader)
    _prepare_jenv(jenv)

    template = jenv.get_template(os.path.basename(path))
    return template.render(**data)


def metadata(name, data=None):
    """
    Retrieve the metadata from the 'templates/{name}/metadata.yml' file.
    :param name: Name of the template
    :returns: Dictionary of metadata on success. None on error.
    """
    if data is None:
        data = {}

    metadata_path = os.path.join(config.templates_folder, name, "metadata.yml")

    template_metadata = io.yaml_load(metadata_path)
    if template_metadata is None:
        logger.warning(f"template '{name}' missing or empty 'metadata.yml' file")
        return None

    return template_metadata


def all():
    """
    Get a list of all templates.
    :returns: Ordered dictionary of template's name
    """
    templates = {}
    for template in os.listdir(config.templates_folder):
        template_metadata = metadata(template)
        if template_metadata is not None:
            templates[template] = template_metadata

    # Order by template name (keys)
    templates = OrderedDict(sorted(templates.items()))

    return templates
