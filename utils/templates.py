import os
from collections import OrderedDict

import config
from utils import io, logger


def all():
    templates = {}
    for template in os.listdir(config.templates_folder):
        metadata_path = os.path.join(config.templates_folder, template, "metadata.yml")

        template_metadata = io.load_yaml(metadata_path)
        if template_metadata is None:
            logger.warning(f"template '{template}' missing or empty 'metadata.yml' file")
            continue

        templates[template] = template_metadata

    # Order by template name (keys)
    templates = OrderedDict(sorted(templates.items()))

    return templates
