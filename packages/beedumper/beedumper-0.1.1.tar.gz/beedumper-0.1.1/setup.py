# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beedumper']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'click>=7.0,<8.0',
 'pathos>=0.2.3,<0.3.0',
 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['beedumper = beedumper.cli:cli']}

setup_kwargs = {
    'name': 'beedumper',
    'version': '0.1.1',
    'description': 'Exporting SupportBee data for better integration with other ticketing tools',
    'long_description': None,
    'author': 'Jorge Sanz',
    'author_email': 'jsanz@carto.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
