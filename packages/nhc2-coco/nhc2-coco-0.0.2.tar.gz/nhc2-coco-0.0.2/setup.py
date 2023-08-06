# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nhc2_coco']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt==1.4.0']

setup_kwargs = {
    'name': 'nhc2-coco',
    'version': '0.0.2',
    'description': 'Python controller for a Niko Home Control II installation',
    'long_description': None,
    'author': 'filipvh',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
