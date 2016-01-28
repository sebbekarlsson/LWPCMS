from flask import Blueprint, render_template, abort, request, redirect, url_for

import glob

import json

from lwpcms.forms import UploadFileForm, PostForm
from lwpcms.api.files import upload_file
from lwpcms.api.posts import publish_post
from lwpcms.api.modules import call_module_event, get_modules
from lwpcms.api.themes import get_themes
from lwpcms.mongo import db

import pymongo as pymongo
from bson.objectid import ObjectId


bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/admin'
)

@bp.route('/')
def render():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin.html', side_nav_data=side_nav_data)


@bp.route('/publish/<id>', methods=['POST', 'GET']) 
@bp.route('/publish', defaults={'id': None}, methods=['POST', 'GET'])
def render_publish(id):
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    form = PostForm(csrf_enabled=False)

    post = None

    if id:
        post = db.collections.find_one({"_id": ObjectId(id)})
        if post and request.method != 'POST':    
            form.title.data = post["title"]
            form.content.data = post["content"]

    if form.validate_on_submit():
        attachment_ids = request.form.getlist('attachment_id')
        attachments = []

        for a_id in attachment_ids:
            if a_id is not None and len(a_id) > 3:
                attachment = db.collections.find_one({"_id": ObjectId(a_id)})

                if attachment is not None:
                    attachments.append(attachment)

        new_post = publish_post(
                           title=form.title.data,
                           content=form.content.data,
                           attachments=attachments,
                           id=id
                       )

        return redirect('/admin/publish/{}'.format(new_post["_id"]))
        

    return render_template('admin_publish.html', side_nav_data=side_nav_data,
            form=form, post=post, id=id)


@bp.route('/posts')
def render_posts():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    posts = list(
                db.collections.find(
                        {
                            "classes": ["post"]
                        }
                    ).sort('created', pymongo.DESCENDING)
                )
    return render_template('admin_posts.html', side_nav_data=side_nav_data,
            posts=posts)


@bp.route('/users')
def render_users():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_users.html', side_nav_data=side_nav_data)


@bp.route('/modules', methods=['POST', 'GET'])
def render_modules():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

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

    modules = get_modules()

    return render_template('admin_modules.html', side_nav_data=side_nav_data, modules=modules)


@bp.route('/themes', methods=['POST', 'GET'])
def render_themes():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())


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


        themes = get_themes()

    return render_template('admin_themes.html', side_nav_data=side_nav_data, themes=themes)


@bp.route('/files', methods=['POST', 'GET'])
def render_files():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    form = UploadFileForm(csrf_enabled=False)
    if form.validate_on_submit():
        upload_file(form.file.data, form.title.data)

    files = list(
                db.collections.find(
                    {
                        "classes": ["post", "file"]
                    }
                )
            )
    
    return render_template('admin_files.html',
        side_nav_data=side_nav_data,
        form=form,
        files=files
    )


@bp.route('/development')
def render_development():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())
    
    return render_template('admin_development.html',
            side_nav_data=side_nav_data)


@bp.route('/settings')
def render_settings():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_settings.html', side_nav_data=side_nav_data)
