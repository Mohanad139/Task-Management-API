from passlib.context import CryptContext
import bcrypt
from database import getuser
from jose import jwt
import secrets
from datetime import datetime, timedelta



SECRET_KEY = 'c3a4c87dbba5c6e2a192069f6adca8d7ac5185cf2ff47f71dcbd4852fb3ee178'



def hash_password(password):
    password_bytes = password.encode('utf-8')

    hashed = bcrypt.hashpw(password_bytes,bcrypt.gensalt())

    return hashed.decode('utf-8')

def verify_password(plain,hashed):
    password = plain.encode('utf-8')
    hashpass = hashed.encode('utf-8')

    return bcrypt.checkpw(password,hashpass)


def create_access_token(username: str):

    payload = {
        'sub' : username,
        'exp' : datetime.utcnow() +  timedelta(hours=24)
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['sub']
        return username
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.JWTError:
        return None  
