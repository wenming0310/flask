from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
#login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    '''
    #方法二
    db.app = app
    # db.drop_all()
    db.create_all()
    '''
    #方法三
    with app.test_request_context():
        db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')#url_prefix这里如果写错成url_pre在启动时就不会显示Login界面，
    # 同时不会报错，跳转http://127.0.0.1:5000/auth/login时会出现无法找到页面的情况
    return app
