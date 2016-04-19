""" This route is used for logging in to the site/application. """
from flask import Blueprint, render_template, abort, request, redirect, session

from lwpcms.forms import LoginForm
from lwpcms.api.posts import set_option, get_option
from lwpcms.api.user import login_user


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/login', methods=['POST', 'GET'])
def render():
    form = LoginForm(csrf_enabled=False)
    msg = None

    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        if login_user(user_name, password):
            return redirect('/admin')
        else:
            msg = 'Wrong password or username'

    return render_template('login.html', form=form, msg=msg)


@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['user_id']

    return redirect('/')
