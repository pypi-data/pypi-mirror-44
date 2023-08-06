import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDaqMultin",
    version="0.0.2",
    author="Yuriy coroli, Hittech Multin",
    author_email="iuriikoroli@gmail.com",
    description="A package of examples of NI DAQ board controls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
