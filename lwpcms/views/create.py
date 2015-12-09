from flask import Blueprint, render_template, abort, request


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/create')
def render():
    return render_template('create.html')
