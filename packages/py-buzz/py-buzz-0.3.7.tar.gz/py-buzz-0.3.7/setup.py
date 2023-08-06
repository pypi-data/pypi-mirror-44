# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['buzz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-buzz',
    'version': '0.3.7',
    'description': '"That\'s not flying, it\'s falling with style: Exceptions with extras"',
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
