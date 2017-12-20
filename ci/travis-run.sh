#!/bin/bash
set -e

# Python 2 testing
source activate trackhub-test-env2
pytest -v --doctest-modules trackhub
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$HERE/run_build.sh && rm -rf $HERE/trackhub-demo $HERE/example_hub
(
  cd $HERE/../doc && make doctest
)
source deactivate

# Python 3 testing
source activate trackhub-test-env3
pytest -v --doctest-modules trackhub
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$HERE/run_build.sh && rm -rf $HERE/trackhub-demo $HERE/example_hub
(
  cd $HERE/../doc && make doctest
)

# Build docs under py3
$HERE/build-docs.sh
