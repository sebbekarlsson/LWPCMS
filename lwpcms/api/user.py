from flask import session, redirect
from lwpcms.mongo import db
from bson.objectid import ObjectId
from lwpcms.models import Post
from functools import wraps


def get_current_user():
    if 'user_id' not in session:
        return None
    else:
        return db.collections.find_one(
            {
                '_id': ObjectId(session['user_id']),
                'type': 'user'
            }
        )


def register_user(name, password):
    user = Post(
                title=name,
                type='user',
                classes=['user'],
                meta={
                        'password': password
                    }
            ).export()

    return db.collections.insert_one(user)


def login_user(name, password):
    user = db.collections.find_one(
            {
                'title': name,
                'type': 'user'
            }
        )

    if user is None:
        return False
    else:
        real_password = user['meta']['password']

        if password == real_password:
            session['user_id'] = str(user['_id'])

            return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
