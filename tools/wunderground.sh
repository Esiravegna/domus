#!/usr/bin/env bash
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${BASE_DIR}/../"
export PYTHONPATH=$PYTHONPATH:`pwd`
source venv/bin/activate
source venv/bin/settings

python -m utils.wunderground
