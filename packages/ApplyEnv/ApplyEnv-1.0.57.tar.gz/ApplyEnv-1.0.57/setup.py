import setuptools


def long_description():
    with open("README.md", "rb") as fh:
        long_description = fh.read().decode()
    return long_description


setuptools.setup(
    name="ApplyEnv",
    version="1.0.57",
    author="ApplyEnv",
    author_email="applyenv@protonmail.ch",
    description="Populate variables in a tree-like schema",
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
