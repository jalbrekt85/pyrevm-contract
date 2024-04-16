#!/bin/bash

rm -rf dist/ build/
python setup.py sdist bdist_wheel
VERSION=$(python setup.py --version)
pip3 install dist/pyrevm-contract-$VERSION-py3-none-any.whl --force-reinstall
python -m unittest tests/test_contract.py
