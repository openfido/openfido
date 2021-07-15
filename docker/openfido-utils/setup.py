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
    packages=['application_roles', 'blob_utils', 'openfido'],
    entry_points={
        'console_scripts': ['openfido = openfido.script:main'],
    },
    classifiers=[],
    python_requires='>=3.7',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
