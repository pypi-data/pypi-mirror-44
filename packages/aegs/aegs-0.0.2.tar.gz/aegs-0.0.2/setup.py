import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aegs",
    version="0.0.2",
    author="Rishabh Bhatnagar",
    author_email="bhatnagarrishabh4@gmail.com",
    description="model for aegs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RishabhBhatnagar/mlp",
    packages=setuptools.find_packages(),
    package_data={'':["gensim_model", "lstm_model"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
