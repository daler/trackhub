#!/bin/bash
set -e
set -x

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

src=/tmp/trackhub
mkdir $src
rm -f $HERE/../.git/shallow
git clone $HERE/.. $src
cd $src

# extract version
VERSION=$(python -c 'exec(open("trackhub/version.py").read());print(version)')
conda create -y -n trackhub-env python=2 --file requirements.txt
set +x; source activate trackhub-env; set -x
python setup.py clean sdist
pip install dist/trackhub-${VERSION}.tar.gz
conda install -y nose
nosetests trackhub/test/test.py
nosetests trackhub/test/test_parentonoff/test_parentonoff.py


