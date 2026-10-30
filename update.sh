#!/bin/sh
set -eu

python -m unittest discover -s tests -v
python -m build
version=$(python -c 'from pathlib import Path; ns = {}; exec(Path("nlpcda/_version.py").read_text(), ns); print(ns["__version__"])')
python -m twine check "dist/nlpcda-$version.tar.gz" "dist/nlpcda-$version-py3-none-any.whl"
python -m twine upload --non-interactive "dist/nlpcda-$version.tar.gz" "dist/nlpcda-$version-py3-none-any.whl"
