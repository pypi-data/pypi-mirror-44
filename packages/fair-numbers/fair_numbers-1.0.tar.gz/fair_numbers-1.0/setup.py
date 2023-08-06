import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fair_numbers",
    version="1.0",
    author="Xalion",
    author_email="xalion67@gmail.com",
    description="Formating long numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/xalion/pretty-numbers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
