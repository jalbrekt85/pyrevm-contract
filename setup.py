from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyrevm-contract",
    version="0.3.1",
    author="jalbrekt85",
    author_email="jcalbrecht85@gmail.com",
    description="Contract wrapper for pyrevm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jalbrekt85/pyrevm-contract",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyrevm==0.3.0",
        "eth-abi",
        "eth-utils",
        "eth-hash[pycryptodome]",
    ],
)
