from projectstarter.commands.start import parse_commands


def test_parse_commands_simple():
    data_tree = {
        "commands": ["echo ok"]
    }
    expected = ["echo ok"]

    parse_commands(data_tree)
    assert data_tree["commands"] == expected


def test_parse_commands_multiple():
    data_tree = {
        "commands": ["echo ok", "echo ok2"]
    }
    expected = ["echo ok", "echo ok2"]

    parse_commands(data_tree)
    assert data_tree["commands"] == expected


def test_parse_commands_nested_simple_option():
    data_tree = {
        "commands": ["{{ options.license.commands }}"],
        "options": {
            "license": {
                "commands": ["echo ok"]
            }
        }
    }
    expected = ["echo ok"]

    parse_commands(data_tree)
    assert data_tree["commands"] == expected


def test_parse_commands_nested_simple_option_multiple():
    data_tree = {
        "commands": ["{{ options.license.commands }}", "{{ options.git.commands }}"],
        "options": {
            "license": {
                "commands": ["echo ok"]
            },
            "git": {
                "commands": ["echo ok2"]
            }
        }
    }
    expected = ["echo ok", "echo ok2"]

    parse_commands(data_tree)
    assert data_tree["commands"] == expected


def test_parse_commands_nested_twice_simple_option():
    data_tree = {
        "commands": ["{{ options.license.commands }}"],
        "options": {
            "license": {
                "commands": ["{{ options.mit.commands }}"],
                "options": {
                    "mit": {
                        "commands": ["echo ok"]
                    }
                }
            }
        }
    }
    expected = ["echo ok"]

    parse_commands(data_tree)
    assert data_tree["commands"] == expected


def test_parse_commands_nested_complex_option(data_tree):
    expected = ["echo lgpl3", "echo mit", "git init", "git add ."]

    parse_commands(data_tree)
    assert data_tree["commands"] == expected
