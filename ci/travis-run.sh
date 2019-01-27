#!/bin/bash
set -e

# Python 2 testing
source activate trackhub-test-env-py2
pytest -vv --doctest-modules trackhub
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
(
  cd $HERE/../doc && make doctest
)
source deactivate

# Python 3 testing
source activate trackhub-test-env-py3
pytest -vv --doctest-modules trackhub
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
(
  cd $HERE/../doc && make doctest
)

# Build docs and upload to trackhub-demo repo only under py3
$HERE/run_build.sh && rm -rf $HERE/trackhub-demo $HERE/example_hub
$HERE/build-docs.sh
