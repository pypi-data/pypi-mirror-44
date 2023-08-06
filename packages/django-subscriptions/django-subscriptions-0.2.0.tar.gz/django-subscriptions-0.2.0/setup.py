# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['subscriptions', 'subscriptions.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-fsm-log>=1.6,<2.0', 'django-fsm>=2.6,<3.0']

extras_require = \
{':python_version >= "2.7.0" and python_version < "2.8.0"': ['enum34>=1.1.6,<1.2.0']}

setup_kwargs = {
    'name': 'django-subscriptions',
    'version': '0.2.0',
    'description': 'A django package for managing subscription states',
    'long_description': '# django-subscriptions\n\nA django package for managing the status and terms of a subscription.\n\n[![CircleCI](https://circleci.com/gh/kogan/django-subscriptions.svg?style=svg)](https://circleci.com/gh/kogan/django-subscriptions)\n\n## Compatibility\n\n- Django: 1.11 and 2.2 (LTS versions only)\n- Python: 2.7 and 3.6+\n\nOther Django or Python versions **may** work, but that is totally cooincidental\nand no effort is made to maintain compatibility with versions other than those\nlisted above.\n\n## Installation\n\n```bash\n$ pip install django-subscriptions\n```\n\nThen add the following packages to `INSTALLED_APPS` in your settings:\n\n```\nINSTALLED_APPS = [\n    ...\n    "django_fsm_log",\n    "subscriptions.apps.SubscriptionsConfig",\n    ...\n]\n```\n\nAnd of course, you\'ll need to run the migrations:\n\n```\n$ python manage.py migrate\n```\n\nYou\'ll also need to setup the triggers, which can be scheduled with celery or\nrun from a management task. See the [Triggers](#triggers) section below.\n\n## Design\n\nManages subscriptions in a single table. Pushes events (signals) so that\nconsumers can do the actual work required for that subscription, like billing.\n\nSubscriptions are built around a Finite State Machine model, where states and\nallowed transitions between states are well defined on the Model. To update from\none state to another, the user calls methods on the Subscription instance. This\nway, all side-effects and actions are contained within the state methods.\n\nSubscription State must not be modified directly.\n\nWhen a state change is triggered, the subscription will publish relevant signals\nso that interested parties can, themselves, react to the state changes.\n\n![State Diagram](subscriptions-state-diagram.png)\n\n## API\n\nThere are 3 major API components. State change methods, signals/events, and the\ntriggers used to begin the state changes.\n\n### State Methods\n\n\n| Method                    \t| Source States                   \t| Target State \t| Signal Emitted       \t|\n|-------------------------- \t|---------------------------------\t|--------------\t|----------------------\t|\n| `cancel_autorenew()`      \t| ACTIVE                          \t| EXPIRING     \t| `autorenew_canceled` \t|\n| `enable_autorenew()`      \t| EXPIRING                        \t| ACTIVE       \t| `autorenew_enabled`  \t|\n| `renew()`                 \t| ACTIVE,SUSPENDED                \t| RENEWING     \t| `subscription_due`   \t|\n| `renewed()`               \t| RENEWING,ERROR                  \t| ACTIVE       \t| `subscription_renewed`\t|\n| `renewal_failed(reason="")`\t| RENEWING,ERROR                  \t| SUSPENDED    \t| `renewal_failed`     \t|\n| `end_subscription()`      \t| ACTIVE,SUSPENDED,EXPIRING,ERROR \t| ENDED        \t| `subscription_ended` \t|\n| `state_unknown(reason="")`\t| RENEWING                        \t| ERROR        \t| `subscription_error` \t|\n\nExample:\n\n`subscription.renew()` may only be called if `subscription.state` is either `ACTIVE` or `SUSPENDED`,\nand will cause `subscription.state` to move into the `RENEWING` state.\n\n\n### Triggers\n\nThere are a bunch of triggers that are used to update subscriptions as they become\ndue or expire. Nothing is configured to run these triggers by default. You can\neither call them as part of your own process, or use `celery beat` to execute\nthe triggers using the tasks provided in `subscriptions.tasks`.\n\n\nCreate a new subscription:\n\n```\nSubscription.objects.add_subscription(start_date, end_date, reference) -> Subscription\n```\n\nTrigger subscriptions that are due for renewal:\n\n```\nSubscription.objects.trigger_renewals() -> int  # number of renewals sent\n```\n\nTrigger subscriptions that are due to expire:\n\n```\nSubscription.objects.trigger_expiring() -> int  # number of expirations\n```\n\nTrigger subscriptions that have been suspended for longer than `timeout_days` to\nexpire:\n\n```\nSubscription.objects.trigger_suspended_timeout(timeout_days=3) -> int  # number of suspensions\n```\n\nTrigger subscriptions that have been stuck in renewing state for longer than `timeout_hours`\nto be marked as an error:\n\n```\nSubscription.objects.trigger_stuck(timeout_hours=2) -> int  # number of error subscriptions\n```\n\n\n### Tasks\n\nThe following tasks are defined but are not scheduled:\n\n```\nsubscriptions.tasks.trigger_renewals\nsubscriptions.tasks.trigger_expiring\nsubscriptions.tasks.trigger_suspended_timeout\nsubscriptions.tasks.trigger_stuck\n```\n\nIf you\'d like to schedule the tasks, do so with a celery beat configuration like this:\n\n```\n# settings.py\n\nCELERYBEAT_SCHEDULE = {\n    "subscriptions_renewals": {\n        "task": "subscriptions.tasks.trigger_renewals",\n        "schedule": crontab(hour=0, minute=10),\n    },\n    "subscriptions_expiring": {\n        "task": "subscriptions.tasks.trigger_expiring",\n        "schedule": crontab(hour=0, minute=15),\n    },\n    "subscriptions_suspended": {\n        "task": "subscriptions.tasks.trigger_suspended_timeout",\n        "schedule": crontab(hour=0, minute=40),\n        "kwargs": {"days": 3},\n    },\n    "subscriptions_stuck": {\n        "task": "subscriptions.tasks.trigger_stuck",\n        "schedule": crontab(hour="*/2", minute=50),\n        "kwargs": {"hours": 2},\n    },\n}\n```\n\n## Contributing\n\nWe use `pre-commit <https://pre-commit.com/>` to enforce our code style rules\nlocally before you commit them into git. Once you install the pre-commit library\n(locally via pip is fine), just install the hooks::\n\n    pre-commit install -f --install-hooks\n\nThe same checks are executed on the build server, so skipping the local linting\n(with `git commit --no-verify`) will only result in a failed test build.\n\nCurrent style checking tools:\n\n- flake8: python linting\n- isort: python import sorting\n- black: python code formatting\n\nNote:\n\n    You must have python3.6 available on your path, as it is required for some\n    of the hooks.\n',
    'author': 'Josh Smeaton',
    'author_email': 'josh.smeaton@gmail.com',
    'url': 'http://github.com/kogan/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
