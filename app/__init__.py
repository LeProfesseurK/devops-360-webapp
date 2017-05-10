#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import git

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

################################################################################
### Override with specific settings based on the FLASK_ENV env var
################################################################################

if "FLASK_ENV" in os.environ:
    if os.environ["FLASK_ENV"] == 'prod':
        app.config.from_object('app.config.prod.ProductionConfig')
    else:
        app.config.from_object('app.config.config.DevelopmentConfig')
else:
    app.config.from_object('app.config.config.DevelopmentConfig')

################################################################################
### Extra Jinja Filters
################################################################################

@app.template_filter()
def display_beer_icon_filter(value):
    escaped_beer_name = value.lower().replace(" ", "_")

    if os.path.isfile("%s/static/img/beers/%s.png" %(app.config['BASE_DIR'], escaped_beer_name)):
      return url_for('static', filename="img/beers/%s.png" %(escaped_beer_name))
    else:
      return url_for('static', filename='img/beers/unknown.png')

app.jinja_env.filters['display_beer_icon'] = display_beer_icon_filter

################################################################################
### Code revision
################################################################################

git_repo = git.Repo(search_parent_directories=True)
git_sha = git_repo.head.object.hexsha[:7]
git_ref = str(git_repo.head.reference) if git_repo.head else '-'

app.config['GIT_REVISION'] = git_sha
app.config['GIT_TAG'] = git_ref

################################################################################
### Backend Setup
################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://%s:%s@%s/%s" % (app.config['MYSQL_USER'],
    app.config['MYSQL_PWD'],
    app.config['MYSQL_SERVER'],
    app.config['MYSQL_DB'])

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

################################################################################
# http://stackoverflow.com/questions/13809890/flask-context-processors-functions
################################################################################

@app.context_processor
def include_server_info():
    server_name, git_revision, git_tag = request.host.split(':')[0], app.config['GIT_REVISION'], app.config['GIT_TAG']

    def get_server_name():
        return server_name

    def get_git_revision():
        return git_revision

    def get_git_tag():
        return git_tag

    def get_db_connection_string():
        m = re.search('Engine\((.+)\)', str(db.engine))
        db_connection_string = m.group(1).split('?')[0]
        try:
            db.execute("VERSION()")
            return db_connection_string
        except:
            return db_connection_string

    def get_db_connection_state():
        try:
            db.engine.connect()
            return True
        except:
            return False


    return dict(get_server_name=get_server_name,
        get_git_revision=get_git_revision,
        get_git_tag=get_git_tag,
        get_db_connection_string=get_db_connection_string,
        get_db_connection_state=get_db_connection_state)


################################################################################
# Blueprints registration
################################################################################

from app.beerbattle.controllers import beerbattle
from app.heartbeat.controllers import heartbeat
from app.info.controllers import info

app.register_blueprint(beerbattle)
app.register_blueprint(heartbeat)
app.register_blueprint(info)

@app.route('/', methods=['GET'])
def index(error=None):
  return redirect(url_for('beerbattle.display'))

################################################################################
# Global errors handling
################################################################################

if not app.config['DEBUG']:
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('error.html', error=str(error), code=500, ), 500

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error.html', error=str(error), code=404), 404

    @app.errorhandler(Exception)
    def exception_handler(error):
        return render_template('error.html', error=error)