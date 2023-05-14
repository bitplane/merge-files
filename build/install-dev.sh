#!/usr/bin/env bash

# activate venv
source .venv/bin/activate

# install our package
python3 -m pip install -e ./merge-files[dev]

# let make know that we are installed in user mode
echo "Installed in dev mode"
touch .venv/.installed-dev
rm .venv/.installed || true
