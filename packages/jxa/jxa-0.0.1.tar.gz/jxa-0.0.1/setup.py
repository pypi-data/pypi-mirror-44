import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jxa",
    version="0.0.1",
    author="Jurek Kedra",
    author_email="jurek.kedra@gmail.com",
    description="Generic Libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jkedra/jxa",
    packages=['jxa'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
