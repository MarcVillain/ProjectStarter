import re

import setuptools
from setuptools import setup


VERSION_FILE = "projectstarter/_version.py"


def get_version():
    with open(VERSION_FILE, "rt") as f:
        pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
        line = f.read()
        match = re.search(pattern, line, re.M)
        if match:
            return match.group(1)
        else:
            raise RuntimeError("Unable to find version string in %s." % (VERSION_FILE,))


if __name__ == "__main__":
    setup(
        version=get_version(),
        packages=setuptools.find_packages(),
        entry_points={
            "console_scripts": ["project=projectstarter.__main__:main"],
        },
        include_package_data=True,
    )
