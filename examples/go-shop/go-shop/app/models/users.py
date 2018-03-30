# -*- coding: utf-8 -*-

"""
users.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

import datetime

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_principal import Permission, RoleNeed
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired,
                          BadTimeSignature,
                          BadSignature)
from . import db
from .commodities import Record
from extensions import login_manager

# ==================角色定义=======================
ROLES = ['admin', 'vip']
ROLES_MAP = {
    'admin': '管理员',
    'vip': '会员'
}

# ==================权限声明=======================
admin_permission = Permission(RoleNeed('admin'))
vip_permission = Permission(RoleNeed('vip'))


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(255))

    @staticmethod
    def insert_role():
        db.session.add_all(map(lambda r: Role(name=r, description=ROLES_MAP.get(r)), ROLES))
        db.session.commit()

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return "<Role id: {}>".format(self.id)


users_to_roles = db.Table(
    'users_to_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), index=True, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    roles = db.relationship('Role',
                            secondary=users_to_roles,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')
    name = db.Column(db.String(64), default='go-shop-user', index=True)
    gender = db.Column(db.Boolean(), index=True)
    password_hash = db.Column(db.String(128))
    birthday = db.Column(db.Date(), default=datetime.date.today())
    phone = db.Column(db.String(32), unique=True, index=True)
    phone_confirmed = db.Column(db.Boolean(), default=False)
    records = db.relationship('Record', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def is_admin(self):
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role in self.roles:
            return True
        return False

    @property
    def is_vip(self):
        vip_role = Role.query.filter_by(name='vip').first()
        if vip_role in self.roles:
            return True
        return False

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=7200):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=expiration
        )
        return str(s.dumps({'id': self.id}), encoding="utf8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(bytes(token, encoding="utf8"))
        except (SignatureExpired, BadSignature, TypeError):
            return None, '1001'
        except BadTimeSignature:
            return None, '1002'
        else:
            return User.query.get(data['id']), '1000'

    @staticmethod
    def create_user(username, password, name=None, gender=None, birthday=None, phone=None):
        user = User(username=username,
                    password=password,
                    name=name,
                    gender=gender,
                    birthday=birthday,
                    phone=phone)
        db.session.add(user)
        db.session.commit()
        return user

    def buy_commodity(self, records):
        """
        购买商品
        :param records:JSON Obj
        :return:
        """
        record = Record(record=records,
                        u_id=self.id)
        db.session.add(record)
        db.session.commit()

    def buy_vip(self, year, month, day):
        """
        购买会员
        :param year:
        :param day:
        :param month:
        :return:
        """
        if self.is_vip:
            vip = Vip.query.filter_by(u_id=self.id).first()
            vip.end_date = datetime.date(year, month, day)
        else:
            vip_role = Role.query.filter_by(name='vip').first()
            self.roles.append(vip_role)
            vip = Vip(u_id=self.id,
                      end_date=datetime.date(year, month, day))
        db.session.add(vip)
        db.session.commit()

    def del_vip(self):
        """
        移除会员
        :return:
        """
        vip_role = Role.query.filter_by(name='vip').first()
        if vip_role in self.roles:
            self.roles.remove(vip_role)
            vip = Vip.query.filter_by(u_id=self.id).first()
            db.session.add(self)
            db.session.delete(vip)
            db.session.commit()

    def expire_vip(self):
        """
        自动判断会员到期
        :return:
        """
        vip_role = Role.query.filter_by(name='vip').first()
        if vip_role in self.roles:
            vip = Vip.query.filter_by(u_id=self.id).first()
            if vip.end_date >= datetime.date.today():
                self.roles.remove(vip_role)
                db.session.add(self)
                db.session.delete(vip)
                db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'gender': self.gender,
            'birthday': self.birthday.strftime("%Y-%m-%d"),
            'phone': self.phone,
            'create_time': self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __init__(self, username, password, name=None, gender=None, birthday=None, phone=None):
        self.username = username
        self.password = password
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.phone = phone

    def __repr__(self):
        return "<User id: {id}>".format(id=self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Vip(db.Model):
    __tabename__ = 'vip'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    start_date = db.Column(db.Date(), default=datetime.date.today())
    end_date = db.Column(db.Date())

    def __init__(self, **kwargs):
        super(Vip, self).__init__(**kwargs)

    def __repr__(self):
        return "<Vip id: {id}>".format(id=self.id)
