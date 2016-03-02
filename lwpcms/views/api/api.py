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


@bp.route('/query_files/<query>', defaults={'page': 0, 'limit': 100})
@bp.route('/query_files/<query>/<page>/<limit>', methods=['POST', 'GET'])
def query_files(query, page, limit):

    page = int(page)
    limit = int(limit)

    if query != '*':
        obj = db.collections.find(
                        {
                            "classes": ["post", "file"],
                            "title": {"$regex": u"[a-zA-Z]*{}[a-zA-Z]*".format(query)}
                        }
                    ).sort('created', pymongo.DESCENDING)
        if page != -1 and limit != -1:
            obj.skip(page * limit).limit(limit)

        files = list(
                    obj
                )
    else:
        obj = db.collections.find(
                        {
                            "classes": ["post", "file"]
                        }
                    ).sort('created', pymongo.DESCENDING)
        if page != -1 and limit != -1:
            obj.skip(page * limit).limit(limit)

        files = list(
                obj
                )

    return jsonify(
                {
                    'meta':{
                            'length': len(files)
                        },
                    'files':[
                        {
                            'id': str(file["_id"]),
                            'title': file["title"],
                            'content': file["content"],
                            'original': file['meta']['original_filename']
                        }
                    for file in files]
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
