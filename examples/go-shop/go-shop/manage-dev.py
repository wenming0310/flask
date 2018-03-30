# -*- coding: utf-8 -*-

"""
manage.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_assets import ManageAssets

from app import create_app
from app.config import DevelopmentConfig
from app.models import db
from app.models.users import Role
from app.fake import (user_generate_fake,
                      tag_generate_fake,
                      commodity_generate_fake,
                      vip_user_generate_fake,
                      admin_user_generate_fake,
                      comment_generate_fake)
from extensions import assets_env

app = create_app(DevelopmentConfig)

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets(assets_env))


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def test_db():
    """
    清空数据，创建测试数据库
    :return:
    """
    db.drop_all()
    db.create_all()
    Role.insert_role()
    user_generate_fake()
    vip_user_generate_fake()
    admin_user_generate_fake()
    tag_generate_fake()
    commodity_generate_fake()
    comment_generate_fake()


@manager.command
def new_db():
    """
    清空数据，重置数据库
    :return:
    """
    db.drop_all()
    db.create_all()
    Role.insert_role()


if __name__ == '__main__':
    manager.run()
