import setuptools


def long_description():
    with open("README.md", "rb") as fh:
        long_description = fh.read().decode()
    return long_description


setuptools.setup(
    name="pydotdict",
    version="3.3.11",
    author="PyDotDict",
    author_email="pydotdict@protonmail.ch",
    description="Production ready Python 3 dictionary with dot style access",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=(
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ),
)
