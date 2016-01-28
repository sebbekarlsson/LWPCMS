from flask import (
    Blueprint,
    render_template,
    abort, url_for,
    render_template_string,
    send_file,
    jsonify
)
from lwpcms.api.themes import get_activated_theme
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
