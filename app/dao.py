import hashlib

from app import db
from app.models import User


def authenticate_user(username, password):
    return (db.session.query(User)
        .filter(User.username == username,User.password == hashlib.md5(password.encode('utf-8')).hexdigest()).first())


def get_user_by_id(user_id):
    return db.session.query(User).filter(User.id == user_id).first()