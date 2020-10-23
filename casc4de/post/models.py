from datetime import datetime
from casc4de import db
from flask_login import current_user


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    posted_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    modified_date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    abstract = db.Column(db.String(300), nullable = True)
    content = db.Column(db.Text, nullable = False)
    cate_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    users = db.relationship('Users', backref = db.backref("post", lazy = True))
    category = db.relationship('Category', backref = db.backref("post", lazy = True))

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

    def __init__(self, title, abstract, cate_id, content):
        self.title = title
        self.abstract = abstract
        self.cate_id = cate_id
        self.posted_date = datetime.now()
        self.modified_date = datetime.now()
        self.user_id = current_user.id
        self.content = content