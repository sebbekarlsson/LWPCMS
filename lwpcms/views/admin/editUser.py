from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.forms import UserForm
from lwpcms.api.user import login_required, register_user
from lwpcms.api.posts import publish_post
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

@bp.route('/edituser/<id>', methods=['POST', 'GET']) 
@bp.route('/edituser', defaults={'id': None}, methods=['POST', 'GET'])
@login_required
def render_publish(id):
    sidenav = get_sidenav()

    form = UserForm(csrf_enabled=False)

    user = None

    if id:
        user = db.collections.find_one({"_id": ObjectId(id)})
        if user and request.method != 'POST':    
            form.user_name.data = user["nick_name"]
            form.password.data = user["password"]

    if form.validate_on_submit():
        if id:
            new_user = register_user(
                    form.user_name.data,
                    form.password.data,
                    id)
        
    return render_template('editUser.html', sidenav=sidenav,
            form=form, user=user, id=id)
