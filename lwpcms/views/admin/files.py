from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.forms import UploadFileForm
from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.admin import get_sidenav
from lwpcms.api.files import upload_file

from lwpcms.mongo import db
import pymongo as pymongo
from bson.objectid import ObjectId

import os


bp = Blueprint(
    __name__, __name__,
    template_folder=os.path.dirname(os.path.dirname(__file__)) + '/../templates/admin',
    url_prefix='/admin'
)


@bp.route('/files', defaults={'page': 0}, methods=['POST', 'GET'])
@bp.route('/files/<page>', methods=['POST', 'GET'])
@login_required
def render_files(page):
    sidenav = get_sidenav()

    form = UploadFileForm(csrf_enabled=False)
    if form.validate_on_submit():
        files = request.files.getlist('file')
        
        for file in files:
            upload_file(file)

    page = int(page)
    limit = int(get_option('site_filespage_limit')['value'])
    
    query = {
            'structure': '#File'
    }
    files = list(
                db.collections.find(query).sort('created', pymongo.DESCENDING).skip(page * limit)\
                        .limit(limit)
            )
    page_count = int(db.collections.count(query) / limit)
    return render_template('files.html',
        sidenav=sidenav,
        form=form,
        files=files,
        page_count=page_count
    )
