#!/usr/bin/env bash
# One-liner dev setup for new contributors
set -e
python -m pip install -r requirements.txt
python -m pip install -e ".[dev]"
pre-commit install
echo "✅  Environment ready – run: pytest -q"
