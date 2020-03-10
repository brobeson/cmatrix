"""Setuptools installation script."""

import setuptools

setuptools.setup(
    name="matrix_builder",
    version="0.1",
    author="brobeson",
    author_email="brobeson@users.noreply.github.com",
    description="A tool to run a matrix build of a C++ project.",
    url="https://github.com/brobeson/matrix_builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": "mbuild = matrix_builder.mbuild:main"},
)
