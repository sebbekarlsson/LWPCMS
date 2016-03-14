from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.forms import PostForm
from lwpcms.api.user import login_required
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

    form = PostForm(csrf_enabled=False)

    post = None

    if id:
        post = db.collections.find_one({"_id": ObjectId(id)})
        if post and request.method != 'POST':    
            form.title.data = post["nick_name"]
            form.content.data = post["nick_name"]

    if form.validate_on_submit():
        file_ids = request.form.getlist('file_id')
        tags = request.form.getlist('lwpcms_tag')
        attachments = []

        for a_id in file_ids:
            if a_id is not None and len(a_id) > 3:
                file = db.collections.find_one({"_id": ObjectId(a_id)})

                if file is not None:
                    attachments.append(file)

        new_post = publish_post(
                           title=form.title.data,
                           content=form.content.data,
                           attachments=attachments,
                           published=form.published.data,
                           tags=tags,
                           id=id
                       )

        return redirect('/admin/edituser/{}'.format(new_post["_id"]))

    if post is None:
        form.published.data = True
       
    return render_template('editUser.html', sidenav=sidenav,
            form=form, post=post, id=id)
