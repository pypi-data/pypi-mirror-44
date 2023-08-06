# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kira_setup', 'kira_setup.pipelines']

package_data = \
{'': ['*']}

install_requires = \
['python-gitlab>=1.8,<2.0', 'termcolor>=1.1,<2.0']

entry_points = \
{'console_scripts': ['kira-setup = kira_setup.cli:main']}

setup_kwargs = {
    'name': 'kira-setup',
    'version': '0.1.0',
    'description': "Kira's CLI to setup new projects",
    'long_description': '# Kira Setup Bot\n\n[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)\n[![kira-family](https://img.shields.io/badge/kira-family-pink.svg)](https://github.com/wemake-services/kira)\n[![Build Status](https://travis-ci.org/wemake-services/kira-setup.svg?branch=master)](https://travis-ci.org/wemake-services/kira-setup)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/wemake-services/kira-setup/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\nCLI utility to automate routine work with creating new projects.\n\nPart of the [`@kira`](https://github.com/wemake-services/kira) bots family.\n\n\n## Installation\n\n```\npip install kira-setup\n```\n\n## Running\n\n```\nkira-setup group_or_user_name/project_name --token=YOUR_ACCESS_TOKEN\n```\n\n## Features\n\nWe use this CLI to setup high quality standards for our repository.\nFeatures that we care about:\n1. Protected `master` and tags for releases only\n2. Mandatory code reviews\n3. Integration with [`kira-stale`](https://github.com/wemake-services/kira-stale) and [`kira-release`](https://github.com/wemake-services/kira-release)\n',
    'author': 'sobolevn',
    'author_email': 'mail@sobolevn.me',
    'url': 'https://github.com/wemake-services/kira-setup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
