#!/usr/bin/env python

import os
from setuptools import setup, find_packages

current_dir = os.path.dirname(__file__)

# load __version__, __author__, __email__, etc variables
with open(os.path.join(current_dir,'imagepypelines_tools/version_info.py')) as f:
    exec(f.read())

long_description = ''
if os.path.exists(os.path.join(current_dir,'README.md')):
    with open(os.path.join(current_dir,'README.md'), 'r') as f:
        long_description = f.read()

setup(name='imagepypelines-tools',
      version=__version__,
      description=__description__,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author=__author__,
      author_email=__email__,
      license=__license__,
      url=__url__,
      download_url=__download_url__,
      maintainer=__maintainer__,
      maintainer_email=__maintainer_email__,
      keywords=__keywords__,
      python_requires=__python_requires__,
      platforms=__platforms__,
      classifiers=__classifiers__,
      packages=find_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['imagepypelines = imagepypelines_tools:main'],}
      )
