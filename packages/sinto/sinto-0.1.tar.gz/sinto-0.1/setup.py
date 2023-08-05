#!/usr/bin/env python

import setuptools
import versioneer
import subprocess
import sys


def samtools():
    if (sys.version_info > (3, 0)):
        v = subprocess.check_output(['samtools', '--version']).decode().split()[1].split('.')
    else:
        v = subprocess.check_output(['samtools', '--version']).split()[1].split('.')
    major = int(v[0])
    if major >= 1:
        return True
    return False


if __name__ == "__main__":
    if not samtools():
        raise Exception("sinto requires samtools >= v1")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'sinto',
    version = versioneer.get_version(),
    cmdclass = versioneer.get_cmdclass(),
    description = "sinto: tools for single-cell data processing",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = 'Tim Stuart',
    install_requires = [
        'pysam>=0.8',
    ],
    scripts = ["scripts/sinto"],
    author_email = 'tstuart@nygenome.org',
    url = 'https://github.com/timoast/sinto',
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    ]
)
