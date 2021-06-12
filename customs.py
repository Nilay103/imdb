import json
from bson import json_util
from flask import jsonify, make_response

def custom_response(data, message, status):
    count = len(data) if isinstance(data, list) else 1
    return make_response(json.loads(json_util.dumps({
        'count': count,
        'data': data,
        'message': message
    })), status)

# json.loads(json_util.dumps