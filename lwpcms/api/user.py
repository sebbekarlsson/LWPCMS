from flask import session, redirect
from lwpcms.mongo import db
from bson.objectid import ObjectId
from lwpcms.models import User
from functools import wraps


def get_current_user():
    if 'user_id' not in session:
        return None
    else:
        return db.collections.find_one(
            {
                '_id': ObjectId(session['user_id']),
                'structure': '#User'
            }
        )


def register_user(name, password, avatar=None, id=None):
    user = User(
                nick_name=name,
                password=password,
                avatar=avatar
            ).export()

    if not id:
        return db.collections.insert_one(user)
    else:
        return db.collections.update_one(
                {'structure': '#User', '_id': ObjectId(id)},
                {
                    '$set' : user
                })


def login_user(name, password):
    user = db.collections.find_one(
            {
                'nick_name': name,
                'structure': '#User'
            }
        )

    if user is None:
        return False
    else:
        real_password = user['password']
        print('real:' + real_password)

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
