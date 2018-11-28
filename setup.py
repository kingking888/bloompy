import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bloompy",
    version="0.0.1",
    author="linkin",
    author_email="yooleak@outlook.com",
    description="Implementation of Bloom Filter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/01ly/bloompy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "bitarray >= 0.8.3",
    ],
)