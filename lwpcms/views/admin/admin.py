from flask import Blueprint, render_template, abort, request, redirect, url_for

import glob

import json

from lwpcms.forms import UploadFileForm, PostForm, SettingsForm
from lwpcms.api.files import upload_file
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.modules import call_module_event, get_modules
from lwpcms.api.themes import get_themes
from lwpcms.api.admin import get_sidenav
from lwpcms.api.user import login_required
from lwpcms.mongo import db

import pymongo as pymongo
from bson.objectid import ObjectId

import os
import shutil


bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/admin'
)

@bp.route('/')
@login_required
def render():
    sidenav = get_sidenav()

    return render_template('admin.html', sidenav=sidenav)


@bp.route('/publish/<id>', methods=['POST', 'GET']) 
@bp.route('/publish', defaults={'id': None}, methods=['POST', 'GET'])
@login_required
def render_publish(id):
    sidenav = get_sidenav()

    form = PostForm(csrf_enabled=False)

    post = None

    if id:
        post = db.collections.find_one({"_id": ObjectId(id)})
        if post and request.method != 'POST':    
            form.title.data = post["title"]
            form.content.data = post["content"]
            form.published.data = post['published']

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
                           published=form.published.data,
                           id=id
                       )

        return redirect('/admin/publish/{}'.format(new_post["_id"]))
        

    return render_template('admin_publish.html', sidenav=sidenav,
            form=form, post=post, id=id)


@bp.route('/posts')
@login_required
def render_posts():
    sidenav = get_sidenav()

    posts = list(
                db.collections.find(
                        {
                            "classes": ["post"]
                        }
                    ).sort('created', pymongo.DESCENDING)
                )
    return render_template('admin_posts.html', sidenav=sidenav,
            posts=posts)


@bp.route('/users')
@login_required
def render_users():
    sidenav = get_sidenav()

    users = list(
                db.collections.find(
                    {
                        'structure': 'User',
                    }
                )
            )

    return render_template('admin_users.html', sidenav=sidenav, users=users)


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

    return render_template('admin_modules.html', sidenav=sidenav, modules=modules)


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

    return render_template('admin_themes.html', sidenav=sidenav, themes=themes)


@bp.route('/files', methods=['POST', 'GET'])
@login_required
def render_files():
    sidenav = get_sidenav()

    form = UploadFileForm(csrf_enabled=False)
    if form.validate_on_submit():
        upload_file(form.file.data, form.title.data)

    files = list(
                db.collections.find(
                    {
                        "classes": ["post", "file"]
                    }
                ).sort('created', pymongo.DESCENDING)
            )
    return render_template('admin_files.html',
        sidenav=sidenav,
        form=form,
        files=files
    )


@bp.route('/settings', methods=['POST', 'GET'])
@login_required
def render_settings():
    sidenav = get_sidenav()

    form = SettingsForm(csrf_enabled=False)
    if form.validate_on_submit():
        set_option('site_demo', form.demo.data)
        set_option('site_name', form.site_name.data)
        set_option('site_description', form.site_description.data)
        site_tags = ','.join(request.form.getlist('lwpcms_tag'))
        set_option('site_tags', site_tags)
    
    is_demo = get_option('site_demo')
    if is_demo:
        is_demo = is_demo['value']

    site_name = get_option('site_name')
    if site_name:
        site_name = site_name['value']

    site_description = get_option('site_description')
    if site_description:
        site_description = site_description['value']

    site_tags = get_option('site_tags')
    if site_tags:
        site_tags = site_tags['value']
    else:
        site_tags = ''

    form.demo.data = is_demo
    form.site_name.data = site_name
    form.site_description.data = site_description

    return render_template('admin_settings.html', sidenav=sidenav, site_tags=site_tags, form=form)
