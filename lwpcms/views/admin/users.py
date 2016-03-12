from flask import Blueprint, render_template, abort, request, redirect, url_for

from lwpcms.api.user import login_required
from lwpcms.api.posts import publish_post, get_option, set_option
from lwpcms.api.admin import get_sidenav

from lwpcms.mongo import db
import pymongo as pymongo

import os


bp = Blueprint(
    __name__, __name__,
    template_folder=os.path.dirname(os.path.dirname(__file__)) + '/../templates/admin',
    url_prefix='/admin'
)

@bp.route('/users')
@login_required
def render_users():
    sidenav = get_sidenav()

    users = list(
                db.collections.find(
                    {
                        'structure': '#User',
                    }
                )
            )

    return render_template('users.html', sidenav=sidenav, users=users)
