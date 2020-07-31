#!/bin/bash

set -e
set -x

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


if ! hash conda; then
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /tmp/miniconda
    export PATH=/tmp/miniconda/bin:$PATH
    conda config --add channels defaults
    conda config --add channels conda-forge
    conda config --add channels bioconda
fi

# extract version
VERSION=$(python -c 'exec(open("trackhub/version.py").read());print(version)')


CONDA_ENV3=trackhub-test-env-py3
conda env list | grep -q $CONDA_ENV3 && conda env remove -y -n $CONDA_ENV3
conda create -y -n $CONDA_ENV3 python=3 --file requirements.txt --file test-requirements.txt
set +x; source activate $CONDA_ENV3; set -x
python setup.py clean sdist
pip install dist/trackhub-${VERSION}.tar.gz

CONDA_ENV2=trackhub-test-env-py2
conda env list | grep -q $CONDA_ENV2 && conda env remove -y -n $CONDA_ENV2
conda create -y -n $CONDA_ENV2 python=2 --file requirements.txt --file test-requirements.txt
set +x; source activate $CONDA_ENV2; set -x
python setup.py clean sdist
pip install dist/trackhub-${VERSION}.tar.gz
