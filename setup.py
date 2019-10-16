#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
from os.path import join as opj
from os.path import dirname


def get_version():
    """Load version only
    """
    with open(opj(dirname(__file__), 'schizconnect_dd_to_json', '__init__.py')) as f:
        version_lines = list(filter(lambda x: x.startswith('__version__'), f))
    assert (len(version_lines) == 1)
    return version_lines[0].split('=')[1].strip(" '\"\t\n")

# extension version
version = get_version()
PACKAGES = find_packages()

README = opj(dirname(__file__), 'README.md')
try:
    import pypandoc
    long_description = pypandoc.convert(README, 'rst')
except (ImportError, OSError) as exc:
    print(
        "WARNING: pypandoc failed to import or threw an error while converting"
        " README.md to RST: %r  .md version will be used as is" %exc
    )
    long_description = open(README).read()

# Metadata
setup(
    name='schizconnect_dd_to_json',
    version=version,
    description='Converts some of schizconnect data dictionaries to json',
    long_description=long_description,
    author='David Keator',
    author_email='dbkeator@uci.edu',
    url='https://github.com/dbkeator/schizconnect_dd_to_json',
    packages=PACKAGES,
    install_requires=[
        'numpy',
        'pandas',
    ], # Add requirements as necessary
    include_package_data=True,
    extras_require={
        'devel-docs': [
            # for converting README.md -> .rst for long description
            'pypandoc',
        ]},
    entry_points={
        'console_scripts': [
            'schizconnect2json=schizconnect_dd_to_json.schizconnect_dd_to_json:main' # this is where the console entry points are defined
            ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Change if necessary
)

