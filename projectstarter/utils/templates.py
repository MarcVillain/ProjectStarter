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


def _include_templates(data):
    """
    Recursively iterate through every fields of a dictionary and replace the
    'include_templates' fields with the corresponding template's metadata.
    :param data: The metadata to update
    :return: The updated metadata
    """
    templates = []

    for k, v in data.items():
        # Recursive iteration
        if isinstance(v, dict):
            data[k] = _include_templates(v)
        # Extract templates to include
        elif k == "include_templates":
            templates += v

    # if there are templates to include
    if len(templates) > 0:
        # Remove include field
        data.pop("include_templates")

        # Update fields with template's data
        for template in templates:
            logger.debug(f"including template: {template}")
            included_data = metadata(template)
            logger.debug(f"{template} template data: {included_data}")
            # Append new values to the data
            for k, v in included_data.items():
                # If it does not exist, add the new field
                if k not in data.keys():
                    data[k] = v

                # If its a list, append item to existing values if necessary
                elif isinstance(data[k], list):
                    if isinstance(v, list):
                        for item in v:
                            if item not in data[k]:
                                data[k].append(item)
                    else:
                        if v not in data[k]:
                            data[k].append(v)

    return data


def metadata(name):
    """
    Retrieve the metadata from the 'templates/{name}/metadata.yml' file.
    :param name: Name of the template
    :returns: Dictionary of metadata on success. None on error.
    """
    metadata_path = os.path.join(config.templates_folder, name, "metadata.yml")
    logger.debug(f"metadata.yml path: {metadata_path}")

    # Load template metadata
    template_metadata = io.yaml_load(metadata_path)
    if template_metadata is None:
        logger.warning(f"template '{name}' missing or empty 'metadata.yml' file")
        return None

    # Load included templates
    template_metadata = _include_templates(template_metadata)

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
