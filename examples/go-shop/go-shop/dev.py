# -*- coding: utf-8 -*-

"""
dev.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from app import create_app
from app.config import DevelopmentConfig

dev = create_app(DevelopmentConfig)

if __name__ == '__main__':
    for k, v in dev.config.items():
        print('{k} == {v}'.format(k=k, v=v))
    dev.run(debug=True, host='0.0.0.0', port=5000)
