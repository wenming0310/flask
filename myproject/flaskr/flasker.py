# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
'''
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
#app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
'''

#app.config.from_envvar(‘FLASKR_SETTINGS’, silent=True)
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

if __name__ == '__main__':

     app = Flask(__name__)
     app.run()
