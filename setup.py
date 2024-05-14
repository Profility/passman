from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "Terminal password manager in Python"
LONG_DESCRIPTION = ""

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="python-passman",
    version=VERSION,
    author="profility",
    author_email="contact@profility.slmail.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/profility/passman",
    packages=find_packages(),
    install_requires=[
        "typer",
        "python-gnupg"
    ],
    entry_points = {
        "console_scripts": [
            "passman=passman.cli:app"
        ]
    }
)