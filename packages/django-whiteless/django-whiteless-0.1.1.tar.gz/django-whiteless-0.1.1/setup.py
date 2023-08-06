# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['whiteless', 'whiteless.templatetags']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['Django>=1.11,<2.0'],
 ':python_version >= "3.5" and python_version < "4.0"': ['Django>=2.0,<3.0']}

setup_kwargs = {
    'name': 'django-whiteless',
    'version': '0.1.1',
    'description': 'Django template tags for dealing with pesky whitespaces',
    'long_description': None,
    'author': 'Deniz Dogan',
    'author_email': 'denizdogan@users.noreply.github.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
