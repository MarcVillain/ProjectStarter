import os
import pathlib

self_folder = pathlib.Path(__file__).parent.absolute()

templates_folder = os.path.join(self_folder, "templates")
