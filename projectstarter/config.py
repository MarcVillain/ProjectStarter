import os

from pkg_resources import resource_filename, Requirement

_ROOT = os.path.abspath(os.path.dirname(__file__))

templates_folder = os.path.join(_ROOT, "templates")
