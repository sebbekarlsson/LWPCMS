from flask import Blueprint, render_template, abort, request, redirect

from lwpcms.forms import SetupForm
from lwpcms.api.posts import set_option, get_option


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/setup', methods=['POST', 'GET'])
def render():
    if get_option('initialized') is not None:
        return redirect('/')

    form = SetupForm(csrf_enabled=False)

    if form.validate_on_submit():
        site_name = form.site_name.data
        password = form.password.data

        set_option('site_name', site_name)
        set_option('site_password', password)
        set_option('initialized', 'True')

        return redirect('/')

    return render_template('setup.html', form=form)
