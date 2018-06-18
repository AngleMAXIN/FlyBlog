# /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from flask_mongoengine import MongoEngine
from flaskext.markdown import Markdown
from flask_debugtoolbar import DebugToolbarExtension
from config import config

db = MongoEngine()
mail = Mail()
cache = Cache()
login_manager = LoginManager()
debug_tool = DebugToolbarExtension()
login_manager.session_protection = 'strong'

login_manager.login_view = 'user.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.debug = True
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    Markdown(app)
    debug_tool.init_app(app)

    from .main import main as main_blueprint
    from .admin import admin as admin_blueprint
    from .user import user as user_blueprint
    from .data import data as data_blueprint
    from .api_v1 import api_v1 as api_v1_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(data_blueprint, url_prefix='/data')
    app.register_blueprint(api_v1_blueprint, url_prefix='/api_v1')

    return app
