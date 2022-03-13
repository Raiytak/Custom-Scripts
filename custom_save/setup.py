from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="custom-save",
    version="1.0",
    python_requires=">=3.8",
    description="Script to save your important files in your hardware",
    long_description=long_description,
    url="https://github.com/Raiytak/",
    author="Mathieu Salaun",
    author_email="mathieu.salaun12@gmail.com",
    license="MIT",
)
