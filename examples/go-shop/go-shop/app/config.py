# -*- coding: utf-8 -*-

"""
config.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

import os

from flask_uploads import IMAGES

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "\xec|\x94\x96\xcc\x1d\x00\x04\xad'1\xa8!zw}\xf5\x93\x98\xf8l|\xfc\xb7"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SECRET_KEY = 'T4\x86U\x8f\x0b4\xa4&\x87\xa8#;;8\xe5\xa1\x9ek\xf5X\xc9\x19s'
    SLOW_DB_QUERY_TIME = 0.1
    ASSETS_DEBUG = False
    UPLOADED_PHOTO_DEST = os.path.join(BASE_DIR, os.path.join('uploads', 'photos'))
    UPLOADED_PHOTO_ALLOW = IMAGES


class ProductionConfig(Config):
    """
    - - - - - - - - - - -
    | **不要在此添加配置** |
    - - - - - - - - - - -
    所有用于服务器的配置均位于instance文件夹下的config.py文件中
    """
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@{ip}:{port}/{database}?charset={charset}' \
        .format(user='root',
                passwd='Trl.1991318',
                ip='localhost',
                port=3306,
                database='go-shop',
                charset='utf8')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'tianruoliang@sina.com'
    MAIL_PASSWORD = 'Trl.1991318'
    MAIL_DEFAULT_SENDER = 'Go Shop Dev'
    ASSETS_DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
