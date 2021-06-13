import json

from bson import json_util
from flask import make_response


def custom_response(data, message, status):
    count = len(data) if isinstance(data, list) else 1
    return make_response(json.loads(json_util.dumps({
        'count': count,
        'data': data,
        'message': message
    })), status)


def custom_paginated_response(results, url, offset, limit):
    count = len(results)
    if limit < 0 or count < offset:
        return custom_response([], 'Invalid page lookup.', 412)

    # make response
    obj = {}
    obj['offset'] = offset
    obj['limit'] = limit
    obj['count'] = count

    if offset == 1:
        obj['previous'] = ''
    else:
        start_copy = offset - limit
        limit_copy = offset
        obj['previous'] = url + '?offset=%d&limit=%d' % (start_copy, limit_copy)

    if offset + limit > count:
        obj['next'] = ''
    else:
        start_copy = offset + limit
        obj['next'] = url + '?offset=%d&limit=%d' % (start_copy, limit)

    obj['data'] = results[offset:(offset + limit)]
    obj['message'] = 'Success.'
    return make_response(json.loads(json_util.dumps({
        **obj
    })), 201)
