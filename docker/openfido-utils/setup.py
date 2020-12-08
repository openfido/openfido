import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openfido-utils",
    version="0.1.0",
    author="Dane Summers",
    author_email="dane.summers@presencepg.com",
    description="OpenFIDO utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slacgismo/openfido-utils",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.7',
)
