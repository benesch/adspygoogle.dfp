#!/usr/bin/python
#
# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup script for the DFP API Python Client Library."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
from setuptools import setup

from adspygoogle.dfp import LIB_AUTHOR
from adspygoogle.dfp import LIB_NAME
from adspygoogle.dfp import LIB_URL
from adspygoogle.dfp import LIB_VERSION


PACKAGES = ['adspygoogle', 'adspygoogle.common', 'adspygoogle.common.https',
            'adspygoogle.common.soappy', 'adspygoogle.dfp',
            'adspygoogle.SOAPpy', 'adspygoogle.SOAPpy.wstools']
PACKAGE_DATA = {'adspygoogle.dfp': [os.path.join('data', '*')]}
SCRIPTS = ['scripts/dfp_config.py']
INSTALL_REQUIRES = ['zsi', 'fpconst', 'google-api-python-client']


setup(name='adspygoogle.dfp',
      version=LIB_VERSION,
      description=LIB_NAME,
      author=LIB_AUTHOR,
      maintainer=LIB_AUTHOR,
      url=LIB_URL,
      license='Apache License 2.0',
      long_description='For additional information, please see %s' % LIB_URL,
      scripts=SCRIPTS,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      install_requires=INSTALL_REQUIRES,
      platforms='any')
