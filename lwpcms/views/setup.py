from flask import Blueprint, render_template, abort, request, redirect

from lwpcms.forms import SetupForm
from lwpcms.api.posts import set_option, get_option
from lwpcms.api.user import register_user


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
        user_name = form.user_name.data
        password = form.password.data
        demo = form.demo.data

        set_option('site_name', site_name)
        set_option('site_demo', demo)
        set_option('site_filespage_limit', 128)
        set_option('site_postspage_limit', 128)

        register_user(
                    name=user_name,
                    password=password
                )

        set_option('initialized', 'True')

        return redirect('/')

    return render_template('setup.html', form=form)
