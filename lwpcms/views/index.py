from flask import (
        Blueprint,
        render_template,
        abort, url_for,
        render_template_string,
        redirect,
        request
        )
from lwpcms.api.themes import get_activated_theme
from lwpcms.mongo import db
from lwpcms.api.posts import set_option, get_option
from lwpcms.api.modules import call_module_event
from lwpcms.api.constants import hooks
import glob
import os
import os.path
import ntpath


bp = Blueprint(
        __name__, __name__,
        template_folder='templates'
        )


@bp.route('/', defaults={'template_name': 'index.html'}, methods=['POST', 'GET'])
@bp.route('/<template_name>', methods=['POST', 'GET'])
def render(template_name):

    package = {
            'request_get': request.args,
            'request_post': request.form,
            'request_body': request.get_data(),
            'request_unknown': request.stream.read()
            }

    if not get_option('initialized'):
        return redirect('/setup')


    if template_name is None:
        template_name = 'index.html'

    theme = get_activated_theme()

    if theme is not None:
        pages_path = 'lwpcms/{}/pages'.format(theme['path'])
        abs_pages_path = os.path.abspath(pages_path)
        abs_templates_path = os.path.abspath('lwpcms/templates')
        page_path = '{}/{}'.format(pages_path, template_name)

        if not os.path.exists('{}/theme'.format(abs_templates_path)):
            os.makedirs('{}/theme'.format(abs_templates_path))

        for filename in glob.iglob('{}/*.html'.format(abs_pages_path)):
            linked_file = '{}/theme/{}'.format(abs_templates_path, ntpath.basename(filename))
            
            if os.path.islink(linked_file):
                os.unlink(linked_file)

            os.symlink(filename, linked_file)

        call_module_event(hooks['site_request'], {'package': package})
        
        if not os.path.isfile(page_path):
            return render_template(
                    'error.html',
                    error='This page does not exist'
                    ), 404

        return render_template_string(open(page_path).read(), package=package)
    else:
        return render_template('index.html')
