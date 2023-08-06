import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MultiBinary",
    version="1.0.0",
    author="Devin Wallace",
    author_email="devinwallace@protonmail.com",
    description="A multi-thread binary search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Devin-Wallace/MultiBinary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)