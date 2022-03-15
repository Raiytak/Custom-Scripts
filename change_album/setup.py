from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="change-album",
    version="1.0",
    python_requires=">=3.8",
    description="Script to change the album's name of mp3 files",
    long_description=long_description,
    url="https://github.com/Raiytak/",
    author="Mathieu Salaun",
    author_email="mathieu.salaun12@gmail.com",
    install_requires="eyed3",
    packages=["change_album"],
    license="MIT",
)
