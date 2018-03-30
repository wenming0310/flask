# -*- coding: utf-8 -*-

"""
__init__.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask import Flask, g, request
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user
from flask_uploads import configure_uploads, patch_request_class

from .models import db
from .forms import csrf
from .email import mail
from extensions import (login_manager,
                        principal,
                        cache,
                        photos,
                        assets_env,
                        main_css, main_js, main_js_ie8,
                        admin_css, admin_js, admin_js_ie8)


def create_app(config_name, production=False):
    """
    工厂方法创建 Web App
    :param config_name: 从config中加载一个配置类
    :param production: 只有服务器部署时候设置为True，会加载instance下的config.py
    :return: app
    """
    app = Flask(__name__, instance_relative_config=production)
    app.config.from_object(config_name)
    app.config.from_pyfile('config.py', silent=True)

    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    principal.init_app(app)
    cache.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app, 64 * 1024 * 1024)
    assets_env.init_app(app)
    assets_env.register('main_css', main_css)
    assets_env.register('main_js', main_js)
    assets_env.register('main_js_ie8', main_js_ie8)
    assets_env.register('admin_css', admin_css)
    assets_env.register('admin_js', admin_js)
    assets_env.register('admin_js_ie8', admin_js_ie8)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        g.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    return app
