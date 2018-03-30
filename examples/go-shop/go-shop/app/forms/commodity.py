# -*- coding: utf-8 -*-

"""
commodity.py
~~~~~~~~~~~~~~~~~~~~

introduce

"""

from flask_wtf.form import FlaskForm
from wtforms import SubmitField, FileField, StringField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models.commodities import Tag


class PhotoForm(FlaskForm):
    files = FileField(label='选择照片', validators=[DataRequired()])
    submit = SubmitField(label='上传')


class CommodityForm(FlaskForm):
    name = StringField(label='商品名称', validators=[DataRequired()])
    tags = QuerySelectField(label='分类标签',
                            id='tags',
                            query_factory=lambda: Tag.query.all(),
                            get_pk=lambda x: x.id,
                            get_label=lambda x: x.name,
                            allow_blank=False)
    price = StringField(label='普通价格', validators=[DataRequired()])
    vip_price = StringField(label='会员价格', validators=[DataRequired()])
    digest = StringField(label='商品摘要', validators=[DataRequired()])
    description = TextAreaField(label='商品描述', validators=[DataRequired()])
    submit = SubmitField(label='提交')
