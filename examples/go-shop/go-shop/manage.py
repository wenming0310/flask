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
from app.config import ProductionConfig
from app.models import db
from app.models.users import Role
from extensions import assets_env

app = create_app(ProductionConfig, production=True)

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets(assets_env))


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def new_db():
    """
    清空数据，重置数据库
    clean all data and reset database
    :return:
    """
    db.drop_all()
    db.create_all()
    Role.insert_role()


if __name__ == '__main__':
    manager.run()
    #app.run()
