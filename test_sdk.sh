#! /bin/bash

source venv/bin/activate

for f in ./server/zero_sdk/__tests__/*.py; do
    PYTHONPATH=$(pwd) python3 $f
done