from flask import Blueprint, render_template, url_for, redirect, jsonify, make_response
from flask_login import current_user
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, jwt_required
import os

main = Blueprint(
    "main",
     __name__,
     template_folder="templates",
     static_folder="static"
)

@main.route("/", methods=["GET"])
# @jwt_required
def index():
    return render_template("main/index.html")


@main.route("/protected1/", methods=["GET"])
@jwt_required
def protected1():
    response = make_response(jsonify({"msg":"nice try. This is protected link 1 in app folder", "status":"success"}), 201)
    return response

@main.route("/protected2/", methods=["GET"])
@jwt_required
def protected2():
    response = make_response(jsonify({"msg":"nice try. This is protected link 2 in app folder", "status":"success"}), 201)
    return response 