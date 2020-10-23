from datetime import datetime
from casc4de import db
from flask_login import current_user

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    created_date = db.Column(db.DateTime(), nullable = False, default = datetime.now())
    modified_date = db.Column(db.DateTime(), nullable = False, default = datetime.now())
    abstract = db.Column(db.String(300), nullable = True)
    # is_child = db.Column(db.Boolean, nullable = False, default = False)
    parent_id = db.Column(db.Integer, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    users = db.relationship('Users', backref = db.backref("category", lazy = True))

    def __repr__(self):
        return f"Post('{self.name}','{self.created_date}')"

    def __init__(self, name, abstract, parent_id=0):
        self.name = name
        self.abstract = abstract
        # self.is_child = is_child
        self.parent_id = parent_id
        self.created_date = datetime.now()
        self.modified_date = datetime.now()
        self.user_id = current_user.id