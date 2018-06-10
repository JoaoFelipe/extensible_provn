import subprocess
import sys
import os
from setuptools import setup, find_packages
from codecs import open
from os import path


def recursive_path(pack, path):
    matches = []
    for root, _, filenames in os.walk(os.path.join(pack, path)):
        for filename in filenames:
            matches.append(os.path.join(root, filename)[len(pack) + 1:])
    return matches


def get_version(*save_path):
    """Use git describe to get version from tag"""
    proc = subprocess.Popen(
        ("git", "describe", "--tag", "--always"),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output, _ = proc.communicate()
    result = output.decode("utf-8").strip()
    if proc.returncode != 0:
        sys.stderr.write(
            ">>> Git Describe Error:\n    " +
            result
        )
        return "1+unknown"
    split = result.split("-", 1)
    version = "+".join(split).replace("-", ".")

    if len(split) > 1:
        sys.stderr.write(
            ">>> Please verify the commit tag:\n    " +
            version + "\n"
        )

    if save_path:
        with open(path.join(*save_path), "w") as fil:
            fil.write(version)
    return version


with open('README.md', 'r') as f:
	long_description = f.read()


setup(
    name='extensible_provn',
    version=get_version("extensible_provn", "resources", "version.txt"),
    description='Extensible PROV-N visualizer and querier',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests_*', 'tests']),
    package_data={
        "extensible_provn": recursive_path("extensible_provn", "resources"),
    },
    entry_points={
        'console_scripts': [
            "provn=extensible_provn.view.provn:_main",
            "prov-dictionary=extensible_provn.view.prov_dictionary:_main",
            "versioned-prov=extensible_provn.view.versioned_prov:_main",
        ]
    },
    install_requires=[
        "lark-parser"
    ],
    author=('Joao Pimentel',),
    author_email='joaofelipenp@gmail.com',
    license='MIT',
    keywords='provenance visualization',
    url='https://github.com/JoaoFelipe/extensible_provn',
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Visualization',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],
)

