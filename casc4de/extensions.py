from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from logging import DEBUG, FileHandler, WARNING
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

# filehandle = FileHandler("log.txt")
# filehandle.setLevel(DEBUG)

