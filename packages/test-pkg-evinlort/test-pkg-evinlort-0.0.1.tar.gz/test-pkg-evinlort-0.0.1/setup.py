import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test-pkg-evinlort",
    version="0.0.1",
    author="Evegny",
    author_email="evg@wallter.com",
    description="A small test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evinlort/test_pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)