from functools import wraps

import jwt
from customs import custom_response

from constants import SECRET_KEY
from flask import request


def authenticate(f):
    # def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # run some method that checks the request
        # for the client's authorization status
        if not 'Authorization' in request.headers:
            return custom_response(None, 'Not authenticated', status=412)
        token = request.headers['Authorization']
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        if not token:
            return custom_response(None, 'Not authenticated', status=412)

        # the user is authorized.
        # run the handler method and return the response
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return custom_response(None, 'Invalid token.', status=412)
        return f(*args, **kwargs)

    return decorated_function
