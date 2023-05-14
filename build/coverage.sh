#!/usr/bin/env bash

source .venv/bin/activate

pytest --cov=merge-files/src --cov-report=html .
