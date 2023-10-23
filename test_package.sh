#!/bin/bash

rm -rf dist/ build/
python3 setup.py sdist bdist_wheel
VERSION=$(python3 setup.py --version)
pip3 install dist/pyrevm_contract-$VERSION-py3-none-any.whl --force-reinstall
python3 tests/test_contract.py
