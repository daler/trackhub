import ez_setup
ez_setup.use_setuptools()

import os
import sys
from setuptools import setup

version_py = os.path.join(os.path.dirname(__file__), 'trackhub', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"','')

long_description = """
Create and manage UCSC track hubs from Python
"""

install_requires = ['fabric']
if (sys.version_info[0] == 2) and (sys.version_info[1] < 7):
    install_requires.append('ordereddict')

setup(
        name="trackhub",
        version=version,
        install_requires=install_requires,
        packages=['trackhub',
                  'trackhub.test',
                  'trackhub.test.data',
                  'trackhub.scripts'],
        author="Ryan Dale",
        description=long_description,
        long_description=long_description,
        url="http://github.com/daler/trackhub",
        package_data = {'trackhub':["test/data/*"]},
        package_dir = {"trackhub": "trackhub"},
        #scripts = ['trackhub/scripts/example_script.py'],
        author_email="dalerr@niddk.nih.gov",
        classifiers=['Development Status :: 4 - Beta'],
    )
