""" This route is used for administrating themes in the admin panel. """
from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.admin import get_sidenav
from lwpcms.api.themes import get_themes

from lwpcms.mongo import db
import pymongo as pymongo
from bson.objectid import ObjectId

import os
import json
import shutil


bp = Blueprint(
    __name__, __name__,
    template_folder=os.path.dirname(os.path.dirname(__file__)) + '/../templates/admin',
    url_prefix='/admin'
)

@bp.route('/themes', methods=['POST', 'GET'])
@login_required
def render_themes():
    sidenav = get_sidenav()

    if request.method == 'POST':
        if 'theme_path' in request.form:
            theme_path = request.form['theme_path']

            with open('lwpcms/{}/theme.json'.format(theme_path)) as file:
                data = json.loads(file.read())
                theme = data['theme']
                
                if 'activated' in theme:
                    activated = theme['activated']
                else:
                    activated = False

            
                if activated:
                    activated = False
                else:
                    activated = True

                theme['activated'] = activated

                with open('lwpcms/{}/theme.json'.format(theme_path), 'w') as jsonFile:
                    jsonFile.write(
                            json.dumps(
                                data,
                                sort_keys=True,indent=4,
                                separators=(',', ': ')
                                )
                            )

                    abs_templates_path = os.path.abspath('lwpcms/templates')
                    
                    if os.path.isdir('{}/theme'.format(abs_templates_path)):
                        shutil.rmtree('{}/theme'.format(abs_templates_path))

                    return redirect('/admin/themes')

    themes = get_themes()

    return render_template('themes.html', sidenav=sidenav, themes=themes)

