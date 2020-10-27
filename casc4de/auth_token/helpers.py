from functools import wraps
from flask.json import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request, decode_token
from flask import make_response
from logging import raiseExceptions
from .models import db, TokenBlackList
from datetime import datetime


# custom decorator that verifies JWT presents in request 
# and make sure that request is from user admin role
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return make_response(jsonify({"msg":"Admin only!", "status":"fail"}), 403)
        else:
            return fn(*args, **kwargs)
    return wrapper

def epoch_utc_to_datetime(timestamp):
    """ converts epoch timestamp to datetime format"""
    return datetime.fromtimestamp(timestamp)

def add_to_TokenBlackList(refresh_token):
    """
    add new refresh token to database
    """
    decode_tk = decode_token(refresh_token)
    exp = decode_tk["exp"]
    iat = decode_tk["iat"]
    jti = decode_tk["jti"]
    tk_type = decode_tk["type"]
    user_id = decode_tk["identity"]["id"]
    obj = TokenBlackList(
        jti=jti,
        token_type=tk_type,
        user_identity=user_id,
        revoked=False,
        expires=epoch_utc_to_datetime(exp),
        issue_at=epoch_utc_to_datetime(iat)
    )

    db.session.add(obj)
    db.session.commit()

def is_revoked(jti):
    """
    Verfify a given token is revoked or not;
    return: Boolean
    """
    # decode_tk = decode_token(token)
    # jti = decode_tk["jti"]
    try:
        data = TokenBlackList.query.filter_by(jti=jti).first()
        return data.revoked
    except Exception:
        return True

def revoke_token(jti):
    """
    Revokes a given token. Raise exception if token is not existed
    """
    # decode_tk = decode_token(token)
    # jti = decode_tk["jti"]
    try:
        data = TokenBlackList.query.filter_by(jti=jti).first()
        data.revoked = True
        data.revoked_at = datetime.now()
        db.session.commit()
    except Exception :
        raiseExceptions("jti is not existed")

def revoke_global(user_id):
    """
    revoke all tokens from a given user
    """
    try:
        tokens = TokenBlackList.query.filter(user_identity=user_id).all()
        for token in tokens:
            token.revoked_at = datetime.now()
            token.revoke = True
        db.session.commit()
    except Exception:
        raiseExceptions('User id is not existed')

def unrevoked_token(token):
    """
    Un revoked a given token. Raise exception if token is not existed
    """
    decode_tk = decode_token(token)
    jti = decode_tk["jti"]
    try:
        data = TokenBlackList.query.filter_by(jti=jti).first()
        data.revoked = False
        db.session.commit()
    except Exception :
        raiseExceptions("jti is not existed")

def get_user_tokens(user_id):
    """
    get all tokens from a given user id
    """
    try:
        return TokenBlackList.query.filter_by(user_identity=user_id).all()
    except Exception:
        raiseExceptions('User id is not existed')

def prune_database():
    """
    delete tokens which are expired in database
    should be called as a cron job
    """
    expired_tokens = TokenBlackList.query.filter(TokenBlackList.expire < datetime.now()).all()
    for token in expired_tokens:
        db.session.delete(token)
    db.session.commit()