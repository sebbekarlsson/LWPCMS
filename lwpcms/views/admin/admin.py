from flask import Blueprint, render_template, abort, request, redirect, url_for

import glob

import json

from lwpcms.forms import UploadFileForm, PostForm
from lwpcms.api.files import upload_file
from lwpcms.api.posts import publish_post
from lwpcms.models import sess, Post
from lwpcms.api.modules import call_module_event


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
        post = sess.query(Post)\
                .filter(Post.id==int(id), Post.type=='post')\
                .first()
        if post and request.method != 'POST':    
            form.title.data = post.title
            form.content.data = post.content

    if form.validate_on_submit():
        attachment_ids = request.form.getlist('attachment_id')
        attachments = []

        for a_id in attachment_ids:
            attachment = sess.query(Post).filter(Post.id==a_id).first()

            if attachment is not None:
                attachments.append(attachment)

        new_post = publish_post(title=form.title.data, content=form.content.data,
                attachments=attachments, id=id) 

        return redirect('/admin/publish/{}'.format(new_post.id))
        

    return render_template('admin_publish.html', side_nav_data=side_nav_data,
            form=form, post=post, id=id)


@bp.route('/posts')
def render_posts():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    posts = sess.query(Post)\
            .filter(Post.type=='post')\
            .order_by(Post.created.desc()).all()

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

    modules = []

    avail_modules = glob.glob('lwpcms/modules/*_module')
    for avail_module in avail_modules:
        with open('{}/module.json'.format(avail_module)) as file:
            data = json.loads(file.read())
            module = data['module']
            module['path'] = avail_module
            
            activated = False

            if 'activated' in module:
                activated = module['activated']

            module['activated'] = activated

            modules.append(module)

    if request.method == 'POST':
        if 'module_path' in request.form:
            module_path = request.form['module_path'] 
            
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

    return render_template('admin_modules.html', side_nav_data=side_nav_data, modules=modules)


@bp.route('/themes')
def render_themes():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_themes.html', side_nav_data=side_nav_data)


@bp.route('/files', methods=['POST', 'GET'])
def render_files():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    form = UploadFileForm(csrf_enabled=False)
    if form.validate_on_submit():
        upload_file(form.file.data, form.title.data)

    files = sess.query(Post)\
            .filter(Post.type=='file')\
            .order_by(Post.created.desc())\
            .all()
    
    return render_template('admin_files.html',
        side_nav_data=side_nav_data,
        form=form,
        files=files
    )


@bp.route('/settings')
def render_settings():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_settings.html', side_nav_data=side_nav_data)
