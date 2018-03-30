# -*- coding: utf-8 -*-

"""
views.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_sqlalchemy import get_debug_queries
from flask import current_app, render_template, request, g, session

from . import main, main_log
from ..log import slow_query_log
from ..models.commodities import Tag, Commodity, Comment
from ..models.users import Role


@main.before_app_request
def before_request():
    g.tags = Tag.query.all()
    g.roles = Role.query.all()


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            slow_log = 'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' \
                       % (query.statement, query.parameters, query.duration, query.context)
            slow_query_log.warning(slow_log)
    return response


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Commodity.query.paginate(page,
                                          per_page=8,
                                          error_out=False)
    commodities = pagination.items
    return render_template('index.html',
                           title='Go Shop',
                           commodities=commodities,
                           pagination=pagination)


@main.route('/commodity/<c_id>')
def item(c_id=None):
    commodity = Commodity.query.get_or_404(c_id)
    return render_template('item.html',
                           title='Go Shop',
                           commodity=commodity)


@main.route('/tag/<t_id>')
def tag(t_id=None):
    t = Tag.query.get_or_404(t_id)
    page = request.args.get('page', 1, type=int)
    pagination = t.commodities.paginate(page,
                                        per_page=6,
                                        error_out=False)
    commodities = pagination.items
    return render_template('tag.html',
                           title='Go Shop',
                           tag=t,
                           commodities=commodities,
                           pagination=pagination)
