

import os

import setuptools


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="flake8_extensions",
    version="0.1.0",
    description="Flake8 extensions",
    author="Auchan Direct",
    packages=[
        "flake8_extensions",
    ],
    install_requires=[
        "flake8 > 3.0.0",
    ],
    entry_points={
        'flake8.extension': [
            'F8E = flake8_extensions:ForbidenImportsChecker',
        ],
    },
)
