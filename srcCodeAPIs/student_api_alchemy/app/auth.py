import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from app import create_app

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_VALIDATION_CODE = "123456"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token manquant'}), 403
        try:
            jwt.decode(token, create_app().config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token invalide'}), 403
        return f(*args, **kwargs)
    return decorated