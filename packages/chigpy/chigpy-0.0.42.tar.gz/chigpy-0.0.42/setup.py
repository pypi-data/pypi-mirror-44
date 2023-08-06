import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chigpy",
    version="0.0.42",
    author="Chirag Aswani",
    author_email="chirag@aswani.net",
    description="A python package built by Chirag Aswani",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChiragAswani/chigpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)