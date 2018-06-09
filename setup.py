import subprocess
import sys
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

with open('README.md', 'r') as f:
	long_description = f.read()


def get_version():
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
    return version


setup(
    name='extensible_provn',
    version=get_version(),
    description='Extensible PROV-N visualizer and querier',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests_*', 'tests']),
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

