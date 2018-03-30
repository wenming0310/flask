# -*- coding: utf-8 -*-

"""
extensions.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_login import LoginManager
from flask_principal import Principal
from flask_assets import Environment, Bundle
from flask_cache import Cache
from flask_uploads import UploadSet

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录'
login_manager.login_message_category = 'warning'
login_manager.blueprint_login_views = {
    'admin': 'admin.login'
}
login_manager.session_protection = 'strong'

redis_config = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": "127.0.0.1",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_PASSWORD": "",
    "CACHE_DEFAULT_TIMEOUT": 3600,
    "CACHE_KEY_PREFIX": "flask_go_shop_"
}
cache = Cache(config=redis_config)

principal = Principal()

photos = UploadSet('PHOTO')

assets_env = Environment()
main_css = Bundle('vendor/amazeui/css/amazeui.css',
                  filters='cssmin',
                  output='assets/css/base.css')

main_js = Bundle('vendor/jquery/jquery-2.2.4.js',
                 'vendor/amazeui/js/amazeui.js',
                 'js/global.js',
                 filters='jsmin',
                 output='assets/js/main.js')

main_js_ie8 = Bundle('vendor/jquery/jquery-1.12.4.js',
                     'vendor/amazeui/js/modernizr.js',
                     'vendor/amazeui/js/amazeui.ie8polyfill.js',
                     'vendor/amazeui/js/amazeui.js',
                     'js/global.js',
                     filters='jsmin',
                     output='assets/js/main_ie8.js')

admin_css = Bundle('vendor/amazeui/css/amazeui.css',
                   'css/admin.css',
                   filters='cssmin',
                   output='assets/css/admin.css')

admin_js = Bundle('vendor/jquery/jquery-2.2.4.js',
                  'vendor/amazeui/js/amazeui.js',
                  'js/admin.js',
                  'js/global.js',
                  filters='jsmin',
                  output='assets/js/admin.js')

admin_js_ie8 = Bundle('vendor/jquery/jquery-1.12.4.js',
                      'vendor/amazeui/js/modernizr.js',
                      'vendor/amazeui/js/amazeui.ie8polyfill.js',
                      'vendor/amazeui/js/amazeui.js',
                      'js/admin.js',
                      'js/global.js',
                      filters='jsmin',
                      output='assets/js/admin_ie8.js')
