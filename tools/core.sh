#!/usr/bin/env bash
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${BASE_DIR}/../"
export PYTHONPATH=`pwd`:$PYTHONPATH
source venv/bin/activate
#environmental variables
source venv/bin/settings
python -mu domus.core > /var/log/domus/domus.log
