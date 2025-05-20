#!/usr/bin/env bash
set -e
pip install -r requirements.txt
python -m py_compile bot.py
echo "Offline CI passed."
