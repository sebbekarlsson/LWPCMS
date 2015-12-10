from flask import Blueprint, render_template, abort, request

from lwpcms.forms import SetupForm


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/setup', methods=['POST', 'GET'])
def render():
    form = SetupForm(csrf_enabled=False)

    return render_template('setup.html', form=form)
