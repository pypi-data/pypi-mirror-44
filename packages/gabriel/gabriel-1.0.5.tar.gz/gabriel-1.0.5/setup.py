import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gabriel",
    version="1.0.5",
    author="April",
    author_email="aaprilthemonth@gmail.com",
    description="Discord RPC cli tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aapriI/gabriel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/gab'],
)