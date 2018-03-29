from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'None'
#app.config['SECRET_KEY'] = 'hard to guess string'
#app.config['WTF_CSRF_ENABLED'] = 'False'

bootstrap = Bootstrap(app)
moment = Moment(app)
#manager = Manager(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# 把业务逻辑和表现逻辑混在一起会导致代码难以理解和维护
"""
#响应http://127.0.0.1:5000/，返回Hello World!
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
#响应http://127.0.0.1:5000/，返回Bad Request
'''
@app.route('/')
def index():
    return '<h1>Bad Request</h1>', 400
'''
#创建了一个响应对象，然后设置了 cookie
'''
@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
'''
#一种名为重定向的特殊响应类型
'''
@app.route('/')
def index():
    redirect('http://www.example.com')
    #redirect('http://www.baidu.com')
'''

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s!</h1>' % user.name
'''
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name
'''
"""
# 使用渲染模板
'''
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
'''
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name, current_time=datetime.utcnow())
'''
#重新定向
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name!=form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#D:\CC++C#Code
if __name__ == '__main__':
    app.run()

    #使用Flask-Script
    #manager.run()