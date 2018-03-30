# -*- coding: utf-8 -*-

"""
views.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

import os

from flask import render_template, current_app, redirect, url_for, flash, request, abort
from flask_login import login_required, logout_user, login_user, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity

from . import admin, admin_log
from ..models import db
from ..models.users import admin_permission, User, Role
from ..models.commodities import Commodity, Tag, Photo
from ..forms.users import AdminLoginForm
from ..forms.commodity import PhotoForm, CommodityForm
from extensions import photos


@admin.route('/')
@login_required
@admin_permission.require(403)
def index():
    return render_template('admin/index.html',
                           title='后台管理系统')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.verify_password(form.password.data):
            if u.is_admin:
                login_user(u, True)
                identity_changed.send(current_app._get_current_object(), identity=Identity(u.id))
                return form.redirect('admin.index')
            else:
                flash('你不是管理员', 'warning')
        else:
            flash('用户名或密码错误', 'error')
    return render_template('admin/login.html',
                           title='后台登录',
                           form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('admin.login'))


@admin.route('/commodity')
@admin.route('/commodity/tag/<tag_id>')
@login_required
@admin_permission.require(403)
def all_commodity(tag_id=None):
    page = request.args.get('page', 1, type=int)
    tag = None
    if tag_id:
        tag = Tag.query.get_or_404(tag_id)
        pagination = tag.commodities.paginate(page,
                                              per_page=10,
                                              error_out=False)
    else:
        pagination = Commodity.query.paginate(page,
                                              per_page=10,
                                              error_out=False)
    commodities = pagination.items
    return render_template('admin/commodity/index.html',
                           commodities=commodities,
                           pagination=pagination,
                           tag=tag)


@admin.route('/commodity/detail/<c_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(403)
def commodity_detail(c_id=None):
    c = Commodity.query.get_or_404(c_id)
    photo_form = PhotoForm()
    commodity_form = CommodityForm(data=dict(name=c.name,
                                             price=c.price,
                                             vip_price=c.vip_price,
                                             digest=c.digest,
                                             description=c.description))
    commodity_form.tags.data = c.tag
    if commodity_form.validate_on_submit():
        c.name = commodity_form.name.data
        c.tag = commodity_form.tags.data
        c.price = commodity_form.price.data
        c.vip_price = commodity_form.vip_price.data
        c.digest = commodity_form.digest.data
        c.description = commodity_form.description.data
        db.session.add(c)
        db.session.commit()
        redirect(url_for('admin.commodity_detail', c_id=c_id))

    return render_template('admin/commodity/detail.html',
                           commodity=c,
                           photo_form=photo_form,
                           commodity_form=commodity_form)


@admin.route('/commodity/detail/<c_id>/photo/upload', methods=['GET', 'POST'])
@login_required
@admin_permission.require(403)
def commodity_upload(c_id):
    photo_form = PhotoForm()
    if photo_form.validate_on_submit():
        upload_files = photo_form.files.raw_data
        for f in upload_files:
            real_name = str(f.filename)
            f.filename = Photo.md5_filename(real_name)
            if Photo.has_file(f.filename, c_id):
                flash(u'上传失败，{} 已经存在'.format(real_name), category='warning')
            elif not photos.file_allowed(storage=f, basename=real_name):
                flash(u'上传失败，{} 类型不支持'.format(real_name), category='error')
            else:
                try:
                    path = photos.save(f, folder=c_id)
                    f_stat = os.stat(os.path.join(current_app.config['UPLOADED_PHOTO_DEST'], path))
                    new_file = Photo(path=path,
                                     name=real_name,
                                     size=f_stat.st_size,
                                     c_id=c_id,
                                     md5_name=f.filename)
                    db.session.add(new_file)
                except:
                    db.session.rollback()
                    flash(u'上传失败，{} 存储错误'.format(real_name), category='error')
                else:
                    db.session.commit()

    return redirect(url_for('admin.commodity_detail', c_id=c_id))


@admin.route('/commodity/detail/<c_id>/photo/delete/<p_id>')
@login_required
def commodity_delete(c_id, p_id):
    f = Photo.query.get_or_404(p_id)
    file_local_path = os.path.join(current_app.config['UPLOADED_PHOTO_DEST'], f.path)
    if os.path.isfile(file_local_path):
        try:
            db.session.delete(f)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            os.remove(file_local_path)
    else:
        db.session.delete(f)
        db.session.commit()
    return redirect(url_for('admin.commodity_detail', c_id=c_id))


@admin.route('/commodity/detail/<c_id>/photo/cover/<p_id>')
@login_required
def commodity_cover(c_id, p_id):
    f = Photo.query.get_or_404(p_id)
    f.cover = False if f.cover else True
    db.session.add(f)
    db.session.commit()

    return redirect(url_for('admin.commodity_detail', c_id=c_id))


@admin.route('/commodity/detail/<c_id>/photo/show/<p_id>')
@login_required
def commodity_show(c_id, p_id):
    f = Photo.query.get_or_404(p_id)
    f.show = False if f.show else True
    db.session.add(f)
    db.session.commit()

    return redirect(url_for('admin.commodity_detail', c_id=c_id))


@admin.route('/users')
@admin.route('/users/<role_id>')
@login_required
@admin_permission.require(403)
def all_user(role_id=None):
    page = request.args.get('page', 1, type=int)
    role = None
    if role_id:
        role = Role.query.get_or_404(role_id)
        pagination = role.users.paginate(page,
                                         per_page=10,
                                         error_out=False)
    else:
        pagination = User.query.paginate(page,
                                         per_page=10,
                                         error_out=False)
    users = pagination.items
    return render_template('admin/user/index.html',
                           users=users,
                           pagination=pagination,
                           role=role)
