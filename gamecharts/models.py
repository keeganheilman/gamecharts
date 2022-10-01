from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pwd = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())

    def get_id(self):
        return self.user_id



# class Play(db.Model):
#     db_play_id