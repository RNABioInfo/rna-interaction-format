from setuptools import setup, find_packages

NAME = "RIF"
DESCRIPTION = "Python API for handling RIF Format"

setup(
    name=NAME,
    version="0.0.0",
    author="RNAProNet Consortium",
    author_email="rabsch@informatik.uni-freiburg.de",
    packages=["RIF"],
    license="LICENSE",
    url="https://github.com/Ibvt/rna-interaction-specification",
    description=DESCRIPTION,
    long_description=open(
        "README.md"
    ).read(),
    package_data={'RIF': ['rna-interaction-schema_v1.json', 'tests/*.py', 'tests/*.json', 'tests/*.bed']},
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["ijson", "jsonschema", "biopython"]
)
