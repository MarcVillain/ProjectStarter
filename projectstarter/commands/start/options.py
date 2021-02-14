import re

from projectstarter import config
from projectstarter.utils import logger


def _filter_options(patterns, options_tree):
    """
    Recursive iteration on nested options. If an option matches one of
    the given names, it is added to the list of returned options.
    :param patterns: List of the options patterns to look for (separated with config.options_sep if nested)
    :param options_tree: The options dictionary tree
    :return: Dictionary of key/value options that matched the given names. None on error.
    """
    # Stop recursion
    if len(patterns) == 0:
        return {}

    options = {}

    # For each option
    for name, value in options_tree.get("options", {}).items():
        # For each pattern
        for pattern in patterns:
            try:
                if config.options_sep not in pattern:
                    # Handle simple option
                    if re.match(pattern, name):
                        # No need for nested options on match
                        if "options" in value.keys():
                            value.pop("options")
                        # Add option in options list
                        options[name] = value
                else:
                    # Handle nested option
                    if re.match(pattern.split(config.options_sep)[0], name):
                        # Move patterns one option forward
                        new_patterns = [
                            re.sub(r"^.*?" + config.options_sep, "", p)
                            for p in patterns
                            if config.options_sep in p
                        ]
                        # Get nested options
                        new_options = _filter_options(new_patterns, value)
                        if new_options is None:
                            return None
                        # Ensure the key exists
                        options[name] = options.setdefault(name, value)
                        # Set the new options
                        options[name]["options"] = new_options
            except re.error as e:
                logger.error(f"option pattern '{pattern}' is invalid: {e}")
                return None

    return options


def filter_options(patterns, options_tree):
    """
    Recursive iteration on nested options. If an option matches one of
    the given names, it is added to the list of returned options.
    If the list of patterns is empty, then all options are filterd.
    :param patterns: List of the options patterns to look for (separated with config.options_sep if nested)
    :param options_tree: The options dictionary tree
    :return: Dictionary of key/value options that matched the given names. None on error.
    """
    if len(patterns) == 0:
        # Retrieve all
        filtered_options = options_tree.get("options", {})
    else:
        # Retrieve partial
        filtered_options = _filter_options(patterns, options_tree)

    # Display unmatched options
    pattern_has_not_matched = False
    for pattern in patterns:
        if pattern.split(config.options_sep)[0] not in filtered_options.keys():
            pattern_has_not_matched = True
            logger.error(f"Option pattern '{pattern}' did not match anything.")

    return None if pattern_has_not_matched else filtered_options
