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
import os
import os.path
import ntpath


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
        pages_path = 'lwpcms/{}/pages'.format(theme['path'])
        abs_pages_path = os.path.abspath(pages_path)
        abs_templates_path = os.path.abspath('lwpcms/templates')
        page_path = '{}/{}'.format(pages_path, template_name)

        if not os.path.exists('lwpcms/templates/theme'):
            os.makedirs('lwpcms/templates/theme')

        for filename in glob.iglob('{}/*.html'.format(abs_pages_path)):
            linked_file = '{}/theme/{}'.format(abs_templates_path, ntpath.basename(filename))

            if not os.path.islink(linked_file):
                os.symlink(filename, linked_file)

        return render_template_string(open(page_path).read())
    else:
        return render_template('index.html')
