from flask import session, redirect
from lwpcms.mongo import db
from bson.objectid import ObjectId
from lwpcms.models import User
from functools import wraps


def get_current_user():
    """ Return Object
    This function is used to get the current user object.
    """
    if 'user_id' not in session:
        return None
    else:
        return db.collections.find_one(
            {
                '_id': ObjectId(session['user_id']),
                'structure': '#User'
            }
        )

def user_exists(name):
    """ Return Boolean
    This function is used to check if an user exists.
    """
    existing = db.collections.find_one({
            'structure': '#User',
            'nick_name': name
        })

    return existing is not None


def register_user(name, password, avatar=None, id=None):
    """ Return Boolean
    This function is used to register a new user.
    """
    existing = db.collections.find_one({
            'structure': '#User',
            'nick_name': name
        })
    if existing is not None and id is None:
        return False

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
    """ Return Boolean
    This funciton is used to login a user.
    """
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
    """
    This is a wrapper for routes.
    Routes are decorated with this function to make them secure and require
    a login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user():
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
