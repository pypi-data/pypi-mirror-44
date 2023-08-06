# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pyramid_rasa']
setup_kwargs = {
    'name': 'pyramid-rasa',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Hadrien David',
    'author_email': 'hadrien@ectobal.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
