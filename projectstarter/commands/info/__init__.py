"""
Get more information on a template
"""
import argparse

from projectstarter.utils import templates, io


def _clean_metadata(metadata, parent=None, parent_key=None):
    """
    Keep only wanted metadata fields and move descriptions if necessary.
    :param metadata: The metadata to cleanup
    :param parent: The parent dict of the current metadata field
    :param parent_key: The key of the current metadata field in the parent dict
    """
    keys_to_keep = ["description", "include_templates"]
    keys_to_pop = []

    for k, v in metadata.items():
        # Go down the tree
        if isinstance(v, dict):
            _clean_metadata(v, parent=metadata, parent_key=k)
            continue

        # Filter out keys to remove
        if k not in keys_to_keep:
            keys_to_pop.append(k)

    # Remove unwanted keys
    for k in keys_to_pop:
        metadata.pop(k)

    # If there is only a description field, make it go up by one
    if parent is not None \
            and len(metadata.keys()) == 1 \
            and metadata.get("description", None) is not None:
        parent[parent_key] = metadata["description"]


def run(args):
    """
    Run the command.
    :param args: Arguments given to the command
    """
    metadata = templates.metadata(args.template, include=False)
    if not metadata:
        return 1

    _clean_metadata(metadata)

    io.yaml_dump(metadata)


def parse(prog, args):
    """
    Parse all the arguments given to the command.
    :param prog: Name of the program
    :param args: Arguments given to the command
    """
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        "template",
        help="template to display (see `project templates` for an exhaustive list)",
    )
    return parser.parse_args(args)
