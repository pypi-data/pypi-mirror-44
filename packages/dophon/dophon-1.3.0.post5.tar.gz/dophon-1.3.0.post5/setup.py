# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon',
 'dophon.annotation',
 'dophon.annotation.description',
 'dophon.annotation.req',
 'dophon.annotation.res',
 'dophon.tools',
 'dophon.tools.framework_const',
 'dophon.tools.gc']

package_data = \
{'': ['*']}

install_requires = \
['dophon-logger',
 'dophon-manager',
 'dophon-properties',
 'flask',
 'tornado',
 'tqdm',
 'urllib3']

setup_kwargs = {
    'name': 'dophon',
    'version': '1.3.0.post5',
    'description': 'dophon web framework like springboot',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
