""" This route is used for managing settings in the admin panel."""
from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.admin import get_sidenav
from lwpcms.forms import SettingsForm

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

    form = SettingsForm(csrf_enabled=False)
    if form.validate_on_submit():
        set_option('site_demo', form.demo.data)
        set_option('site_name', form.site_name.data)
        set_option('site_description', form.site_description.data)
        site_tags = ','.join(request.form.getlist('lwpcms_tag'))
        set_option('site_tags', site_tags)
        set_option('site_filespage_limit', form.site_filespage_limit.data)
        set_option('site_postspage_limit', form.site_postspage_limit.data)
    
    is_demo = get_option('site_demo')
    if is_demo:
        form.demo.data = is_demo['value']

    site_name = get_option('site_name')
    if site_name:
        form.site_name.data = site_name['value']

    site_description = get_option('site_description')
    if site_description:
        form.site_description.data = site_description['value']

    site_tags = get_option('site_tags')
    if site_tags:
        site_tags = site_tags['value']
    else:
        site_tags = ''
    
    site_filespage_limit = get_option('site_filespage_limit')
    if site_filespage_limit:
        form.site_filespage_limit.data = site_filespage_limit['value']

    site_postspage_limit = get_option('site_postspage_limit')
    if site_postspage_limit:
        form.site_postspage_limit.data = site_postspage_limit['value']

    
    return render_template(
            'settings.html',
            sidenav=sidenav,
            site_tags=site_tags,
            form=form
            )
