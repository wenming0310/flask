# -*- coding: utf-8 -*-

"""
commodities.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

import datetime
import os

from hashlib import md5

from . import db
from extensions import photos


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    commodities = db.relationship('Commodity', backref='tag', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)

    def __repr__(self):
        return "<Tag id: {id}>".format(id=self.id)


class Commodity(db.Model):
    __tablename__ = 'commodity'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    t_id = db.Column(db.Integer(), db.ForeignKey('tag.id'))
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    vip_price = db.Column(db.Float(), nullable=False)
    digest = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    comments = db.relationship('Comment', backref='commodity', lazy='dynamic')
    photos = db.relationship('Photo', backref='commodity', lazy='dynamic')
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now())

    def __init__(self, **kwargs):
        super(Commodity, self).__init__(**kwargs)

    def __repr__(self):
        return "<Commodity id: {id}>".format(id=self.id)


class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    record = db.Column(db.JSON())
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    pay = db.Column(db.Boolean(), default=False)

    def __init__(self, record, u_id):
        self.record = record
        self.u_id = u_id

    def __repr__(self):
        return "<Record id: {id}>".format(id=self.id)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    c_id = db.Column(db.Integer(), db.ForeignKey('commodity.id'))
    u_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    body = db.Column(db.Text(), nullable=False)
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now())

    def __init__(self, c_id, u_id, body):
        self.c_id = c_id
        self.u_id = u_id
        self.body = body

    def __repr__(self):
        return "<Comment id: {id}>".format(id=self.id)


class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    c_id = db.Column(db.Integer(), db.ForeignKey('commodity.id'))
    path = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    size = db.Column(db.Integer)
    md5_name = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    show = db.Column(db.Boolean(), default=False)
    cover = db.Column(db.Boolean(), default=False)

    @classmethod
    def has_file(cls, md5_name, c_id):
        return cls.query.filter_by(path=c_id + os.sep + md5_name).first()

    @staticmethod
    def md5_filename(filename):
        b_filename = filename
        if isinstance(filename, str):
            b_filename = bytes(filename, encoding="utf8")
        return md5(b_filename).hexdigest().upper() + '.{}'.format(filename.split('.')[-1])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': photos.url(self.path),
            'size': self.size,
            'create_time': self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __init__(self, **kwargs):
        super(Photo, self).__init__(**kwargs)

    def __repr__(self):
        return '<Photo id: {id}>'.format(id=self.id)
