# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

with open('README.md', 'r') as f:
	long_description = f.read()

setup(
    name='extensible_provn',
    version='0.0.1',
    description='Extensible PROV-N visualizer and querier',
    long_description=long_description,
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
    ],
)

