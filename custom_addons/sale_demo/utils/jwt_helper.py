import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'DEMO_SECRET_KEY'
ALGORITHM = 'HS256'


def create_access_token(user):
    payload = {
        'uid': user.id,
        'login': user.login,
        'type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user):
    payload = {
        'uid': user.id,
        'type': 'refresh_token',
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
