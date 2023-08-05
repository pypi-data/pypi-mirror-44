# -*- coding: UTF-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyTechBrain",
    version="0.6.2",
    author="Adam Jurkiewicz",
    python_requires='>=3',
    author_email="python@abixedukacja.eu",
    description="PyTechBrain to nowa platforma wprowadzająca uczniów w dziedzinę IoT - Internet of Things (Internet Rzeczy).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ABIX-Edukacja/PyTechBrain",
    keywords='Arduino PyFirmata',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
	"Intended Audience :: Education",
    ],
)
