# -*- coding: utf-8 -*-

"""
__init__.py.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import (users,
               commodities)
