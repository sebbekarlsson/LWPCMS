from flask import Flask

from lwpcms.views.index import bp as index_bp
from lwpcms.views.admin.admin import bp as admin_bp
from lwpcms.views.api.api import bp as api_bp
from lwpcms.views.setup import bp as setup_bp

from lwpcms.api.files import is_image
from lwpcms.api.modules import call_module_event
from lwpcms.api.posts import shorten_text
from lwpcms.api.themes import render_stylesheet



app = Flask(__name__)
app.register_blueprint(setup_bp)
app.register_blueprint(index_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

app.jinja_env.globals.update(is_image=is_image)
app.jinja_env.globals.update(call_module_event=call_module_event)
app.jinja_env.globals.update(shorten_text=shorten_text)
app.jinja_env.globals.update(render_stylesheet=render_stylesheet)
