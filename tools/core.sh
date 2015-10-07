#!/usr/bin/env bash
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${BASE_DIR}/../"
export PYTHONPATH=$PYTHONPATH:`pwd`
source venv/bin/activate
#environmental variables
source venv/bin/settings
python -m domus.core >> /var/domus/domus.log