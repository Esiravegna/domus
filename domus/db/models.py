"""
The database models used by Flask-Restless

"""
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Command(db.Model):
    __tablename__ = 'praeceptum'
    id = db.Column('id', db.Integer, primary_key=True)
    who = db.Column(db.String(255))
    what = db.Column(db.String(255))
    when = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, who, what):
        self.who = who
        self.what = what
        self.when = datetime.utcnow()

