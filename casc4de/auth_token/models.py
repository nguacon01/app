from casc4de import db
import bcrypt

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