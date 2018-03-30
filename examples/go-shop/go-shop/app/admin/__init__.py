# -*- coding: utf-8 -*-

"""
__init__.py.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask import Blueprint

from ..log import Logger

admin = Blueprint(name='admin',
                  import_name=__name__,
                  url_prefix='/admin')

admin_log = Logger('admin_log', 'admin_log.log')

from . import (views, )
