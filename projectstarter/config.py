import os

from pkg_resources import resource_filename, Requirement

# Root directory (based on where the present file was installed)
_ROOT = os.path.abspath(os.path.dirname(__file__))

# Path to the templates folder
templates_folder = os.path.join(_ROOT, "templates")
