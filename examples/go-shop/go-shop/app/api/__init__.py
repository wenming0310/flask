# -*- coding: utf-8 -*-

"""
__init__.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask import Blueprint

from ..log import Logger

api = Blueprint(name='api',
                import_name=__name__,
                url_prefix='/api')

api_log = Logger('api_log', 'api_log.log')


@api.before_request
def api_before_request():
    pass


from . import (cart, )
