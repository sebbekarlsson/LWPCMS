from flask import Blueprint, render_template, abort

import json


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/admin')
def render():
    with open('lwpcms/static/shards/admin_side_nav.json') as file:
        side_nav_buttons = json.loads(file.read())
    
    return render_template('admin.html', side_nav_buttons=side_nav_buttons)
