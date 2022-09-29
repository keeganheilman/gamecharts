from .. import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pwd = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
