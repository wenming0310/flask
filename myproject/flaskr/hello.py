from flask import Flask, render_template
from flask import make_response
from flask import redirect
from flask import abort
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)
#manager = Manager(app)

#把业务逻辑和表现逻辑混在一起会导致代码难以理解和维护
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
#渲染模板
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500


if __name__ == '__main__':
    app.run(debug=True)

    #使用Flask-Script
    #manager.run()