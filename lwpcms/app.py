from flask import Flask

from lwpcms.views.index import bp as index_bp

from lwpcms.views.admin.admin import bp as admin_bp
from lwpcms.views.admin.publish import bp as admin_publish_bp
from lwpcms.views.admin.posts import bp as admin_posts_bp
from lwpcms.views.admin.users import bp as admin_users_bp
from lwpcms.views.admin.editUser import bp as admin_editUser_bp
from lwpcms.views.admin.modules import bp as admin_modules_bp
from lwpcms.views.admin.themes import bp as admin_themes_bp
from lwpcms.views.admin.files import bp as admin_files_bp
from lwpcms.views.admin.settings import bp as admin_settings_bp

from lwpcms.views.theme import bp as theme_bp
from lwpcms.views.api.api import bp as api_bp
from lwpcms.views.api.api_query import bp as api_query_bp
from lwpcms.views.setup import bp as setup_bp
from lwpcms.views.login import bp as login_bp

from lwpcms.api.files import is_image, file_thumbnail
from lwpcms.api.modules import call_module_event
from lwpcms.api.posts import shorten_text, get_posts, get_option, set_option, render_content
from lwpcms.api.themes import get_activated_theme
from lwpcms.api.site import is_site_demo, get_random_greeting
from lwpcms.api.user import get_current_user

from bson.objectid import ObjectId

import pymongo

import logging


app = Flask(__name__)
app.register_blueprint(setup_bp)
app.register_blueprint(index_bp)

app.register_blueprint(admin_bp)
app.register_blueprint(admin_publish_bp)
app.register_blueprint(admin_posts_bp)
app.register_blueprint(admin_users_bp)
app.register_blueprint(admin_editUser_bp)
app.register_blueprint(admin_modules_bp)
app.register_blueprint(admin_themes_bp)
app.register_blueprint(admin_files_bp)
app.register_blueprint(admin_settings_bp)

app.register_blueprint(api_bp)
app.register_blueprint(api_query_bp)
app.register_blueprint(theme_bp)
app.register_blueprint(login_bp)

app.jinja_env.globals.update(is_image=is_image)
app.jinja_env.globals.update(file_thumbnail=file_thumbnail)
app.jinja_env.globals.update(call_module_event=call_module_event)
app.jinja_env.globals.update(shorten_text=shorten_text)
app.jinja_env.globals.update(get_posts=get_posts)
app.jinja_env.globals.update(get_activated_theme=get_activated_theme)
app.jinja_env.globals.update(set_option=set_option)
app.jinja_env.globals.update(get_option=get_option)
app.jinja_env.globals.update(is_site_demo=is_site_demo)
app.jinja_env.globals.update(get_random_greeting=get_random_greeting)
app.jinja_env.globals.update(get_current_user=get_current_user)
app.jinja_env.globals.update(render_content=render_content)
app.jinja_env.globals.update(pymongo=pymongo)
app.jinja_env.globals.update(ObjectId=ObjectId)

app.secret_key = 'super secret key'

handler = logging.FileHandler('log.log')
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)
