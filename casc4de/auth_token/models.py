from casc4de import db
import bcrypt

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     username = db.Column(db.String(20),nullable = True)
#     password = db.Column(db.String(200), nullable = False)
#     email = db.Column(db.String(100), nullable = False, unique = True)

#     def __init__(self, username, password, email):
#         self.username = username
#         self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
#         self.email = email
    
#     def __repr__(self):
#         return self.id, self.username

#     def check_password(self, password):
#         if bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8')):
#             return True
#         return False
#     def set_password(self, password):
#         self.password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

#     def encode_auth_token(self, user_id):
#         """
#         Generates the auth token
#         return string
#         """
#     def to_dict(self):
#         return {
#             "username" : self.username,
#             "email" : self.email
#         }


class TokenBlackList(db.Model):
    __tablename__ = "tokenblacklist"
    id = db.Column(db.Integer, nullable = False, primary_key = True, autoincrement=True)
    jti = db.Column(db.String(36), nullable = False)
    token_type = db.Column(db.String(36), nullable = False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=True)
    expires = db.Column(db.DateTime, nullable=False)
    issue_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, token_type, user_identity, revoked, expires, issue_at):
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.revoked = revoked
        self.expires = expires
        self.issue_at = issue_at

    def to_dict(self):
        return {
            "id":self.id,
            "jti":self.jti,
            "token_type":self.token_type,
            "user_identity":self.user_identity,
            "revoke":self.iduser_identity,
            "expires":self.expires,
            "issue_at":self.issue_at,
            "revoked_at":self.revoked_at
        }