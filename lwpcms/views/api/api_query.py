from flask import Blueprint, abort, request, send_file
from flask import jsonify

from lwpcms.mongo import db
from bson.objectid import ObjectId
import pymongo


bp = Blueprint(
    __name__, __name__,
    template_folder='templates',
    url_prefix='/api'
)


@bp.route('/query', methods=['POST'])
def return_query():
    json_response = request.get_json()

    filter = None

    if 'query' in json_response:
        query = json_response['query']
    else:
        return jsonify({'status': 'Missing query field'}), 400

    if 'filter' in json_response:
        filter = json_response['filter']

    query = db.collections.find(query)
    
    if filter is not None:
        if 'skip' in filter:
            query.skip(filter['skip'])

        if 'limit' in filter:
            query.limit(filter['limit'])

    results = list(query)
    for result in results:
        result['_id'] = str(result['_id'])

    return jsonify({"results": results})
