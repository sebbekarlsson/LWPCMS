from flask import Blueprint, render_template, abort
from flask import jsonify

from lwpcms.mongo import db
from bson.objectid import ObjectId

import os


bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/api'
)

@bp.route('/delete_file/<id>', methods=['POST', 'GET'])
def delete_file(id):
    file = db.collections.find_one({"_id": ObjectId(id)})
    os.remove(
        os.path.dirname(os.path.realpath(__file__))\
                +'/../../static/upload/{}'.format(file["content"])
    )
    db.collections.delete_many({"_id": ObjectId(id)})
    return 'ok', 200


@bp.route('/delete_post/<id>', methods=['POST', 'GET'])
def delete_post(id):
    db.collections.delete_many({"_id": ObjectId(id)})
    return 'ok', 200


@bp.route('/query_attachments/<query>', defaults={'page': 1})
@bp.route('/query_attachments/<query>/<page>', methods=['POST', 'GET'])
def query_attachments(query, page):

    if query != '*':
        attachments = list(
                    db.collections.find(
                        {
                            "classes": ["post", "file"],
                            "title": {"$regex": u"[a-zA-Z]*{}[a-zA-Z]*".format(query)}
                        }
                    )
                )
    else:
        attachments = list(
                    db.collections.find(
                        {
                            "classes": ["post", "file"]
                        }
                    )
                )

    return jsonify(
                {
                    'meta':{
                            'length': len(attachments)
                        },
                    'attachments':[
                        {
                            'id': str(attachment["_id"]),
                            'title': attachment["title"],
                            'content': attachment["content"],
                            'original': attachment['meta']['original_filename']
                        }
                    for attachment in attachments]
               } 
            )
