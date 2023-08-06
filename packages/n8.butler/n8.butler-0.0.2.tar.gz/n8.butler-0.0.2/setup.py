from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="n8.butler",
    version="0.0.2",
    author="Nidelva",
    author_email="hi@n8.pm",
    license="MIT",
    description="It does a few things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nidelva/butler",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
