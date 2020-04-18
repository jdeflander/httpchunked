from setuptools import setup

_classifiers = [
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.5",
]

with open("README.md") as file:
    _long_description = file.read()

setup(
    author="Jasper Deflander",
    classifiers=_classifiers,
    description="Chunked transfer encoding as defined in RFC 7230",
    long_description=_long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    name="httpchunked",
    python_requires=">=3.5",
    py_modules=["httpchunked"],
    url="https://github.com/jdeflander/httpchunked",
    version="0.1.1",
)
