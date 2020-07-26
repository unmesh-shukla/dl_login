from app import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    encoding = db.Column(db.Text,  nullable=False, unique=True)
