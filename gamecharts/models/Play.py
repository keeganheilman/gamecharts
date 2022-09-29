from .. import db

class Play(db.Model):
    id = db.Colum(db.Integer, primary_key=True)
    username = db.