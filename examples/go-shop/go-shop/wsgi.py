# -*- coding: utf-8 -*-

"""
wsgi.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from app import create_app
from app.config import ProductionConfig

wsgi = create_app(ProductionConfig, production=True)
