from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyrevm_contract",
    version="0.1.2",
    author="jalbrekt85",
    author_email="jcalbrecht85@gmail.com",
    description="Minimal Brownie like contract wrapper for Pyrevm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jalbrekt85/pyrevm_contract",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pyrevm",
        "eth-abi",
        "pysha3",
    ],

)
