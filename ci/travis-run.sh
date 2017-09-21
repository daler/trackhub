#!/bin/bash
pytest trackhub/test
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$HERE/run_build.sh && rm -rf $HERE/trackhub-demo $HERE/example_hub
