from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(os.path.join(here, "pyrailway", "VERSION")) as file:
        return file.read().strip()


def get_readme():
    with open(os.path.join(here, "README.rst")) as file:
        return file.read().strip()

setup(
    name="pyrailway",
    version=get_version(),
    description="A High-Level Architecture for Python Web Applications based on Trailblazer / Railway Oriented Programming",
    long_description=get_readme(),
    url="https://github.com/dpausp/pyrailway",
    author="Tobias dpausp",
    author_email="dpausp@posteo.de",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database",
        "Topic :: Software Development",
        
    ],
    keywords="railway-oriented-programming trailblazer web-applications web architecture pattern",
    packages=find_packages()
)
