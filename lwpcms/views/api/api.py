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


@bp.route('/delete_post/<id>', methods=['POST', 'GET'])
def delete_post(id):
    post = sess.query(Post).filter(Post.id==id).first()
    sess.delete(post)
    sess.commit()

    return 'ok', 200


@bp.route('/query_attachments/<query>', methods=['POST', 'GET'])
def query_attachments(query):
    attachments = sess.query(Post)\
            .filter(Post.type=='file')\
            .filter(Post.title.like('%{}%'.format(query)))\
            .all()
    print(attachments)
    return jsonify(
                {
                    'meta':{
                            'length': len(attachments)
                        },
                    'attachments':[
                        {
                            'id': attachment.id,
                            'title': attachment.title,
                            'content': attachment.content
                        }
                    for attachment in attachments]
               } 
            )
