#! /bin/bash

source venv/bin/activate

for f in ./app/zero_sdk/__tests__/*.py; do
    PYTHONPATH=$(pwd)/app python3 $f
done