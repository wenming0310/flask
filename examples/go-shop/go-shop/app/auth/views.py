# -*- coding: utf-8 -*-

"""
views.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

import os
import random

from io import BytesIO
from captcha.image import ImageCaptcha
from flask_login import login_required, login_user, logout_user, current_user
from flask import make_response, session, render_template, url_for, redirect, flash, current_app, jsonify
from flask_principal import identity_changed, Identity, AnonymousIdentity

from . import auth
from ..models import db
from ..models.users import User
from ..models.commodities import Commodity
from ..forms.users import RegisterForm, LoginForm
from extensions import cache

CHARS = list(set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
FONT_PATH = os.path.join(os.path.abspath(os.path.curdir), os.sep.join(['app', 'static', 'i', 'consola.ttf']))


@auth.route('/captcha/')
def captcha():
    c_str = ''.join(random.sample(CHARS, 4))
    img = ImageCaptcha(width=100, height=60, fonts=[FONT_PATH])
    image = img.create_captcha_image(c_str, color='#dc3545', background='#20c997')
    buf = BytesIO()
    image.save(buf, 'JPEG')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    session['captcha'] = c_str
    return response


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        captcha_str = session.get('captcha').upper()
        if captcha_str == form.captcha.data.upper():
            u = db.session.query(User).filter_by(username=form.username.data).first()
            if u:
                flash('用户名已被使用', 'warning')
            else:
                User.create_user(username=form.username.data,
                                 password=form.password.data)
                flash('注册成功,请登录', 'success')
                return redirect(url_for('auth.login'))
        else:
            flash('验证码错误', 'error')

    return render_template('auth/register.html',
                           title='注册',
                           form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.verify_password(form.password.data):
            login_user(u, form.remember.data)
            identity_changed.send(current_app._get_current_object(), identity=Identity(u.id))
            return form.redirect()
        else:
            flash('用户名或密码错误', 'error')
    return render_template('auth/login.html',
                           title='登录',
                           form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('auth.login'))


@auth.route('/cart')
@auth.route('/cart/<modify>')
@login_required
def cart(modify=None):
    carts = cache.get('cart%d' % current_user.id)
    if carts:
        commodities = Commodity.query.filter(Commodity.id.in_(carts)).all()
    else:
        commodities = None
    if modify == 'add':
        pass
    return render_template('auth/cart/index.html',
                           title='购物车',
                           commodities=commodities)


@auth.route('/token')
@login_required
def token():
    t = current_user.generate_auth_token()
    return jsonify({"token": t})
