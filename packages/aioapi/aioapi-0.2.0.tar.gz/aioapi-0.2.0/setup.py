# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioapi', 'aioapi.inspect']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5.4', 'pydantic>=0.20.1']

setup_kwargs = {
    'name': 'aioapi',
    'version': '0.2.0',
    'description': 'Yet another way to build APIs using AIOHTTP framework',
    'long_description': "# aioapi\n\n![GitHub commit merge status](https://img.shields.io/github/commit-status/Gr1N/aioapi/master/HEAD.svg?label=build%20status) [![codecov](https://codecov.io/gh/Gr1N/aioapi/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aioapi) ![PyPI](https://img.shields.io/pypi/v/aioapi.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioapi.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aioapi.svg)\n\nYet another way to build APIs using [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework.\n\nFollow [documentation](https://gr1n.github.io/aioapi/) to know what you can do with `AIOAPI`.\n\n## Installation\n\n```sh\n$ pip install aioapi\n```\n\n## Usage\n\nExamples of usage can be found at [`examples/`](https://github.com/Gr1N/aioapi/tree/master/example) directory.\n\nTo run example use command below:\n\n```sh\n$ make example\n```\n\n## Contributing\n\nTo work on the `AIOAPI` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/aioapi.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify what you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## Milestones\n\nIf you're interesting in project's future you can find milestones and plans at [projects](https://github.com/Gr1N/aioapi/projects) page.\n\n## License\n\n`AIOAPI` is licensed under the MIT license. See the license file for details.\n",
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'url': 'https://github.com/Gr1N/aioapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
