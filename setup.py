# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

with open("README.md", "r") as f:
	long_description = f.read()

setup(
    name="extensible_provn",
    version="0.0.1",
    description="Extensible PROV-N visualizer and querier",
    long_description=long_description,
    packages=find_packages(exclude=["tests_*", "tests"]),
    author=("Joao Pimentel",),
    author_email="joaofelipenp@gmail.com",
    license="MIT",
    keywords="provenance visualization",
    url="https://github.com/JoaoFelipe/extensible_provn",
)

