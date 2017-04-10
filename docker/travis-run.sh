#!/bin/bash
set -e
set -x

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

src=$(mktemp -d --tmpdir trackhub-XXXX)
rm -f $HERE/../.git/shallow
cp -r $HERE/.. $src
cd $src

CONDA_ENV=trackhub-test-env

conda config --add channels conda-forge
conda config --add channels defaults
conda config --add channels r
conda config --add channels bioconda

conda env list | grep -q $CONDA_ENV && conda env remove -y -n $CONDA_ENV

# extract version
VERSION=$(python -c 'exec(open("trackhub/version.py").read());print(version)')
conda create -y -n $CONDA_ENV python=3 --file requirements.txt --file test-requirements.txt
set +x; source activate $CONDA_ENV; set -x
python setup.py clean sdist
pip install dist/trackhub-${VERSION}.tar.gz

pytest trackhub/test/test.py
