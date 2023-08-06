import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ais-wordnet",
    version="0.0.4",
    author="Minh Dinh",
    author_email="extreme45nm@gmail.com",
    description="An interface for the wordnet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minhdc/ais-wordnet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)