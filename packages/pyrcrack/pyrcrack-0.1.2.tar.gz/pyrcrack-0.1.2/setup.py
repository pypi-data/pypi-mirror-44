# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrcrack']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=3.0,<4.0', 'docopt>=0.6.2,<0.7.0', 'stringcase>=1.2,<2.0']

setup_kwargs = {
    'name': 'pyrcrack',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
