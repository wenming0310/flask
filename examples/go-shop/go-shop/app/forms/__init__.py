# -*- coding: utf-8 -*-

"""
__init__.py.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_wtf import CSRFProtect

csrf = CSRFProtect()

from . import (users,
               commodity)
