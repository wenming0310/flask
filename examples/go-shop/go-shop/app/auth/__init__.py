# -*- coding: utf-8 -*-

"""
__init__.py.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask import Blueprint

from ..log import Logger

auth = Blueprint(name='auth',
                 import_name=__name__,
                 url_prefix='/auth')

auth_log = Logger('auth_log', 'auth_log.log')

from . import (views, )
