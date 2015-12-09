from flask import Blueprint, render_template, abort

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


@bp.route('/modules')
def render_modules():
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
        side_nav_data = json.loads(file.read())

    return render_template('admin_modules.html', side_nav_data=side_nav_data)


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
