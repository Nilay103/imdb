from database import mongo
from datetime import datetime, timedelta

import jwt
from passlib.handlers.sha2_crypt import sha256_crypt
from customs import custom_response
from constants import SECRET_KEY
from flask import Blueprint, request


registration_bp = Blueprint('registration_bp', __name__)

@registration_bp.route('/signup', methods=['POST'])
def signup():
    json = request.json
    name = json.get('name')
    email = json.get('email')
    pwd = json.get('pwd')

    if not name or not email or not pwd:
        return custom_response([], 'Please enter valid information.', 412)

    user = mongo.db.users.find_one({
        'name': name,
        'email': email
    })

    if user:
        return custom_response([], 'User Already Exists', status=412)

    #do not save pwd as a plain text
    _hashed_password = sha256_crypt.hash(pwd)
    # save details
    mongo.db.users.insert({'name': name, 'email': email, 'pwd': _hashed_password})
    return custom_response([], 'Success.', status=201)


@registration_bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = mongo.db.users.find_one({
        'email': body.get('email')
    })

    if not user:
        return custom_response(None, 'Please enter valid information.', status=412)
    try:
        sha256_crypt.verify(body.get('pwd'), sha256_crypt.hash(user['pwd']))
    except:
        return custom_response(None, 'Password mismatch.', status=412)

    token = jwt.encode({
        'user': user['_id'].__str__(),
        'expiration': str(datetime.utcnow() + timedelta(hours=1))
    }, SECRET_KEY)
    return custom_response(token, 'Login Successful.', status=201)
