from flask import Blueprint, render_template, abort, request, redirect, url_for

import glob

import json

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
    template_folder=os.path.dirname(os.path.abspath(__file__)) + '/../../templates/admin',
    url_prefix='/admin'
)

print(bp.template_folder)

@bp.route('/')
@login_required
def render():
    sidenav = get_sidenav()

    return render_template('admin.html', sidenav=sidenav)
