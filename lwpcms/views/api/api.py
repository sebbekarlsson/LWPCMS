from flask import Blueprint, render_template, abort, request, send_file
from flask import jsonify

from lwpcms.mongo import db
from bson.objectid import ObjectId
import pymongo

from lwpcms.api.files import file_thumbnail, make_tarfile
from lwpcms.api.themes import get_themes

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
                +'/../../static/upload/{}'.format(file["filename"])
    )

    for size in [64, 32, 128]:
        os.remove(
            os.path.dirname(os.path.realpath(__file__))\
                +'/../../static/upload/{}'.format(
                    file_thumbnail(file["filename"], size)
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
                            "structure": "#File",
                            "filename": {"$regex": u"[a-zA-Z]*{}[a-zA-Z]*".format(query)}
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
                            "structure": "#File"
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
                            'filename': file["filename"],
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


@bp.route('/themes', methods=['POST', 'GET'])
def themes():
    all_themes = get_themes()

    for theme in all_themes:
        if not os.path.exists('lwpcms/themes/tar'):
            os.mkdir('lwpcms/themes/tar')
        
        tarname = 'lwpcms/themes/tar/{}.tar.gz'.format(theme['name'])

        if not os.path.exists(tarname):
            make_tarfile(tarname, 'lwpcms/' + theme['path'])

        theme['url'] = request.url_root + 'api/themes/download/{}'.format(theme['name'])


    print(request.url_root)
    return jsonify({'themes': all_themes})


@bp.route('/themes/download/<theme_name>', methods=['POST', 'GET'])
def themes_download(theme_name):
    theme = get_themes(theme_name)

    print(theme)
    return send_file('themes/tar/' + theme['name'] + '.tar.gz')
