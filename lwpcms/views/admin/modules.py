from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.admin import get_sidenav
from lwpcms.api.modules import call_module_event, get_modules

from lwpcms.mongo import db
import pymongo as pymongo
from bson.objectid import ObjectId

import os

import json


bp = Blueprint(
    __name__, __name__,
    template_folder=os.path.dirname(os.path.dirname(__file__)) + '/../templates/admin',
    url_prefix='/admin'
)

@bp.route('/modules', methods=['POST', 'GET'])
@login_required
def render_modules():
    sidenav = get_sidenav()
    
    if request.method == 'POST':
        if 'module_path' in request.form:
            module_path = request.form['module_path']

            with open('{}/module.json'.format(module_path)) as file:
                data = json.loads(file.read())
                module = data['module']

                if 'activated' in module:
                    activated = module['activated']
                else:
                    activated = False

                if activated:
                    activated = False
                else:
                    activated = True

                module['activated'] = activated

                with open('{}/module.json'.format(module_path), 'w') as jsonFile:
                    jsonFile.write(
                            json.dumps(
                                data,
                                sort_keys=True,indent=4,
                                separators=(',', ': ')
                                )
                            )

                    return redirect('admin/modules')

    modules = get_modules()

    return render_template('modules.html', sidenav=sidenav, modules=modules)
