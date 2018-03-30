# -*- coding: utf-8 -*-

"""
utils.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from functools import wraps
from flask import jsonify, request

from ..models.users import User


def json_page_response(pagination):
    ret = dict(data=pagination.items,
               total_num=pagination.pages,
               current_num=pagination.page,
               prev_num=pagination.prev_num,
               next_num=pagination.next_num)
    return jsonify(ret)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-USERToken", None)
        if token is None:
            return jsonify({'status': False, 'msg': 'missing token'})
        user, code = User.verify_auth_token(token)
        if user is None:
            if code == '1001':
                return jsonify({'status': False, 'msg': 'token error'})
            if code == '1002':
                return jsonify({'status': False, 'msg': 'token expired'})
        return func(*args, **kwargs)

    return decorated
