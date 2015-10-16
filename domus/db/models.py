"""
The database models used by Flask-Restless

"""
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT
db = SQLAlchemy()


class Command(db.Model):
    __tablename__ = 'praeceptum'
    id = db.Column('id', db.Integer, primary_key=True)
    who = db.Column(db.String(255))
    what = db.Column(db.String(255))
    cts = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(TINYINT)
    error = db.Column(TINYINT)

    def __init__(self, who,what,cts):
        self.who = who
        self.what = what
        self.cts = datetime.utcnow()

