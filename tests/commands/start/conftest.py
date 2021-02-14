import pytest


@pytest.fixture
def data_tree():
    return {
        "commands": [
            "{{ options.license.commands }}",
            "{{ options.git.commands }}",
        ],
        "options": {
            "license": {
                "commands": ["{{ options.lgpl3.commands }}", "{{ options.mit.commands }}"],
                "options": {
                    "mit": {
                        "commands": ["echo mit"]
                    },
                    "lgpl3": {
                        "commands": ["echo lgpl3"]
                    }
                }
            },
            "git": {
                "commands": ["git init", "git add ."]
            }
        }
    }
