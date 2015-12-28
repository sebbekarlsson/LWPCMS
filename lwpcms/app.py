from flask import Flask

from lwpcms.views.index import bp as index_bp
from lwpcms.views.admin.admin import bp as admin_bp
from lwpcms.views.api.api import bp as api_bp
from lwpcms.views.setup import bp as setup_bp

from lwpcms.api.files import is_image

from .models import initialize_database


app = Flask(__name__)
app.register_blueprint(setup_bp)
app.register_blueprint(index_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

app.jinja_env.globals.update(is_image=is_image)

initialize_database()
