import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aegs",
    version="0.0.1",
    author="RishabhBhatnagar",
    author_email="bhatnagarrishabh4@gmail.com",
    description="Model for aegs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/RishabhBhatnagar/mlp/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
