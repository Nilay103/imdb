from functools import wraps

import jwt
from customs import custom_response

from constants import SECRET_KEY
from flask import request


def authenticate():
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            token = getattr(args[0], 'token')
            if not token:
                return custom_response(None, 'Not authenticated', status=412)

            # the user is authorized.
            # run the handler method and return the response
            try:
                jwt.decode(token, SECRET_KEY)
            except:
                return custom_response(None, 'Invalid token.', status=412)
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
