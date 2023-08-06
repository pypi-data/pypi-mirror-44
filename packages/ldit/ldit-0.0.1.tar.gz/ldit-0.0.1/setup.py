import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ldit",
    version="0.0.1",
    author="pany",
    author_email="pany@fedoraproject.org",
    description="List Docker hub Image Tags.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geekpany/ldit",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests"
    ],
    scripts=[
        'bin/ldit'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
