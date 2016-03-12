from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.admin import get_sidenav

from lwpcms.mongo import db
import pymongo as pymongo
from bson.objectid import ObjectId

import os


bp = Blueprint(
    __name__, __name__,
    template_folder=os.path.dirname(os.path.dirname(__file__)) + '/../templates/admin',
    url_prefix='/admin'
)

@bp.route('/settings', methods=['POST', 'GET'])
@login_required
def render_settings():
    sidenav = get_sidenav()
    
    if request.method == 'POST':
        avail_options = request.form.getlist('avail_options')
        
        for key, value in request.form.items():
            if key in ['avail_options', 'lwpcms_tag']:
                continue

            if value == 'on':
                value = True
            else:
                value == False
            
            if type(value) is str:
                value = value.replace(', ', ',')

            set_option(key, value)

        for key in avail_options:
            if key not in request.form.keys():
                set_option(key, False)


    options = list(db.collections.find({'structure': '#Option'}))

    return render_template('settings.html', sidenav=sidenav, options=options)
