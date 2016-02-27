from flask import Blueprint, render_template, abort
from flask import jsonify

from lwpcms.mongo import db
from bson.objectid import ObjectId
import pymongo

from lwpcms.api.files import file_thumbnail

import os


bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/api'
)

@bp.route('/delete_file/<id>', methods=['POST', 'GET'])
def delete_file(id):
    file = db.collections.find_one({"_id": ObjectId(id)})
    print(file['content'])
    os.remove(
        os.path.dirname(os.path.realpath(__file__))\
                +'/../../static/upload/{}'.format(file["content"])
    )

    for size in [64, 32, 128]:
        os.remove(
            os.path.dirname(os.path.realpath(__file__))\
                +'/../../static/upload/{}'.format(
                    file_thumbnail(file["content"], size)
                    )
        )

    db.collections.delete_many({"_id": ObjectId(id)})
    return 'ok', 200


@bp.route('/delete_post/<id>', methods=['POST', 'GET'])
def delete_post(id):
    db.collections.delete_many({"_id": ObjectId(id)})
    return 'ok', 200


@bp.route('/query_attachments/<query>', defaults={'page': 0})
@bp.route('/query_attachments/<query>/<page>', methods=['POST', 'GET'])
def query_attachments(query, page):

    page = int(page)
    limit = 100

    if query != '*':
        attachments = list(
                    db.collections.find(
                        {
                            "classes": ["post", "file"],
                            "title": {"$regex": u"[a-zA-Z]*{}[a-zA-Z]*".format(query)}
                        }
                    ).skip(page * limit).limit(limit).sort('created', pymongo.DESCENDING)
                )
    else:
        attachments = list(
                    db.collections.find(
                        {
                            "classes": ["post", "file"]
                        }
                    ).skip(page * limit).limit(limit).sort('created', pymongo.DESCENDING)
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


@bp.route('/remove_attachment/<post_id>/<attach_id>', methods=['POST', 'GET'])
def remove_attachment(post_id, attach_id):
    db.collections.update_one(
                {
                    '_id': ObjectId(post_id)
                },
                {
                    '$pull': {
                        'attachments': {
                             '_id': ObjectId(attach_id)
                         }
                    }
                }
            )
    return jsonify({
            'status': 200
        }), 200
