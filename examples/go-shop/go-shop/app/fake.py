# -*- coding: utf-8 -*-

"""
fake.py
~~~~~~~~~~~~~~~~~~~~

创建一些虚拟数据，用来测试

"""

import random
import forgery_py

from sqlalchemy.exc import IntegrityError

from .models import db
from .models.users import User, Role
from .models.commodities import Commodity, Tag, Comment


def user_generate_fake(count=3):
    """
    普通用户
    :param count:
    :return:
    """
    random.seed()
    for i in range(count):
        u = User(username=forgery_py.internet.user_name(True),
                 password='123456',
                 name=forgery_py.internet.user_name(),
                 gender=random.choice([True, False]),
                 birthday=forgery_py.date.date(past=True),
                 phone=forgery_py.address.phone())
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def vip_user_generate_fake(count=3):
    """
    VIP用户
    :param count:
    :return:
    """
    random.seed()
    for i in range(count):
        u = User(username=forgery_py.internet.user_name(True),
                 password='123456',
                 name=forgery_py.internet.user_name(),
                 gender=random.choice([True, False]),
                 birthday=forgery_py.date.date(past=True),
                 phone=forgery_py.address.phone())
        db.session.add(u)
        u.buy_vip(2018, 12, 31)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def admin_user_generate_fake(count=3):
    """
    管理员
    :param count:
    :return:
    """
    random.seed()
    admin_role = Role.query.filter_by(name='admin').first()
    for i in range(count):
        u = User.create_user(username=forgery_py.internet.user_name(True),
                             password='123456',
                             name=forgery_py.internet.user_name(),
                             gender=random.choice([True, False]),
                             birthday=forgery_py.date.date(past=True),
                             phone=forgery_py.address.phone())
        u.roles.append(admin_role)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def tag_generate_fake(count=5):
    """
    类别
    :param count:
    :return:
    """
    random.seed()
    for i in range(count):
        t = Tag(name=forgery_py.internet.user_name())
        db.session.add(t)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def commodity_generate_fake(count=20):
    """
    商品
    :param count:
    :return:
    """
    random.seed()
    tags = Tag.query.all()
    for i in range(count):
        c = Commodity(name=forgery_py.name.first_name(),
                      t_id=random.choice(range(1, len(tags))),
                      price=round(random.random() * 100, 2),
                      vip_price=round(random.random() * 100, 2),
                      digest=forgery_py.address.street_address(),
                      description=forgery_py.address.street_address())
        db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def comment_generate_fake():
    """
    评论
    :return:
    """
    random.seed()
    users = User.query.all()
    commodities = Commodity.query.all()
    for u in users:
        for c in commodities:
            comment = Comment(c_id=c.id,
                              u_id=u.id,
                              body=forgery_py.address.street_address())
            db.session.add(comment)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
