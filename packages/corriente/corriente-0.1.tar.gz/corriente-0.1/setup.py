"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
exec(open('corriente/version.py').read())
setup(
    name = "corriente",
    version = __version__,
    description="Python streaming library",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jadielam/corriente",
    author = "Jadiel de Armas",
    author_email = "jadielam@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages = ["corriente"],
    include_package_data = True,
    install_requires = [
        "opencv-python"
    ]
)