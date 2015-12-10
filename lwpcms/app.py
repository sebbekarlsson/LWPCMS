from flask import Flask

from lwpcms.views.index import bp as index_bp
from lwpcms.views.admin.admin import bp as admin_bp
from lwpcms.views.setup import bp as setup_bp


app = Flask(__name__)
app.register_blueprint(setup_bp)
app.register_blueprint(index_bp)
app.register_blueprint(admin_bp)
