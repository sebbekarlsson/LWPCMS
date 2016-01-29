from flask import (
    Blueprint,
    render_template,
    abort, url_for,
    render_template_string,
    redirect
)
from lwpcms.api.themes import get_activated_theme
from lwpcms.mongo import db
from lwpcms.api.posts import set_option, get_option
import glob 


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)


@bp.route('/', defaults={'template_name': 'index.html'})
@bp.route('/<template_name>')
def render(template_name):

    if not get_option('initialized'):
        return redirect('/setup')


    if (template_name is None):
        template_name = 'index.html'

    theme = get_activated_theme()
    
    if theme is not None:
        page_path = 'lwpcms/{}/pages/{}'.format(theme['path'], template_name)

        return render_template_string(open(page_path).read())
    else:
        return render_template('index.html')
