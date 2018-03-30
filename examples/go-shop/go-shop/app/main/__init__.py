# -*- coding: utf-8 -*-

"""
__init__.py.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask import Blueprint

from ..log import Logger

main = Blueprint(name='main',
                 import_name=__name__)

main_log = Logger('main_log', 'main_log.log')

from . import (views, )
