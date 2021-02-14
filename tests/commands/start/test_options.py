from projectstarter import config
from projectstarter.commands.start import filter_options


def test_filter_options_simple(data_tree):
    patterns = ["license"]
    expected_res = {
        "license": {
            "commands": data_tree["options"]["license"]["commands"]
        }
    }

    assert filter_options(patterns, data_tree) == expected_res


def test_filter_options_simple_does_not_exist(data_tree):
    patterns = ["does_not_exist"]
    expected_res = {}

    assert filter_options(patterns, data_tree) == expected_res


def test_filter_options_simple_multiple(data_tree):
    patterns = ["license", "git"]
    expected_res = {
        "license": {
            "commands": data_tree["options"]["license"]["commands"]
        },
        "git": {
            "commands": data_tree["options"]["git"]["commands"]
        }
    }

    assert filter_options(patterns, data_tree) == expected_res


def test_filter_options_nested(data_tree):
    patterns = [f"license{config.options_sep}mit"]
    expected_res = {
        "license": {
            "commands": data_tree["options"]["license"]["commands"],
            "options": {
                "mit": {
                    "commands": data_tree["options"]["license"]["options"]["mit"]["commands"]
                }
            }
        }
    }

    assert filter_options(patterns, data_tree) == expected_res


def test_filter_options_nested_does_not_exist(data_tree):
    patterns = [f"licence{config.options_sep}does_not_exist"]
    expected_res = {}

    assert filter_options(patterns, data_tree) == expected_res


def test_filter_options_nested_multiple(data_tree):
    patterns = [f"license{config.options_sep}mit", f"license{config.options_sep}lgpl3"]
    expected_res = {
        "license": {
            "commands": data_tree["options"]["license"]["commands"],
            "options": {
                "mit": {
                    "commands": data_tree["options"]["license"]["options"]["mit"]["commands"]
                },
                "lgpl3": {
                    "commands": data_tree["options"]["license"]["options"]["lgpl3"]["commands"]
                }
            }
        }
    }

    assert filter_options(patterns, data_tree) == expected_res


def test_filter_all_options(data_tree):
    assert filter_options([], data_tree) == data_tree.get("options", {})
