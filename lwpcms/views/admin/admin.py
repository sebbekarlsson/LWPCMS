from flask import Blueprint, render_template, abort


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/admin')
def render():
    return render_template('index.html')
