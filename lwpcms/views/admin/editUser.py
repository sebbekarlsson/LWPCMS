""" This route is used to render edituser page in the admin panel. """
from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.forms import UserForm
from lwpcms.api.user import login_required, register_user, user_exists
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
    msg = None

    if form.validate_on_submit():
        avatars = request.form.getlist('file_id')
        avatar = None
        if avatars is not None:
            if len(avatars) > 0:
                avatar = avatars[0]


        if avatar is not None:
            avatar_file = db.collections.find_one({'_id': ObjectId(avatar)})
        else:
            avatar_file = None

        if user_exists(form.user_name.data) and id is None:
            msg = 'User already exists'
            return render_template(
                    'editUser.html',
                    sidenav=sidenav,
                    form=form,
                    user=user,
                    id=id,
                    msg=msg
                    )

        new_user = register_user(
                name=form.user_name.data,
                password=form.password.data,
                avatar=avatar_file,
                id=id)

        if not id and new_user is not False:
            return redirect('/admin/edituser/{}'.format(new_user.inserted_id))

    if id:
        user = db.collections.find_one({"_id": ObjectId(id)})
        if user and request.method != 'POST':    
            form.user_name.data = user["nick_name"]
            form.password.data = user["password"]
        
    return render_template('editUser.html', sidenav=sidenav,
            form=form, user=user, id=id, msg=msg)
