from flask import Flask

from lwpcms.views.index import bp as index_bp
from lwpcms.views.admin.admin import bp as admin_bp
from lwpcms.views.theme import bp as theme_bp
from lwpcms.views.api.api import bp as api_bp
from lwpcms.views.setup import bp as setup_bp
from lwpcms.views.login import bp as login_bp

from lwpcms.api.files import is_image
from lwpcms.api.modules import call_module_event
from lwpcms.api.posts import shorten_text, get_posts, get_option, set_option
from lwpcms.api.themes import get_activated_theme

import pymongo


app = Flask(__name__)
app.register_blueprint(setup_bp)
app.register_blueprint(index_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)
app.register_blueprint(theme_bp)
app.register_blueprint(login_bp)

app.jinja_env.globals.update(is_image=is_image)
app.jinja_env.globals.update(call_module_event=call_module_event)
app.jinja_env.globals.update(shorten_text=shorten_text)
app.jinja_env.globals.update(get_posts=get_posts)
app.jinja_env.globals.update(get_activated_theme=get_activated_theme)
app.jinja_env.globals.update(set_option=set_option)
app.jinja_env.globals.update(get_option=get_option)
app.jinja_env.globals.update(pymongo=pymongo)

app.secret_key = 'super secret key'
