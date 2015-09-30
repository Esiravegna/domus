import flask
import flask.ext.sqlalchemy
import flask.ext.restless
from flask.ext.login import current_user, login_user, LoginManager, UserMixin

from flask.ext.restless import ProcessingException
from hashlib import md5
from datetime import datetime

application = flask.Flask(__name__)
application.config['DEBUG'] = True
application.config.from_pyfile('domus.cfg')

#login_manager = LoginManager()
#login_manager.init_app(app)

db = flask.ext.sqlalchemy.SQLAlchemy(application)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column('id', db.Integer, primary_key=True)
    board = db.Column(db.String(255))
    who = db.Column(db.String(255))
    why = db.Column(db.String(255))
    value = db.Column(db.Float)
    when = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, board, who, why, value):
        self.board = board
        self.who = who
        self.why = why
        self.value = value
        self.when = datetime.utcnow()


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column('id', db.Integer, primary_key=True)
    board = db.Column(db.String(255))
    who = db.Column(db.String(255))
    what = db.Column(db.String(255))
    value = db.Column(db.Float)
    when = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, board, who, what, value):
        self.board = board
        self.who = who
        self.what = what
        self.value = value
        self.when = datetime.utcnow()


class User(db.Model):
    __tablename__ = 'ostiarius'
    id = db.Column('id', db.Integer, primary_key=True)
    board = db.Column('board', db.String(32))
    hid = db.Column('hid', db.String(128))

    def __init__(self, board,hid):
        self.board = board
        self.hid = hid


api_manager = flask.ext.restless.APIManager(application, flask_sqlalchemy_db=db)
api_manager.create_api(User, methods=['GET'])
blueprint_Alert = api_manager.create_api(Alert)
api_manager.create_api(Event)

@application.route( '/')
def hello():
    return "Dominus?"



if __name__ == '__main__':
    application.run(host='0.0.0.0')

