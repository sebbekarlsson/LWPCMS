from flask import Blueprint, render_template, abort
from lwpcms.models import sess, Post
from flask import jsonify

import os


bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/api'
)

@bp.route('/delete_file/<id>', methods=['POST', 'GET'])
def delete_file(id):
    file = sess.query(Post).filter(Post.id==id).first()
    os.remove(
        os.path.dirname(os.path.realpath(__file__))\
                +'/../../static/upload/{}'.format(file.content)
    )
    sess.delete(file)
    sess.commit()

    return 'ok', 200
