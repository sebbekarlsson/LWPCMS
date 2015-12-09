from flask import Blueprint, render_template, abort, request

import glob

import json


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


@bp.route('/publish')
def render_publish():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_publish.html', side_nav_data=side_nav_data)


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
                jsonFile.write(json.dumps(data))

    return render_template('admin_modules.html', side_nav_data=side_nav_data, modules=modules)


@bp.route('/files')
def render_files():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_files.html', side_nav_data=side_nav_data)


@bp.route('/settings')
def render_settings():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_settings.html', side_nav_data=side_nav_data)
