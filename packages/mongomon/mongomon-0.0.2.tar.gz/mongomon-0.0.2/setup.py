# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mongomon']

package_data = \
{'': ['*']}

install_requires = \
['attr>=0.3.1,<0.4.0',
 'colored>=1.3,<2.0',
 'pygments>=2.3,<3.0',
 'pymongo>=3.7,<4.0',
 'six>=1.12,<2.0',
 'toolz>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'mongomon',
    'version': '0.0.2',
    'description': 'A profiler for Python and mongodb',
    'long_description': '![](media/cover.png)\n\n# mongomon\n\nA Python mongodb monitor and profiler for development.\n\n\n## Quick Start\n\nInstall using pip/pipenv/etc. (we recommend [poetry](https://github.com/sdispater/poetry) for sane dependency management):\n\n```\n$ poetry add mongomon --dev\n```\n\nInitialize before you set up your MongoDB connection:\n\n```py\nfrom mongomon import Monitor, Config\nMonitor(Config(file_capture=".*/(wiki.*)")).monitor()\n```\n\nUse `file_capture` to specify how to extract relevant project file paths from traces, rather than absolute file paths.\n\n## Exploring the Example\n![](/media/demo.gif)\n\nWe\'ve taken the example from [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) to show how easy it is to have mongomon integrated and running.\n\nYou can [look at the integration here](examples/wiki). To run it:\n\n```\n$ poetry shell\n$ cd examples/wiki && pip install -r requirements\n$ python wiki.py\n```\n\n\n## Configuration\n\nYour main configuration points for mongomon are:\n\n* `file_capture` - an aesthetic configuration point for capturing files for your project. Usually of the form `.*/(your-project.*)`, content in parenthesis are a regular expression capture group, and is what we actually extract.\n* `low_watermark_us` - a threshold in microseconds (us) above which mongomon starts working (yellow).\n* `high_watermark_us` - a high threshold in microseconds (us) above which mongomon displays timing as alert (red).\n\n\nRest of configuration looks like so (with their defaults and comments):\n```py\n    # cleans up stack trace with uninteresting things. Usually packages, standard library, etc.\n    ignores = attrib(\n        default=[\n            ".*/site-packages/.*",\n            ".*traceback.format_stack.*",\n            r".*/lib/python\\d\\.\\d+/.*",\n        ]\n    )\n    # shows a file, cleans up absolute path to a file\n    file_capture = attrib(default="(.*)")\n    # above this value mongomon starts working\n    low_watermark_us = attrib(default=5000)\n    # above this value mongomon flags as alert\n    high_watermark_us = attrib(default=40000)\n    # customize how mongodb query looks like before printing to screen\n    query_filter = attrib(default=identity)\n    # want to print to something else? replace this\n    print_fn = attrib(default=print_)\n    # want shorter stack traces? customize this\n    stack_preprocess = attrib(default=trim_last)\n```\n\n### Thanks:\n\nTo all [Contributors](https://github.com/jondot/mongomon/graphs/contributors) - you make this happen, thanks!\n\n# Copyright\n\nCopyright (c) 2019 [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.',
    'author': 'Dotan Nahum',
    'author_email': 'jondotan@gmail.com',
    'url': 'https://github.com/jondot/mongomon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
