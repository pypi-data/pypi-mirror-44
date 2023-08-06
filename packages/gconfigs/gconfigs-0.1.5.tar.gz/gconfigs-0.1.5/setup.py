# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gconfigs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gconfigs',
    'version': '0.1.5',
    'description': 'Config and Secret parser for your Python projects',
    'long_description': None,
    'author': 'Douglas Miranda',
    'author_email': 'douglascoding@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
