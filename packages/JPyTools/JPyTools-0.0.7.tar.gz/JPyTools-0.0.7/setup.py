import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JPyTools",
    version="0.0.7",
    author="jackkillian",
    description="Collection of fun functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jackkillian/JPyTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
