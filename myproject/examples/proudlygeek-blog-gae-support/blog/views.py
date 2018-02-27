# -*- coding: utf-8 -*-
"""

    blog.views
    ~~~~~~~~~~~~~~~~~~

    This module handles views by using
    flask's app.route() decorator.

    :copyright: (c) 2010 by Gianluca Bargelli.
    :license: MIT License, see LICENSE for more details.


"""

from flask import Flask, request, session, g, redirect, \
     render_template, abort, flash, url_for

app = Flask(__name__)
app.config.from_pyfile('../config.cfg')
# Loading the Data Abstract Layer object
from db import factory
data_layer = factory(app.config['PLATFORM'])

from helpers import check_password_hash, slugify_entry, \
     fill_entries, entry_pages, unpack_pages, split_pages, \
     fill_author, fill_tags, fill_markdown_content, \
     generate_page_title, make_external, random_logo

from werkzeug.contrib.atom import AtomFeed

import datetime
import config


@app.before_request
def before_request():
    """
    Connects to the database before each request and
    looks up the current user.
    """
    g.db = data_layer.connect_db()
    g.user = None 
    
    if 'user_id' in session:
        g.user = data_layer.load_user_profile(session['user_id'])


@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    data_layer.close()
    return response


@app.route('/blog')
@app.route('/blog/tags/<tagname>')
def list_entries(tagname=None):
    """
    Returns a list of entries in the form of pages containing
    MAX_PAGE_ENTRIES entries;
    the default page argument, being ``1'', refers to the latest
    MAX_PAGE_ENTRIES entries.

    Optionally, this method accepts a tagname for tag filtering.
    """
    try:
        page = int(request.args['page'])
        if page <= 0:
            page = 1
    except:
        page = 1

    # Calculate the right offset
    offset = app.config['MAX_PAGE_ENTRIES']*(page-1)
    
    # Obtain entries and num_entries
    entries, num_entries = data_layer.get_entries(tagname, offset)

    # This happens when trying to access a non-existent page
    if len(entries) == 0 and page !=1: 
        abort(404)

    # Splitting pages
    splitted_pages = unpack_pages(split_pages(page, entry_pages(num_entries)))
    
    # Generating title
    title = generate_page_title(tagname)

    # Jinja2 render
    return render_template("list_entries.html",
                            actual_page=page,
                            entries=entries,
                            pages=splitted_pages,
                            title=title)


@app.route('/blog/articles/<int:year>/<int:month>/<int:day>/<title>')
def view_entry(year, month, day, title):
    """Retrieves an article by date and title."""
    try:
        entry_date = datetime.date(year, month, day)
    except:
        abort(400)

    entry = data_layer.get_entry(title=title, entry_date=entry_date)

    if entry is None:
        abort(404)
    else:
        return render_template('list_entries.html', entries=[entry],
                                                    title=entry['title'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate a user into the application given his credentials."""
    error = None
    if request.method == 'POST':
        user = data_layer.get_user(request.form['username'])

        if user is None:
            error = 'Invalid username'

        elif not check_password_hash(request.form['password'], \
                                     user['password']):
            error = 'Invalid password'

        else:
            session['user_id'] = user['id']
            flash('You were logged in')
            return redirect(url_for('list_entries'))

    # If the request is GET then return the login form
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logout the current user."""
    session.pop('user_id', None)
    flash("You were logged out")
    return redirect(url_for('list_entries'))


@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    """Adds a new entry."""
    if g.user:
        errors = []
        if request.method == 'POST':

            if request.form['title'] == '':
                errors.append('No title supplied')

            if request.form['entry_text'] == '':
                errors.append('Message body is empty')

            if (errors == []):
                entry_text = request.form['entry_text']

                if request.form['img_url']:
                    img_string = """<img src = "%s" class = "%s"/>""" % (request.form['img_url'], request.form['img_align'])
                    entry_text = img_string + entry_text

                # Duck Typing (Insert or Update)
                try:
                    entry_id = int(request.form['entry_id'])
                except KeyError:
                    entry_id = None

                if entry_id:
                    data_layer.update_entry(
                            entry_id=entry_id,
                            title=request.form['title'],
                            text=entry_text,
                            tags=request.form['tags'])
                    flash('Entry edited.')
                else:
                    data_layer.insert_entry(
                         title=request.form['title'],
                         text=entry_text,
                         owner=g.user['id'],
                         tags=request.form['tags'])
                    flash('Entry added.')
                
                return redirect(url_for('list_entries'))

        return render_template('add_entry.html', errors=errors)

    return redirect(url_for('list_entries'))


@app.route('/edit/<int:entry_id>')
def edit_entry(entry_id):
    """Displays a page for editing an existing entry."""
    if g.user:
        entry = data_layer.get_entry_by_id(entry_id)

        if entry is None:
            return abort(404)
        else:
            return render_template('edit_entry.html', entry=entry)
    else:
        return redirect(url_for('list_entries'))


@app.route('/projects')
def show_projects():
    """Simply reroute to list_entries."""
    return list_entries(tagname='project')


@app.route('/about')
def show_about():
    """A simple, static page containing infos about me :)"""
    try:
        f = app.open_resource('static/pages/about.md')
        about_txt = f.read()
    except IOError:
        pass

    entry = dict(body=about_txt)

    fill_markdown_content(entries=[entry], gen_readmore=False)
    return render_template('about.html', entry=entry)


@app.route('/admin')
def admin_panel():
    """Display a panel for administration purposes."""
    if g.user is not None:
        if g.user['role_name'] == 'administrator':
            entries_list = data_layer.query_db(
                           """
                           SELECT id, user_id_FK, slug, title 
                           FROM entry
                           """)
            fill_tags(entries_list)
            fill_author(entries_list)

            return render_template('admin.html', entries=entries_list)

        else:
            return redirect(url_for('list_entries'))
    else:
        return redirect(url_for('login'))


@app.route('/recent.atom')
def recent_feed():
    """
    Returns the most recent entries displayed 
    as RSS Atom feeds."""
    feed = AtomFeed("""Proudlygeek's babblings & ramblings""",
                    feed=request.url,
                    url=request.url_root)
    
    entries = data_layer.get_recent_entries(15)
    # Build feed info
    for entry in entries:
        update_date = entry['last_date']
        publish_date = entry['creation_date']
        # Building the entry's relative path
        rel_path = url_for('view_entry', 
                           year=publish_date.year,
                           month=publish_date.month,
                           day=publish_date.day,
                           title=entry['slug'])

        feed.add(entry['title'],
                 unicode(entry['content']),
                 content_type='html',
                 author=entry['author'],
                 # Absolute URL = BASE+REL
                 url=make_external(rel_path),
                 updated=update_date,
                 published=publish_date)

    return feed.get_response()


@app.route('/')
def show_home():
    """ This is the main page."""
    return render_template('home.html', logo_url=random_logo())


if __name__ == "__main__":
    app.run()
