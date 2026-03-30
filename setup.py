from setuptools import setup, find_packages

setup(
    name="horus",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "horus=horus.main:main"
        ]
    },
)