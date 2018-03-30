# -*- coding: utf-8 -*-

"""
users.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask_wtf import FlaskForm
from flask import redirect, url_for, request
from wtforms import StringField, BooleanField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    target = request.args.get('next')
    if is_safe_url(target):
        return target
    else:
        return None


class RedirectForm(FlaskForm):
    next_url = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next_url.data:
            self.next_url.data = get_redirect_target() or ''

    def redirect(self, endpoint='main.index', **values):
        if self.next_url.data and is_safe_url(self.next_url.data):
            return redirect(self.next_url.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class RegisterForm(FlaskForm):
    username = StringField(label='用户名',
                           validators=[DataRequired('请输入用户名'),
                                       Length(1, 32, '用户名太长'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '必须字母开头，只可以包含数字、字母、小数点和下划线')])
    password = PasswordField(label='密码',
                             validators=[DataRequired('请输入密码'),
                                         Length(6, 32, '请输入6-32位密码')])
    confirm = PasswordField(label='再次输入',
                            validators=[DataRequired('请输入密码'),
                                        EqualTo('password', '两次输入不一样')])
    captcha = StringField(label='验证码',
                          validators=[DataRequired('请输入验证码')])
    submit = SubmitField(label='注册')


class LoginForm(RedirectForm):
    username = StringField(label='用户名',
                           validators=[DataRequired('请输入用户名')])
    password = PasswordField(label='密码',
                             validators=[DataRequired('请输入密码')])
    remember = BooleanField(label='记住我')
    submit = SubmitField(label='登录')


class AdminLoginForm(RedirectForm):
    username = StringField(label='用户名',
                           validators=[DataRequired('请输入用户名')])
    password = PasswordField(label='密码',
                             validators=[DataRequired('请输入密码')])
    submit = SubmitField(label='登录')

