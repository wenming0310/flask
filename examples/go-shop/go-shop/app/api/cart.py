# -*- coding: utf-8 -*-

"""
cart.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_login import current_user
from flask import request, jsonify

from . import api
from extensions import cache
from .utils import token_required


@api.route('/cart/add')
def cart_add():
    cart = cache.get('cart%d' % current_user.id)
    c_id = int(request.args.get('id'))
    if cart is None:
        data = []
    else:
        data = cart
    if c_id in data:
        return jsonify({'status': False, 'msg': '您已添加过该产品,不可重复添加'})
    data.append(c_id)
    data = list(set(data))
    cache.set('cart%d' % current_user.id, data)
    return jsonify({'status': True, 'msg': '添加成功'})


@api.route('/haha')
@token_required
def haha():
    return 'haha'
