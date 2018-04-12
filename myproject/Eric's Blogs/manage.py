import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User,Role=Role)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

#下面这行如果不注释掉在控制台输入python manage.py shell会报以下错误：TypeError: <flask_script.commands.Shell object at 0x03D74730>: 'dict' object is not callable
#manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    #app.run()