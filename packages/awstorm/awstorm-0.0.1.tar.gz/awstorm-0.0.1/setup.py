import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "Readme.md").read_text()

setup(
    name="awstorm",
    version="0.0.1",
    description="A Package to generate AWS project skeletons",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/edthamm/awstorm",
    author="Eduard Thamm",
    author_email="eduard.thamm@thammit.at",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["awstorm"],
    include_package_data=True
)
