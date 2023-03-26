#!/bin/bash

source .venv/bin/activate

python3 -m twine upload merge-files/dist/* --user=__token__
