# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pylint_requests', 'pylint_requests.checkers']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.0,<3.0']

setup_kwargs = {
    'name': 'pylint-requests',
    'version': '0.1.0',
    'description': 'A pylint plugin to check for common issues with usage of requests',
    'long_description': "# pylint-requests\n\n[![pypi](https://badge.fury.io/py/pylint-requests.svg)](https://pypi.org/project/pylint-requests)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/pylint-requests)\n[![Downloads](https://img.shields.io/pypi/dm/pylint-requests.svg)](https://pypistats.org/packages/pylint-requests)\n[![Build Status](https://travis-ci.com/m-burst/pylint-requests.svg?branch=master)](https://travis-ci.com/m-burst/pylint-requests)\n[![Code coverage](https://codecov.io/gh/m-burst/pylint-requests/branch/master/graph/badge.svg)](https://codecov.io/gh/m-burst/pylint-requests)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Description\n\nA `pylint` plugin to check for common issues with usage of `requests`.\n\nCurrently the following errors are reported:\n\n* `F7801 (requests-not-available)`  \nReported if this plugin failed to import `requests`.\nThis means that: (a) you are running `pylint` with incorrect `PYTHONPATH`,\n(b) you forgot to install `requests`, or (c) you aren't using `requests` and don't\nneed the plugin.\n* `E7801 (request-without-timeout)`  \nReported if a HTTP call (e.g. `requests.get`) without a timeout is detected.\n\n## Installation\n\n    pip install pylint-requests\n\n## Usage\n\nUse pylint's `--load-plugins` option to enable the plugin:\n\n    pylint --load-plugins=pylint_requests <your_code>\n\n## For developers\n\n### Install deps and setup pre-commit hook\n\n    make init\n\n### Run linters, autoformat, tests etc.\n\n    make pretty lint test\n\n### Bump new version\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n\n## License\n\nMIT\n\n## Change Log\n\n### 0.1.0 - 2019-04-14\n\n* initial\n",
    'author': 'Mikhail Burshteyn',
    'author_email': 'mdburshteyn@gmail.com',
    'url': 'https://pypi.org/project/pylint-requests',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
