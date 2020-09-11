import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="presence-workflow-service",
    version="0.1.0",
    author="Dane Summers",
    author_email="dane.summers@presencepg.com",
    description="Workflow API Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PresencePG/presence-workflow-service",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.7',
)
