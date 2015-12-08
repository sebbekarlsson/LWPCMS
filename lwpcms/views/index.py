from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/')
def render():
    return render_template('index.html')
