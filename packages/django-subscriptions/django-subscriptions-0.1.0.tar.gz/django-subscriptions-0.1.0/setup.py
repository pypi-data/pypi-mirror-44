# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['subscriptions']

package_data = \
{'': ['*']}

install_requires = \
['django-fsm>=2.6,<3.0']

setup_kwargs = {
    'name': 'django-subscriptions',
    'version': '0.1.0',
    'description': 'A django package for managing subscription states',
    'long_description': '# django-subscriptions\nA django package for managing subscription states\n\n[![CircleCI](https://circleci.com/gh/kogan/django-subscriptions.svg?style=svg)](https://circleci.com/gh/kogan/django-subscriptions)\n\n\n## Contributing\n\nWe use `pre-commit <https://pre-commit.com/>` to enforce our code style rules\nlocally before you commit them into git. Once you install the pre-commit library\n(locally via pip is fine), just install the hooks::\n\n    pre-commit install -f --install-hooks\n\nThe same checks are executed on the build server, so skipping the local linting\n(with `git commit --no-verify`) will only result in a failed test build.\n\nCurrent style checking tools:\n\n- flake8: python linting\n- isort: python import sorting\n- black: python code formatting\n\nNote:\n\n    You must have python3.6 available on your path, as it is required for some\n    of the hooks.\n',
    'author': 'Josh Smeaton',
    'author_email': 'josh.smeaton@gmail.com',
    'url': 'http://github.com/kogan/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
