import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="esBuilder",
    version="0.0.1",
    author="silin",
    author_email="silinwork@gmail.com",
    description="ez to use elasticSearch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sl40/esBuilder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)