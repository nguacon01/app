from collections import UserList
from operator import truediv
from bcrypt import checkpw

from flask import json
from flask_jwt_extended.utils import set_access_cookies, set_refresh_cookies

from flask import redirect, url_for, request, Blueprint, make_response, jsonify, make_response, render_template
from flask_jwt_extended import JWTManager as jwt, create_access_token, jwt_required
from flask_jwt_extended import get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from casc4de.auth.models import Users, db
from .models import TokenBlackList
import datetime
from . import helpers
from .helpers import admin_required

auth_token = Blueprint('auth_token', __name__, static_folder="static", template_folder="templates")

now = datetime.datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")

@auth_token.route("/index/")
@auth_token.route("/")
def index():
    return jsonify("authentication index page")

@auth_token.route('/login', methods=["POST", "GET"])
def login():
    """
        User from client connects to any api by sending to this server email and password which are registered.
        Auth server will send back to user client a access token and a refresh token
        access token is used to connect to api server and refresh token is used in case access token expiredss

    """
    if request.method == "POST":
        # get data from json request
        post_data = request.get_json()

        # email = request.args.get("email", None)
        # password = request.args.get("password", None)

        email = post_data.get("email", None)
        password = post_data.get("password", None)
        print(email, password)
        if not email:
            return make_response(jsonify({"msg":"email is not existed", "status":400}))
        if not password:
            return make_response(jsonify({"msg":"you need to type your password", "status":400}))

        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):

            access_token = create_access_token(
                identity={
                    "id":user.id,
                    "name":user.username
                }
            )
            refresh_token = create_refresh_token(
                identity={
                    "id":user.id,
                    "username":user.username
                }
            )
            # add refresh_token into database
            helpers.add_to_TokenBlackList(refresh_token)
            response = jsonify("dang nhap thanh cong")
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response, 201
        return make_response(jsonify({"msg":"Bad password or email", "status":401}))
    # return make_response(jsonify({"msg":"Please fill your email and password", "status":401}))
    return render_template("auth_token/login.html")

@auth_token.route('/refresh_token/', methods=['POST','GET'])
@jwt_refresh_token_required
def refresh_token():

    """
    refresh access token in case it is expired
    """
    curent_user = get_jwt_identity()
    jti = get_raw_jwt()["jti"]
    if helpers.is_revoked(jti):
        return make_response(jsonify({"msg":"Token has been revoked","status":"fail"}), 400)

    access_token = create_access_token(
        identity=curent_user
    )
    response = jsonify({"msg":"Refreshed Successfully"})
    set_access_cookies(response, access_token)
    return response, 201
@auth_token.route('/signup/', methods=["POST"])
def signup():
    # return str(request.form)
    if request.method == "POST":
        post_data = request.get_json()
        username = post_data.get("username", None)
        email = post_data.get("email", None)
        password = post_data.get("password", None)

        if not username or not email or not password:
            responseObj = {
                "msg":"Username, Password and Email are required",
                "status":"fail"
            }
            return make_response(jsonify(responseObj, 400))

        exist_user = Users.query.filter_by(email = email).first() 
        if exist_user is None:
            usr = Users(
                username = username,
                password = password,
                email = email
            )
            db.session.add(usr)
            db.session.commit()
            
            return make_response(jsonify({"msg":"User registration successfully","status":"success"}), 201)
        return make_response(jsonify({"msg":"User existed","status":"fail"}), 403)

@auth_token.route('/logout_access/', methods=["DELETE"])
@jwt_required
def logout_access():
    jti = get_raw_jwt()["jti"]
    blacklist = TokenBlackList(
        jti=jti,
        token_type=get_raw_jwt()["type"],
        user_identity=get_jwt_identity()["id"],
        revoked=True,
        expires=now
    )
    db.session.add(blacklist)
    db.session.commit()

    return make_response(jsonify({"msg":"User Loged out. Token revoked", "status":"success"}))

@auth_token.route('/logout/', methods=["DELETE"])
@jwt_refresh_token_required
def logout():
    jti = get_raw_jwt()["jti"]
    helpers.revoke_token(jti)
    return make_response(jsonify({"msg":"User Loged out. Refresh token revoked", "status":"success"}), 201)

@auth_token.route('/logout_global/', methods=["DELETE"])
@jwt_refresh_token_required
def logout_global():
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    helpers.revoke_global(user_id)
    return make_response(jsonify({"msg":"User Loged out. Refresh token revoked", "status":"success"}), 201)

@auth_token.route('/profile/', methods=["GET"])
@jwt_required
def profile():
    user_identity = get_jwt_identity()
    user_id = user_identity['id']
    user = Users.query.filter_by(id=user_id).first()
    if user:
        return make_response(jsonify({user_identity["name"]:user.to_dict(), "status":"success"}), 201)
    else:
        return make_response(jsonify({"msg":"User is not existed", "status":"fail"}), 403)

@auth_token.route('/edit/', methods=["PUT", "GET"])
@jwt_required
def edit():
    if request.method == "PUT":
        post_data = request.get_json()
        user_id = get_jwt_identity()["id"]

        user = Users.query.filter_by(id=user_id).first()
        if user:
            email = post_data['email']
            username = post_data.get('username', None)
            user.email = email
            user.username = username
            db.session.commit()
            return make_response(jsonify({"mes":"Update successfully", "status":"success"}), 201)
        else:
            return make_response(jsonify({"mes":"User is not existed", "status":"fail"}), 404)
    else:
        return 'Hi'

@auth_token.route('/change_password/', methods=["PUT", "GET"])
@jwt_required
def change_password():
    if request.method == "PUT":
        post_data = request.get_json()
        user_id = get_jwt_identity()["id"]

        user = Users.query.filter_by(id=user_id).first()
        if user:
            old_password = post_data['old_password']
            new_password = post_data['new_password']
            if user.check_password(old_password):
                user.setpassword(new_password)
                db.session.commit()
                return make_response(jsonify({"mes":"Update successfully", "status":"success"}), 201)
            else:
                return make_response(jsonify({"mes":"Your old password is not correct", "status":"fail"}), 403)
        else:
            return make_response(jsonify({"mes":"User is not existed", "status":"fail"}), 404)
    else:
        return 'Hi'

@auth_token.route('/users/', methods=["GET"])
@jwt_required
def users():
    users = Users.query.all()
    user_list = {}
    for user in users:
        user_list[user.id] = user.email

    return jsonify(user_list)