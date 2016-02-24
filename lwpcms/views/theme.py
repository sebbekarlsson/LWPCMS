from flask import (
    Blueprint,
    render_template,
    abort, url_for,
    render_template_string,
    send_file,
    jsonify
)
from lwpcms.api.themes import get_activated_theme, get_themes
from lwpcms.mongo import db
import glob 
import os.path

bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/theme'
)


@bp.route('/static/<folder_name>/<file_name>')
def get_static(folder_name, file_name):
    theme = get_activated_theme()
    
    if theme is not None:
        path = '{}/static/{}/{}'.format(theme['path'], folder_name, file_name)
        mimetype = ''

        if 'css' in folder_name or 'css' in file_name:
            mimetype = 'text/css'

        elif 'image' in folder_name:
            mimtype = 'image/jpg'

        return send_file(path, mimetype=mimetype)
    else:
        return 'No activated theme', 400


@bp.route('/name/<theme_name>/<file_name>')
def get_static_1(theme_name, file_name):
    theme = get_themes(theme_name)

    if theme is not None:
        path = '{}/{}'.format(theme['path'], file_name)
        mimetype = ''

        if 'css' in file_name or 'css' in file_name:
            mimetype = 'text/css'

        elif 'image' in file_name or 'jpg' in file_name or 'png' in file_name:
            mimtype = 'image/jpg'

        return send_file(path, mimetype=mimetype)
    else:
        return 'No activated theme', 400


@bp.route('/pages/<file_name>')
def get_page(file_name):
    theme = get_activated_theme()
    
    if theme is not None:
        path = '{}/pages/{}'.format(theme['path'], file_name)
        mimetype = 'text/raw'

        return send_file(path, mimetype=mimetype)
    else:
        return 'No activated theme', 400
