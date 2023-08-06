# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['letov']

package_data = \
{'': ['*']}

install_requires = \
['zstandard>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'letov',
    'version': '0.2.1',
    'description': 'TripSource logging utilities',
    'long_description': None,
    'author': 'BCD Trip tech',
    'author_email': 'development@bcdtriptech.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
