import flask
import flask.ext.restless
from domus.db.models import Command, db
from domus.utils.config import MYSQL_DB_SERVER, MYSQL_DB_USER, MYSQL_DB_PASS
from domus.utils.logger import master_log
log = master_log.name(__name__)
application = flask.Flask('application')
application.config['DEBUG'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}u@{}/domus'.format(MYSQL_DB_USER,MYSQL_DB_PASS,MYSQL_DB_SERVER)
application.config['SQLALCHEMY_ECHO'] = False

api_manager = flask.ext.restless.APIManager(application, flask_sqlalchemy_db=db)
api_manager.create_api(Command)



@application.route( '/')
def hello():
    return "Dominus?"

if __name__ == '__main__':
    db.init_app(application)
    application.run(host='0.0.0.0')

