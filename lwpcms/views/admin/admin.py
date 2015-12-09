from flask import Blueprint, render_template, abort

import glob

import json


bp = Blueprint(
    __name__, __name__,
    template_folder='templates'
)

@bp.route('/admin')
def render():
    side_nav_buttons = []

    for json_file in glob.glob('lwpcms/static/shards/admin/side_nav/*.json'):
        with open(json_file) as file:
            side_nav_buttons += json.loads(file.read())['buttons']
            
    
    return render_template('admin.html', side_nav_buttons=side_nav_buttons)
