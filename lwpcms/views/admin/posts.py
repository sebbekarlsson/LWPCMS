""" This route is used for administration posts in the admin panel."""
from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
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

@bp.route('/posts', defaults={'page': 0})
@bp.route('/posts/<page>')
@login_required
def render_posts(page):
    sidenav = get_sidenav()

    page = int(page)
    limit = int(get_option('site_postspage_limit')['value'])

    query ={
        "classes": ["post"]
    }
    posts = list(
                db.collections.find(query).sort('created', pymongo.DESCENDING)\
                        .skip(page * limit).limit(limit)
                )
    page_count = int(db.collections.count(query) / limit)
    return render_template('posts.html', sidenav=sidenav,
            posts=posts, page_count=page_count)
